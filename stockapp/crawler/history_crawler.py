#!/usr/bin/env python3
import sys
import os
import argparse
import django
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'StockProject.settings'
from StockProject import settings
django.setup()
from stockapp.models import *
from yahoo_fin.stock_info import get_data
from datetime import datetime, timedelta
import traceback

def get_config():
    parser = argparse.ArgumentParser(description='Historical Stock Data Crawler')
    parser.add_argument('-s', '--standalone', action='store_true',
                        help='Run this script in stadalone mode (loop inside)')
    parser.add_argument('-i', '--interval', type=int, default=24*3600, help='The interval between two crawls in standalone mode (in seconds).')
    parser.add_argument('-d', '--day', type=int, default=1, help='How many days of historical stock data you want to crawl.')
    # Parse args.
    args = parser.parse_args()
    return args

def crawl_historical_data(day):
    print(f'Crawling stock in previous {day} day(s).')
    stocks = Stock.objects.all()
    for stock in stocks:
        try:
            print(f'Crawling stock {stock}')
            now_date = datetime.now().date()
            previous_date = now_date - timedelta(days=day)
            date_format = '%m/%d/%Y'
            stock_historical_data = get_data(stock.symbol.lower(),
                                             start_date=previous_date.strftime(date_format),
                                             end_date=now_date.strftime(date_format),
                                             interval='1d')
            for _, row in stock_historical_data.iterrows():
                date = str(row.name).split(' ')[0]
                his_price_tile = HistoricalPriceTile(
                    stock = stock,
                    date = date,
                    open = row.open,
                    high = row.high,
                    low = row.low,
                    close = row.close,
                    adj_close = row.adjclose,
                    volume = row.volume
                )
                try:
                    his_price_tile.save()
                except django.db.utils.IntegrityError as e:
                    print(e)
        except Exception as e:
            traceback.print_exc()


if __name__ == '__main__':
    args = get_config()
    if args.standalone:
        print('=== Running in standalone mode ===')
        while True:
            crawl_historical_data(args.day)
            print(f'=== Sleeping for {args.interval} seconds ===')
            time.sleep(args.interval)
    else:
        crawl_historical_data(args.day)