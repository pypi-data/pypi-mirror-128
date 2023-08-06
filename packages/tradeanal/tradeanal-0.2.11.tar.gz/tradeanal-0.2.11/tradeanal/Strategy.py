import math
from functools import reduce
import pandas as pd
import matplotlib.pyplot as plt


class Strategy():
    """ Стратегия """

    LONG = 'long'
    SHORT = 'short'

    def __init__(self):

        # Датафрейм для обсчета
        self.df: pd.DataFrame = None

        # Датафрейм со сделками
        self.trades: pd.DataFrame = None

        # Временный массив под сделки
        self.trades_temp = []

        # Временный мессив с позициями
        self.position_value_arr = []

        # Данные по ценам и времени открытия по сделкам текущей позиции
        self.current_position_opens = []

        # Количество сделок в текущей позиции
        self.position = 0

        # Средняя цена позиции
        self.av_price = 0

        # Просадка по позиции
        self.drawdown = math.inf

        # Максимальный профит по позиции
        self.possible_profit = -math.inf

        # Коэф анализу
        self.coef = 0

        # Объем лота сделки в доллагах
        self.lot_dollars = 10

        # Направление торговли
        self.direction = self.LONG

        # Запуск только для оптимизации
        self.for_opt = False

    def tune(self, lot_dollars: float = None, direction: str = None, for_opt: bool = None):
        """ Установить настройки """
        for setting_name, value in locals().items():
            if value is not None:
                self.__setattr__(setting_name, value)

    def increase_position(self, row):
        """ Увеличить позицию """
        self.position += 1
        self.current_position_opens.append({
            'time': row.close_time,
            'price': row.close
        })
        self.av_price = reduce(lambda s, x: s + x['price'], self.current_position_opens, 0) / self.position

    def close_position(self, row):
        """ Закрыть позицию """
        profit = self.calc_trade_profit(self.av_price, row.close, self.position)
        self.trades_temp.append({
            'open_time': self.current_position_opens[0]['time'],
            'close_time': row.close_time,
            'av_price': self.av_price,
            'close': row.close,
            'volume': self.position,
            'profit': profit,
            'max_drawdown': self.drawdown,
            'max_possible_profit': self.possible_profit
        })
        self.coef += self.calc_trade_coef(profit)
        self.reset_position_state()

    def calc_trade_profit(self, open_price: float, close_price: float, volume: float) -> float:
        """ Сосчитать профит по сделке """
        diff = close_price - open_price
        if self.direction == self.SHORT:
            diff = -diff
        return self.lot_dollars * volume / open_price * (diff - 0.0004 * (close_price + open_price))

    def reset_position_state(self):
        """ Сбросить состояние между позициями """
        self.current_position_opens = []
        self.position = 0

        self.drawdown = math.inf
        self.possible_profit = -math.inf

    def reset_process_state(self):
        """ Сбросить состояние между обсчетами"""
        self.trades = None

        self.trades_temp = []
        self.position_value_arr = []

        self.coef = 0

    def run(self, df: pd.DataFrame, params: dict):
        """ Запустить расчеты """
        self.reset_process_state()
        self.reset_position_state()
        self.process(df, params)
        self.set_data_after_process(df)

    def set_data_after_iter(self, row):
        """ Рассчитать максимальные диапазоны профита внутри сделки """
        if self.position > 0:
            current_profit = self.calc_trade_profit(self.av_price, row.close, self.position)
            self.drawdown = min(current_profit, self.drawdown)
            self.possible_profit = max(current_profit, self.drawdown)
        self.position_value_arr.append(self.position)

    def set_data_after_process(self, df: pd.DataFrame):
        if self.for_opt is False:
            self.df = df.copy()
            self.df['position'] = self.position_value_arr
            self.trades = pd.DataFrame(
                self.trades_temp,
                columns=['open_time', 'close_time', 'av_price', 'close',
                         'volume', 'profit', 'max_drawdown', 'max_possible_profit']
            )

    def process(self, df: pd.DataFrame, params: dict):
        """ Обработать датафрем по тратегии """
        pass

    def get_profit(self) -> float:
        """ Получить профит по стратегии """
        return self.trades['profit'].sum()

    @staticmethod
    def calc_trade_coef(profit) -> float:
        """ Рассчитать COEF по сделке """
        if profit < 0:
            return profit + 1.05 ** profit - 1
        return profit

    def draw_cum(self):
        """ Отрисовать кумуляту сделок """
        plt.plot(self.trades['close_time'].values, self.trades['profit'].cumsum().values)
        plt.show()

    def draw_cum_and_price(self):
        """ Отрисовать кумуляту сделок и цену"""
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.plot(self.df['close_time'].values, self.df['close'].values, label='Цена', color='darkred')
        ax2.plot(self.trades['close_time'].values, self.trades['profit'].cumsum().values, label='Прибыль')
        ax1.set_ylabel('Цена')
        ax2.set_ylabel('Прибыль')
        fig.legend()
        plt.show()

    @staticmethod
    def draw_positions(df, need_av_enter=True):
        """ Отрисовать позиции на датафрейме """
        df = df.reset_index(drop=True)
        df['pos_diff'] = df['position'].diff()
        trade_inputs = df[df['pos_diff'] > 0]
        trade_outputs = df[df['pos_diff'] < 0]
        plt.plot(df['close_time'].values, df['close'].values, color='orange')
        plt.plot(df['close_time'].values, df['ma'].values)
        if need_av_enter:
            av_price = trade_inputs['close'].mean()
            plt.plot(
                [df['close_time'][0], df['close_time'][len(df) - 1]],
                [av_price, av_price],
                linestyle='--',
                color='#9EF5A1'
            )
        plt.scatter(trade_inputs['close_time'].values, trade_inputs['close'].values, marker="^", c='green', zorder=10)
        plt.scatter(trade_outputs['close_time'].values, trade_outputs['close'].values, marker="v", c='red', zorder=10)
        plt.show()

    def get_df_by_trade_index(self, trade_index: int) -> pd.DataFrame:
        """ Получить датафрейм по индексу сделки """
        start_ts = self.trades['open_time'][trade_index]
        end_ts = self.trades['close_time'][trade_index]
        return self.df[(self.df['close_time'] >= start_ts) & (self.df['close_time'] <= end_ts)]
