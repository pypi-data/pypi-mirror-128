import itertools as it
from time import sleep
from typing import Callable, Dict, Tuple, Type
from math import inf
from multiprocess import Pool
import numpy as np
import pandas as pd
import nevergrad as ng
import matplotlib.pyplot as plt
from .Strategy import Strategy


def calc_efficiency(train_profit: float, test_profit: float) -> float:
    if train_profit <= 0:
        return np.nan
    return round((test_profit / train_profit) * 100, 2)


def get_calc_strategy_func(strategy: Type[Strategy], brut=False, direction=Strategy.LONG) -> Callable:
    """ Получить функцию для расчета минимумов по стратегии """
    s = strategy

    if brut:
        def calc_strategy_profit(df, params) -> float:
            s_obj = s()
            s_obj.tune(for_opt=True, direction=direction)
            s_obj.run(df, params)
            return -s_obj.coef
    else:
        def calc_strategy_profit(df, **params) -> float:
            s_obj = s()
            s_obj.tune(for_opt=True, direction=direction)
            s_obj.run(df, params)
            return -s_obj.coef
    return calc_strategy_profit


def find_best_params_optimization(
        calc_strategy: Callable,
        df: pd.DataFrame,
        param_ranges: Dict[str, list]
) -> Tuple[float, Dict[str, float]]:
    """ Поиск лучшех параметров подбором с оптимизацией"""
    params = {}
    combinations = 0
    for param_name in param_ranges:
        if combinations == 0:
            combinations = len(param_ranges[param_name])
        else:
            combinations *= len(param_ranges[param_name])
        params[param_name] = ng.p.TransitionChoice(param_ranges[param_name])
    parametrization = ng.p.Instrumentation(
        df=ng.p.TransitionChoice([df]),
        **params
    )
    budget = int(combinations * 0.25)
    budget = max(80, budget)
    optimizer = ng.optimizers.NGOpt(parametrization=parametrization, budget=budget)
    recommendation = optimizer.minimize(calc_strategy)
    best_params = recommendation.kwargs
    del best_params['df']
    best_coef = calc_strategy(df, **best_params)
    return -best_coef, best_params


def find_best_params_brut_parallel(
        calc_strategy: Callable,
        df: pd.DataFrame,
        param_ranges: Dict[str, list]
) -> Tuple[float, Dict[str, float]]:
    """ Поиск лучшех параметров подбором с параллелизацией """
    param_ranges_list = []
    for param_range in param_ranges.values():
        param_ranges_list.append(param_range)
    combs = list(it.product(*param_ranges_list))
    param_names = list(param_ranges.keys())
    best_coef = inf
    best_params = {}
    tasks = {}
    params = {}
    with Pool(12) as pool:
        for i, comb in enumerate(combs):
            args = dict(zip(param_names, comb))
            tasks[i] = pool.apply_async(calc_strategy, (df, args))
            params[i] = args
        while len(tasks):
            for i, task in tasks.copy().items():
                if task.ready():
                    coef = task.get()
                    del tasks[i]
                    if coef < best_coef:
                        best_coef = coef
                        best_params = params[i]
    return -best_coef, best_params


def find_best_params_brut(
        calc_strategy: Callable,
        df: pd.DataFrame,
        param_ranges: Dict[str, list]
) -> Tuple[float, Dict[str, float]]:
    """ Поиск лучшех параметров подбором """
    param_ranges_list = []
    for param_range in param_ranges.values():
        param_ranges_list.append(param_range)
    combs = list(it.product(*param_ranges_list))
    param_names = list(param_ranges.keys())
    best_coef = inf
    best_params = {}
    for comb in combs:
        args = dict(zip(param_names, comb))
        coef = calc_strategy(df, args)
        if coef < best_coef:
            best_coef = coef
            best_params = args
    return -best_coef, best_params


class Epoch:
    """ Данные по эпохе """

    def __init__(self):
        self.task = None

        self.df_train: pd.DataFrame = None
        self.df_test: pd.DataFrame = None

        self.strategy_train: Strategy = None
        self.strategy_test: Strategy = None

        self.best_params = {}
        self.is_done = False

    def get_train_ts(self) -> Dict[str, int]:
        """ Получить временные метки эпохи обучения """
        return {
            'start': int(self.df_train['close_time'][0] / 1000),
            'end': int(self.df_train['close_time'][len(self.df_train) - 1] / 1000)
        }

    def get_test_ts(self) -> Dict[str, int]:
        """ Получить временные метки эпохи теста """
        return {
            'start': int(self.df_test['close_time'][0] / 1000),
            'end': int(self.df_test['close_time'][len(self.df_test) - 1] / 1000)
        }


class FakeTask:
    """ Фейковая задача """

    def __init__(self, func, params):
        self.func = func
        self.params = params

    def ready(self):
        return True

    def get(self):
        return self.func(*self.params)


class BaseForward:
    """ Форвардный анализ """

    def __init__(self):
        self.result: pd.DataFrame = None

        self.df: pd.DataFrame = None
        self.param_ranges = {}
        self.strategy: Type[Strategy] = None

        self.epoch_strategies = {}

        self.train_window = 0
        self.test_window = 0
        self.train_window_days = 0
        self.test_window_days = 0

        self.epochs_data: Dict[int, Epoch] = {}

        self.pool: Pool = None
        self.done_tasks = 0

        self.direction = Strategy.LONG

    def run(self, strategy: Type[Strategy], df: pd.DataFrame, param_ranges: Dict[str, list],
            train_window_days: int, test_window_days: int):
        """ Запустить форвардный анализ """
        self.df = df
        self.param_ranges = param_ranges
        self.strategy = strategy

        self.result = pd.DataFrame(
            columns=['epoch', 'coef_eff', 'train_rel_profit', 'test_profit'] + list(param_ranges.keys())
        )

        self.train_window_days = train_window_days
        self.test_window_days = test_window_days

        self.train_window = train_window_days * 24 * 60
        self.test_window = test_window_days * 24 * 60

        self.init_epochs_data()
        self.done_tasks = 0

        self.pool = Pool(processes=12)
        try:
            self.create_tasks()
            self.monitor_tasks()
        finally:
            self.pool.close()

    def init_epochs_data(self):
        """ Инициализировать данные по эпохам """
        epochs = int((len(self.df) - self.train_window) / self.test_window)
        for epoch in range(epochs):
            self.epochs_data[epoch] = Epoch()

            epoch_start_learn = epoch * self.test_window
            epoch_end_learn = epoch_start_learn + self.train_window
            self.epochs_data[epoch].df_train = self.df[epoch_start_learn:epoch_end_learn].reset_index(drop=True)

            epoch_start_test = epoch_end_learn
            epoch_end_test = epoch_start_test + self.test_window
            self.epochs_data[epoch].df_test = self.df[epoch_start_test:epoch_end_test].reset_index(drop=True)

    def create_tasks(self):
        pass

    def monitor_tasks(self):
        """ Мониторить задачи """
        total_tasks = len(self.epochs_data)
        while self.done_tasks < total_tasks:
            print("\r ", end="")
            print(f' leave epochs: {self.done_tasks}/{total_tasks}'.ljust(40), end="")
            for epoch, epoch_data in self.epochs_data.items():
                if epoch_data.is_done is False and epoch_data.task.ready():
                    self.done_tasks += 1
                    self.epochs_data[epoch].is_done = True

                    train_coef, best_params = epoch_data.task.get()
                    self.epochs_data[epoch].best_params = best_params

                    test_strategy = self.strategy()
                    test_strategy.tune(direction=self.direction)
                    test_strategy.run(epoch_data.df_test, best_params)
                    test_profit = test_strategy.get_profit()

                    train_strategy = self.strategy()
                    train_strategy.tune(direction=self.direction)
                    train_strategy.run(epoch_data.df_train, best_params)
                    train_profit = train_strategy.get_profit()
                    train_rel_profit = train_profit * self.test_window_days / self.train_window_days

                    self.result = self.result.append({
                        'epoch': epoch,
                        'train_coef': train_coef,
                        'train_rel_profit': train_rel_profit,
                        'test_profit': test_profit,
                        'coef_eff': calc_efficiency(train_rel_profit, test_profit),
                        **best_params
                    }, ignore_index=True)
                    self.epochs_data[epoch].strategy_test = test_strategy
                    self.epochs_data[epoch].strategy_train = train_strategy
                    print("\r ", end="")
                    print(f' leave epochs: {self.done_tasks}/{total_tasks}'.ljust(40), end="")
            sleep(0.1)

        print("\r ", end="")
        print(f' leave epochs: {self.done_tasks}/{total_tasks}'.ljust(40))
        self.result = self.result.sort_values('epoch').reset_index(drop=True)

    def get_epoch(self, number: int) -> Epoch:
        """ Получить эпоху """
        return self.epochs_data[number]

    def draw_train_profit(self):
        plt.plot(self.result['train_rel_profit'].cumsum())
        plt.show()

    def draw_test_profit(self):
        plt.plot(self.result['test_profit'].cumsum())
        plt.show()

    def draw_profit(self):
        plt.plot(self.result['test_profit'].cumsum())
        plt.plot(self.result['train_rel_profit'].cumsum())
        plt.show()

    def calc_full_test(self) -> pd.DataFrame:
        trades = pd.DataFrame(
            columns=['open_time', 'close_time', 'av_price', 'close',
                     'volume', 'profit', 'max_drawdown', 'max_possible_profit']
        )
        last_stop = 0
        for epoch in self.epochs_data.values():
            start, stop = epoch.get_test_ts().values()
            start *= 1000
            stop *= 1000
            start = max(start, last_stop)
            strategy = self.strategy()
            strategy.tune(direction=self.direction)
            strategy.run(self.df, epoch.best_params)
            epoch_trades = strategy.trades
            epoch_trades = epoch_trades[(epoch_trades['open_time'] >= start) & (epoch_trades['open_time'] <= stop)]
            trades = trades.append(epoch_trades, ignore_index=True)
            total_trades = len(trades)
            if total_trades:
                last_stop = trades['open_time'][total_trades - 1] + 1
        return trades


class ForwardOpt(BaseForward):
    """ Форвардный анализ с оптимизацией, паралельный просчет эпох """

    def create_tasks(self):
        """ Создать задачи """
        for epoch, epoch_data in self.epochs_data.copy().items():
            self.epochs_data[epoch].task = self.pool.apply_async(find_best_params_optimization, (
                get_calc_strategy_func(self.strategy, direction=self.direction),
                epoch_data.df_train,
                self.param_ranges
            ))


class ForwardBrut(BaseForward):
    """ Форвардный анализ, паралельный просчет эпох """

    def create_tasks(self):
        """ Создать задачи """
        for epoch, epoch_data in self.epochs_data.copy().items():
            self.epochs_data[epoch].task = self.pool.apply_async(find_best_params_brut, (
                get_calc_strategy_func(self.strategy, brut=True, direction=self.direction),
                epoch_data.df_train,
                self.param_ranges
            ))


class ForwardParallelBrut(BaseForward):
    """ Форвардный анализ, паралельный подбор параметров """

    def create_tasks(self):
        """ Создать задачи """
        for epoch, epoch_data in self.epochs_data.copy().items():
            self.epochs_data[epoch].task = FakeTask(find_best_params_brut_parallel, [
                get_calc_strategy_func(self.strategy, brut=True, direction=self.direction),
                epoch_data.df_train,
                self.param_ranges
            ])

