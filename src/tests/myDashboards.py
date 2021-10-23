import streamlit as st
import pandas as pd
import numpy as np
import requests
import tweepy
import config
import psycopg2, psycopg2.extras
import plotly.graph_objects as go
from binance.client import Client
import degiroapi
from degiroapi.product import Product
from degiroapi.order import Order
from degiroapi.utils import pretty_json

import yfinance as yf

from datetime import date
from datetime import timedelta





def test_crypto():
    client = Client(config.Clave_Api_Binance_publica, config.Clave_Api_Binance_secreta)

    klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1DAY, "1 day ago UTC")
    st.write(klines)
    today = date.today()
    yesterday = date.today() - timedelta(days=1)
    lastWeek = date.today() - timedelta(days=7)
    last2Weeks = date.today() - timedelta(days=14)
    lastMonth = date.today() - timedelta(days=30)

    st.write("""
    # Simple Stock Price App
    Shown are the stock closing price and volume of Google!
    """)

    # https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
    # define the ticker symbol
    tickerSymbol = 'CGC'
    # get data on this ticker
    tickerData = yf.Ticker(tickerSymbol)
    st.write(yesterday.strftime("%Y-%m-%d"))

    # get the historical prices for this ticker
    tickerDf = tickerData.history(period='1d', start=lastMonth, end=today)
    st.write(tickerDf.index)
    st.write(tickerDf)
    openPrices = tickerDf["Open"]
    st.write("El precio de ayer es= ", openPrices.loc[yesterday.strftime("%Y-%m-%d")])

    # Open	High	Low	Close	Volume	Dividends	Stock Splits

    st.line_chart(tickerDf.Close)
    st.line_chart(tickerDf.Volume)

    # balBTC = get_asset_balance("BTC")

    st.title("Binance")
    info = client.get_account()

    bal = info['balances']
    for i in bal:
        if float(i['free']) > 0:
            st.write('Symbol: ', i['asset'], '- Amount: ', i['free'])


def test_stock():
    degiro = degiroapi.DeGiro()
    degiro.login("", "")
    portfolio = degiro.getdata(degiroapi.Data.Type.PORTFOLIO, True)
    st.title("Bienvenido a tu dashboard!")
    st.title("Degiro")
    for data in portfolio:
        asset = degiro.product_info(data['id'])
        st.write(asset["name"])
        st.write("Cantidad: ", data["size"], " x ", data["price"], asset["currency"], " = ", data["value"])



test_crypto()
test_stock()
