import datetime
import json

from colorama import *
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


def get_coins_currencies_list():
    coin_url = 'https://web-api.coinmarketcap.com/v1/cryptocurrency/map'
    fiat_url = 'https://web-api.coinmarketcap.com/v1/fiat/map'
    headers = {'Accepts': 'application/json'}
    session = Session()
    session.headers.update(headers)

    try:
        response_coin = session.get(coin_url)
        coin_cache = json.loads(response_coin.text)
        response_fiat = session.get(fiat_url)
        fiat_cache = json.loads(response_fiat.text)

    except (ConnectionError, Timeout, TooManyRedirects) as exception:
        print(exception)

    coin_list = ''
    fiat_list = ''

    for i, v in enumerate(zip(coin_cache["data"], fiat_cache["data"])):
        coin_list += str(f"{coin_cache['data'][i]['name']} {coin_cache['data'][i]['symbol']} \n")
        fiat_list += str(f"{fiat_cache['data'][i]['name']} {fiat_cache['data'][i]['symbol']} \n")

    return coin_list, fiat_list


# API requires start date & end datetime objects
def get_historical_url(fiat, coin, start_date='', end_date=''):
    # Set end_date to one day past start_date
    if start_date != '' and end_date == '':
        date_obj = datetime.datetime.strptime(start_date, '%d-%m-%Y')
        end_date = date_obj + datetime.timedelta(days=1)
        end_date = end_date.strftime('%d-%m-%Y')

    # default start date for Coinmarketcap API but too early for most coins, will return lots of empty price caches
    if start_date == '':
        start_date = '28-4-2013'

    if end_date == '':
        yesterday = datetime.date.today() - datetime.timedelta(1)
        end_date = yesterday.strftime('%d-%m-%Y')

    # convert dates to format required by API url
    start_date = int((datetime.datetime.strptime(start_date, '%d-%m-%Y')).timestamp())
    end_date = int(datetime.datetime.strptime(end_date, '%d-%m-%Y').timestamp())

    historical_url = f"https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?convert={fiat}" \
                     f"&symbol={coin}&time_end={end_date}&time_start={start_date}"

    return historical_url, start_date, end_date


def get_historical_price_cache(fiat, coin, start_date='', end_date=''):
    historical_url, start_date, end_date = get_historical_url(fiat, coin, start_date, end_date)
    headers = {'Accepts': 'application/json'}
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(historical_url)
        coin_cache = json.loads(response.text)

        return coin_cache, start_date, end_date

    except (ConnectionError, Timeout, TooManyRedirects) as exception:
        print(exception)


def get_todays_price_cache(url='https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/latest', fiat='EUR'):
    fiat = {'convert': fiat}
    headers = {'Accepts': 'application/json'}
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=fiat)
        converter_cache = json.loads(response.text)
        return converter_cache

    except (ConnectionError, Timeout, TooManyRedirects) as exception:
        print(exception)
