import logging
import os

import requests
import json
import traceback

from model import SpotTrade, Quote, SpotOrder, SpotView, MetaData, Portfolio
from service import CustomFormatter

from datetime import datetime, timedelta

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter.CustomFormatter())

log.addHandler(ch)

coin_marketcap_host = "https://pro-api.coinmarketcap.com"
api_key = "ecc1d428-d19e-4d84-8f61-2f7f612b3ec4"
coin_market_timeout = 60

#saganavis_api_host = "https://api.saganavis.xyz"
saganavis_api_host = "http://api.saganavis.co.in"
trade_path = "/v1/rates/spotTrade/portfolio/{portfolioName}"
portfolio_path = '/v1/rates/portfolio/{portfolioName}'
spot_trade_get_path = "/v1/rates/spotTrade/{spotId}"
spot_trade_post_path = "/v1/rates/spotTrade"
saganavis_api_timeout = 50
all_trade_path = "/v1/rates/tradeLatest/{portfolioName}"

def parse_trades(response):
    trades = []
    items = json.loads(response.content)
    for x in items:
        info = SpotTrade.SpotTrade(x['id'], x['cid'], x['symbol'], x['buyPrice'], x['qty'], x['imgUrl'], x['portfolioId'])
        trades.append(info)
    return trades

def get_all_spot_trades(portfolio_name):
    trades = []
    try:
        trade_api = saganavis_api_host + trade_path
        #log.info(trade_api)
        # Define the path parameter
        path_params = {"portfolioName": portfolio_name}

        # Format the URL with the path parameter
        formatted_url = trade_api.format(**path_params)
        log.info(formatted_url)

        response = requests.get(formatted_url, timeout=saganavis_api_timeout)
        #log.info (response)
        #log.info(response.status_code)
        if response.status_code == 200:
            #log.info(response)
            trades = parse_trades(response)
            #log.info (len(trades))
        response.close()
        return trades
    except Exception as ex:
        log.error(f"Error connecting stock trade uri: {ex}")


def delete_spot_trade(spot_id):
    try:
        headers = {"Content-Type": "application/json"}
        spot_trade_delete_api = saganavis_api_host + spot_trade_get_path
        path_params = {"spotId": spot_id}

        # Format the URL with the path parameter
        formatted_url = spot_trade_delete_api.format(**path_params)
        print("Delete API: ", formatted_url)

        response = requests.delete(formatted_url, headers=headers)
        print("Response code:", response.status_code)

        if response.status_code == 200:
            print("Item deleted successfully!")
        else:
            print("Failed to create post:", response.status_code)

    except Exception as ex:
        log.error(f"Error save connecting stock trade uri: {ex}")

def save_spot_trade(spot_trade):
    try:
        headers = {"Content-Type": "application/json"}

        # Data to be sent as JSON (Python dictionary)
        json_spot_trade = {
            "id": spot_trade.id,
            "cid": spot_trade.coin_marketcap_id,
            "symbol": spot_trade.symbol,
            "buyPrice": str(spot_trade.buy_price),  # or use a float if needed
            "qty": str(spot_trade.quantity),
            "portfolioId": spot_trade.portfolioId,
            "updatePrice": spot_trade.updatePrice
        }

        log.info(json_spot_trade)
        spot_trade_post_api = saganavis_api_host + spot_trade_post_path
        log.info(spot_trade_post_api)
        response = requests.post(spot_trade_post_api, json=json_spot_trade, headers=headers)
        print("Response Text:", response.text)

        if response.status_code == 200:
            print("Post created successfully!")
            print("Response JSON:", response.json())
        else:
            print("Failed to create post:", response.status_code)
    except Exception as ex:
        log.error(f"Error save connecting stock trade uri: {ex}")

def parse_portfolio(response):
    #log.info(response.content)
    x = json.loads(response.content)
    # log.info(x)
    return Portfolio.Portfolio(x['id'], x['name'], x['logo'])


def get_portfolio(portfolio_name):
    portfolio = None
    try:
        portfolio_api = saganavis_api_host + portfolio_path
        #log.info(portfolio_api)
        # Define the path parameter
        path_params = {"portfolioName": portfolio_name}

        # Format the URL with the path parameter
        formatted_url = portfolio_api.format(**path_params)
        log.info(formatted_url)

        response = requests.get(formatted_url, timeout=saganavis_api_timeout)
        #log.info (response)
        #log.info(response.status_code)
        if response.status_code == 200:
            #log.info(response)
            portfolio = parse_portfolio(response)
            #log.info (len(trades))
        response.close()
        return portfolio
    except Exception as ex:
        log.error(f"Error connecting portfolio uri: regx{ex}")
        print(print(traceback.format_exc()))

def parse_rates(response, coin_market_ids):
    x = json.loads(response.content)
    #log.info (x)
    quotes = []
    for cid in coin_market_ids:
        coin_id = str(cid)
        coins = x['data'][coin_id]
        quote = coins['quote']['USDT']
        last_updated = datetime.fromisoformat(quote['last_updated'][:-1])
        delta = timedelta(hours=5, minutes=30)
        new_datetime = last_updated + delta
        info = Quote.Quote(coins['id'], coins['symbol'], coins['name'], quote['price'], new_datetime)
        quotes.append(info)

    return quotes


def get_crypto_rates(coin_market_ids):
    quotes = []
    try:
        ids = ','.join(map(str, coin_market_ids))
        #log.info(ids)
        uri = str(f"{coin_marketcap_host}/v2/cryptocurrency/quotes/latest?id={ids}&convert=USDT")
        log.info (uri)
        headers = {"X-CMC_PRO_API_KEY": api_key}
        #log.info (headers)
        response = requests.get(uri, headers=headers, timeout=coin_market_timeout)
        #log.info (response)
        #log.info(response.status_code)
        if response.status_code == 200:
            #log.info(response)
            quotes = parse_rates(response, coin_market_ids)
            #log.info (len(quotes))
        response.close()
        return quotes
    except Exception as ex:
        log.error(f"Error connecting coin market cap: {ex}")


def parse_meta_data(response, cid):
    x = json.loads(response.content)
    #log.info (x)

    coin_id = str(cid)
    coins = x['data'][coin_id]
    platform = coins['platform']
    platform_id = platform['id'] if platform else ''
    platform_name = platform['name'] if platform else ''

    info = MetaData.MetaData(coins['id'], coins['name'], coins['symbol'], coins['category'], coins['description'], coins['logo'], platform_id, platform_name)
    return info


def get_meta_data(cid):
    meta = None
    try:
        uri = str(f"{coin_marketcap_host}/v2/cryptocurrency/info?id={cid}")
        log.info(uri)
        headers = {"X-CMC_PRO_API_KEY": api_key}
        response = requests.get(uri, headers=headers, timeout=coin_market_timeout)
        if response.status_code == 200:
            meta = parse_meta_data(response, cid)
        response.close()
        return meta
    except Exception as ex:
        log.error(f"Error connecting CMC meta data api: {ex}")

def get_spot_view(portfolio_name):
    spot_orders = get_all_spot_orders(portfolio_name)
    if len(spot_orders) > 0:
        return SpotView.SpotView(spot_orders)
    else:
        return None

def get_all_spot_orders(portfolio_name):
    spot_orders = []
    spot_trades = get_all_spot_trades(portfolio_name)
    if len(spot_trades) > 0:
        coin_market_ids = [trade.coin_marketcap_id for trade in spot_trades]
        quotes = get_crypto_rates(coin_market_ids)

        for spot in spot_trades:
            for quote in quotes:
                if spot.coin_marketcap_id == quote.cid:
                    spot_order_info = SpotOrder.SpotOrder(spot.id, spot.coin_marketcap_id, spot.symbol, quote.name, spot.logo, quote.price, spot.buy_price, spot.quantity, quote.last_updated)
                    #log.info (spot_order_info)
                    spot_orders.append(spot_order_info)

    return spot_orders


def parse_spot_trade(response):
    x = json.loads(response.content)
    # log.info(x)
    return SpotTrade.SpotTrade(x['id'], x['cid'], x['symbol'], x['buyPrice'], x['qty'], x['imgUrl'], x['portfolioId'])


def get_spot_trade(spot_id):
    spot_trade = None
    try:
        get_spot_api = saganavis_api_host + spot_trade_get_path
        path_params = {"spotId": spot_id}

        # Format the URL with the path parameter
        formatted_url = get_spot_api.format(**path_params)
        log.info(formatted_url)

        response = requests.get(formatted_url, timeout=saganavis_api_timeout)
        if response.status_code == 200:
            spot_trade = parse_spot_trade(response)
        response.close()
        return spot_trade
    except Exception as ex:
        log.error(f"Error connecting get spot trade uri: regx{ex}")
        print(print(traceback.format_exc()))


if __name__ == "__main__":
    log.info("MAIN started")
    #print (os.urandom(24).hex())
    #spot_view = get_spot_view("Abdul")
    #if spot_view:
         #s = sorted(spot_view.spot_orders, key=lambda x: x.pnl, reverse=True)
         #for spot_order in s:
             #log.info(spot_order)
    #log.info(get_meta_data(1361))


