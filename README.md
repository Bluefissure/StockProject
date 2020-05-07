# StockProject


[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Bluefissure/StockProject/blob/master/LICENSE)


## Requirements

- MySQL 5.7+
- Python 3.7.5
- [requirements.txt](https://github.com/Bluefissure/StockProject/blob/master/requirements.txt)

## Installation

1. `pip install -r requirements.txt`
1. `mv StockProject/settings_example.py StockProject/settings.py`
1. edit the settings file so that it can connect to the database
1. `python manage.py check`
1. `python manage.py makemigrations`
1. `python manage.py migrate`

## Stock data crawler

Implemented by [yahoo_fin](https://github.com/atreadw1492/yahoo_fin).

Please go into [stockapp/crawler/](https://github.com/Bluefissure/StockProject/tree/master/stockapp/crawler) and
 run `python *_crawler.py -h` for more help.

You can either run cron tasks in Linux/Unix or use the standalone mode to establish a daemon.

## REST API
- Design&manage by [django-rest-framework](https://www.django-rest-framework.org/)
- Documented by [drf-yasg](https://github.com/axnsan12/drf-yasg)

Please read `/swagger/` after running the demo for the details.