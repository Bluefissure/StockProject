#!/usr/bin/env python3
import sys
import os
import argparse
import django
import ta
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'StockProject.settings'
from StockProject import settings
django.setup()
from stockapp.models import *
from yahoo_fin.stock_info import get_data
from datetime import datetime, timedelta
import traceback
from decimal import Decimal

def get_config():
    parser = argparse.ArgumentParser(description='Historical Stock Data Crawler')
    parser.add_argument('-s', '--symbol', type=str,
                        help='The stock symbol for calculating indicators.')
    # Parse args.
    args = parser.parse_args()
    return args

def calc_indicator(stock):
    hs = stock.historical_price.all()
    df = pd.DataFrame(columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
    for i, h in enumerate(hs):
        df.at[i, 'Timestamp'] = datetime.strptime(str(h.date), '%Y-%m-%d').timestamp()
        df.at[i, 'Open'] = float(h.open)
        df.at[i, 'High'] = float(h.high)
        df.at[i, 'Low'] = float(h.low)
        df.at[i, 'Close'] = float(h.close)
        df.at[i, 'Volume'] = float(h.volume)

    adx = ta.trend.ADXIndicator(high=df["High"], low=df["Low"], close=df["Close"], fillna=True)
    # print(adx.adx())

    macd = ta.trend.MACD(close=df["Close"], fillna=True)
    # print(macd.macd())

    vi = ta.trend.VortexIndicator(high=df["High"], low=df["Low"], close=df["Close"], fillna=True)
    # print(vi.vortex_indicator_pos())
    # print(vi.vortex_indicator_neg())

    for i, (h, adx) in enumerate(zip(hs, adx.adx())):
        indicator, _ = Indicator.objects.get_or_create(name="ADX", price=h)
        indicator.value = adx
        indicator.save()

    for i, (h, macd) in enumerate(zip(hs, macd.macd())):
        indicator, _ = Indicator.objects.get_or_create(name="MACD", price=h)
        indicator.value = macd
        indicator.save()

    for i, (h, pos, neg) in enumerate(zip(hs, vi.vortex_indicator_pos(), vi.vortex_indicator_neg())):
        indicator, _ = Indicator.objects.get_or_create(name="+VI", price=h)
        indicator.value = pos
        indicator.save()
        indicator, _ = Indicator.objects.get_or_create(name="-VI", price=h)
        indicator.value = neg
        indicator.save()

if __name__ == '__main__':
    args = get_config()
    if not args.symbol:
        for stock in Stock.objects.all():
            print("Calculating indicators in {}......".format(stock))
            calc_indicator(stock)
    else:
        stock = Stock.objects.get(symbol=args.symbol)
        calc_indicator(stock)

