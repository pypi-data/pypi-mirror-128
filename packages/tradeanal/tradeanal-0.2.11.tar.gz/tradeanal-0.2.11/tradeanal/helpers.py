import os
from datetime import datetime
from time import sleep

import pandas as pd
import numpy as np
from binance.client import Client
from binance.enums import HistoricalKlinesType
from ta.volatility import average_true_range
from ta.trend import sma_indicator


def download_data(ticket: str, ts_start: int, ts_end: int = 0,
                  timeframe: str = Client.KLINE_INTERVAL_1MINUTE) -> pd.DataFrame:
    """ Скачать данные с Binance API """
    client = Client('', '')
    titles = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'Quote asset volume',
              'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Can be ignored']
    data_generator = client.get_historical_klines_generator(
        symbol=ticket,
        interval=timeframe,
        start_str=ts_start * 1000,
        end_str=None if ts_end == 0 else ts_end * 1000,
        klines_type=HistoricalKlinesType.FUTURES
    )
    rows = []
    for row in data_generator:
        rows.append(row)
    df = pd.DataFrame(rows, columns=titles)
    df = df[['close_time', 'close', 'open', 'high', 'low', 'volume']]
    df[['close', 'open', 'high', 'low', 'volume']] = df[['close', 'open', 'high', 'low', 'volume']].astype(np.float64)
    return df


def calc_rel_atr(df: pd.DataFrame, atr_window: int) -> pd.Series:
    """ Расчитать относительный АТР """
    return average_true_range(df['high'], df['low'], df['close'], window=atr_window) / df['close'] * 100


def cal_rel_atr_by_other_timeframe(df: pd.DataFrame, ticket: str, atr_window: int,
                                   timeframe: str = Client.KLINE_INTERVAL_1DAY) -> pd.Series:
    """ Получить атр для другого таймфрейма"""
    period_seconds = {
        Client.KLINE_INTERVAL_1DAY: 24 * 60 * 60,
        Client.KLINE_INTERVAL_4HOUR: 4 * 60 * 60,
        Client.KLINE_INTERVAL_1HOUR: 1 * 60 * 60,
        Client.KLINE_INTERVAL_30MINUTE: 30 * 60,
        Client.KLINE_INTERVAL_15MINUTE: 15 * 60
    }[timeframe]
    df_start_date = int(df['close_time'][0] / 1000)
    df_end_date = int(df['close_time'][len(df) - 1] / 1000)
    data = download_data(ticket, df_start_date - (atr_window + 1) * period_seconds, df_end_date, timeframe)
    data['atr'] = calc_rel_atr(data, atr_window)
    atr_by_days = {int(row['close_time']): row['atr'] for i, row in data.iterrows()}
    del data
    atr_arr = []
    for row in df.itertuples():
        for ts, atr in atr_by_days.copy().items():
            diff = (row.close_time - ts) / 1000
            if diff > period_seconds:
                del atr_by_days[ts]
            else:
                atr_arr.append(atr)
                break
    return pd.Series(atr_arr)


def cal_ma_by_other_timeframe(df: pd.DataFrame, ticket: str, window: int,
                              timeframe: str = Client.KLINE_INTERVAL_1DAY) -> pd.Series:
    """ Получить атр для другого таймфрейма"""
    period_seconds = {
        Client.KLINE_INTERVAL_1DAY: 24 * 60 * 60,
        Client.KLINE_INTERVAL_4HOUR: 4 * 60 * 60,
        Client.KLINE_INTERVAL_1HOUR: 1 * 60 * 60,
        Client.KLINE_INTERVAL_30MINUTE: 30 * 60,
        Client.KLINE_INTERVAL_15MINUTE: 15 * 60
    }[timeframe]
    df_start_date = int(df['close_time'][0] / 1000)
    df_end_date = int(df['close_time'][len(df) - 1] / 1000)
    data = download_data(ticket, df_start_date - (window + 1) * period_seconds, df_end_date, timeframe)
    data['ma'] = sma_indicator(data['close'], window)
    ma_by_days = {int(row['close_time']): row['ma'] for i, row in data.iterrows()}
    del data
    ma_arr = []
    for row in df.itertuples():
        for ts, atr in ma_by_days.copy().items():
            diff = (row.close_time - ts) / 1000
            if diff > period_seconds:
                del ma_by_days[ts]
            else:
                ma_arr.append(atr)
                break
    return pd.Series(ma_arr)


def download_futures_trades(ticket: str, start_date: str = '2020-10-01 00:00:00'):
    """ Скачивание сделок по фьючерсам """
    downloader = _FuturesTradesDownloader(ticket, start_date)
    downloader.download_futures_trades()


class _FuturesTradesDownloader:
    """ Скачивание сделок по фьючерсам """

    TITLES = ['id', 'price', 'volume', 'ts', 'is_long']
    COLUMNS = ['a', 'p', 'q', 'T', 'm']
    MAX_REQ_TO_MIN = 500

    def __init__(self, ticket: str, start_date: str):
        self.client = Client('', '')
        self.ticket = ticket
        self.filename = f'data/{ticket}_trades.csv'
        self.start_ts_ms = int(datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)

    def download_futures_trades(self):

        last_id = self._get_last_id()

        req_to_min = 0
        start_part_ts = 0

        while True:
            if req_to_min > self.MAX_REQ_TO_MIN:
                if datetime.now().timestamp() - start_part_ts < 60:
                    sleep(1)
                    continue
                else:
                    req_to_min = 0
                    start_part_ts = datetime.now().timestamp()

            data = self.client.futures_aggregate_trades(**{
                'symbol': self.ticket,
                'fromId': last_id,
                'limit': 1000
            })
            req_to_min += 1
            if len(data) == 0:
                break
            last_id = self._save_data(data)
            if req_to_min % 3 == 0:
                sleep(0.5)

    def _get_last_id(self):
        if not os.path.isfile(self.filename):
            df = pd.DataFrame([], columns=self.TITLES)
            df.to_csv(self.filename, index=False)
            return self._req_last_id()
        df = pd.read_csv(self.filename)
        if df.shape[0] > 0:
            return df['id'].values[-1]
        return self._req_last_id()

    def _req_last_id(self):
        data = self.client.futures_aggregate_trades(**{
            'symbol': self.ticket,
            'startTime': self.start_ts_ms,
            'limit': 1
        })
        if len(data):
            return data[0]['a']
        return 0

    def _save_data(self, data):
        df = pd.DataFrame(data, columns=self.COLUMNS)
        df.to_csv(self.filename, index=False, header=False, mode='a')
        print("\r ", end="")
        print(datetime.fromtimestamp(df['T'].values[-1] / 1000).strftime('%Y-%m-%d %H:%M:%S').ljust(40), end="")
        return df['a'].values[-1]
