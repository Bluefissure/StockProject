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
from yahoo_fin.stock_info import get_live_price, get_quote_table
from django.utils import timezone
import traceback

def get_config():
    parser = argparse.ArgumentParser(description='Live Stock Price Crawler')
    parser.add_argument('-s', '--standalone', action='store_true',
                        help='Run this script in stadalone mode (loop inside)')
    parser.add_argument('-i', '--interval', type=int, default=60, help='The interval between two crawls in standalone mode (in seconds).')
    # Parse args.
    args = parser.parse_args()
    return args

def crawl_live_price():
    print('Crawling stock live price.')
    stocks = Stock.objects.all()
    for stock in stocks:
        try:
            now_time = timezone.now()
            time_format = '%Y-%m-%d %H:%M:%S'
            print(f'Crawling stock {stock} at {now_time.strftime(time_format)}')
            live_data= get_quote_table(stock.symbol.lower())
            live_price_tile = LivePriceTile(
                stock = stock,
                time = now_time,
                price = live_data['Quote Price'],
                volume = live_data['Volume']
            )
            try:
                live_price_tile.save()
            except django.db.utils.IntegrityError as e:
                print(e)
            except:
                traceback.print_exc()
        except:
            traceback.print_exc()


if __name__ == '__main__':
    args = get_config()
    if args.standalone:
        print('=== Running in standalone mode ===')
        while True:
            crawl_live_price()
            print(f'=== Sleeping for {args.interval} seconds ===')
            time.sleep(args.interval)
    else:
        crawl_live_price()