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

def get_config():
    parser = argparse.ArgumentParser(description='Historical Stock Data Crawler')
    parser.add_argument('-s', '--standalone', action='store_true',
                        help='Run this script in stadalone mode (loop inside)')
    parser.add_argument('-i', '--interval', default=24*3600, help='The interval between two crawls in standalone mode.')
    parser.add_argument('-d', '--day', default=365, help='How many days of historical stock data you want to crawl.')
    # Parse args.
    args = parser.parse_args()
    return args

def crawl_historical_data(day):
    print(f'Crawling stock in previous {day} day(s).')
    stocks = Stock.objects.all()
    for stock in stocks:
        print(f'Crawling stock {stock}')

if __name__ == '__main__':
    args = get_config()
    if args.standalone:
        while True:
            crawl_historical_data(args.day)
            time.sleep(args.interval)
    else:
        crawl_historical_data(args.day)