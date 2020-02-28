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

