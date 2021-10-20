import streamlit as st
import yfinance as yf
import json as js
import sqlite3
import datetime
import pandas as pd
from datetime import date
from datetime import timedelta

yesterday = date.today() - timedelta(days=1)
def ticker_to_json(tic):

    today = date.today()

    lastWeek = date.today() - timedelta(days=7)
    last2Weeks = date.today() - timedelta(days=14)
    lastMonth = date.today() - timedelta(days=30)

    # get data on this ticker
    tickerData = yf.Ticker(tic)
    st.write(yesterday.strftime("%Y-%m-%d"))
    ticketMSFT = str(yf.Ticker(tic).info).replace("\'", "\"").replace("False","\"FALSE\"").replace("None","\"NULL\"")
    #st.write(ticketMSFT)
    return js.loads(ticketMSFT)
   # st.write("Json info parsed")
    #st.write(js.loads(ticketMSFT))


def create_db():
    try:
        conn = sqlite3.connect('cryptodata.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE cripto_prices (
                    symbol text,
                    Date text,
                    open real,
                    previousClose real,
                    toCurrency text,
                    circulatingSupply real,
                    marketCap real)""")
        c.execute("""CREATE TABLE cripto_info (
                    symbol text,
                    name text,
                    day text,
                    description text,
                    shortName text,
                    quoteType text,
                    startDate text)""")
        conn.commit()
        conn.close()
    except:
        print("The Datase already exist")

def insert_ticker_data(tic):
    jsontic = ticker_to_json(tic)
    st.write(jsontic)
    startday = datetime.datetime.fromtimestamp(jsontic['startDate']).strftime("%Y-%m-%d")
    yesterdayDate = yesterday.strftime("%Y-%m-%d")

    conn = sqlite3.connect('cryptodata.db')
    c = conn.cursor()

    query = c.execute("SELECT * FROM cripto_prices WHERE symbol = \"{}\" AND Date = \"{}\"".format(jsontic['symbol'],yesterdayDate))
    cols = [column[0] for column in query.description]
    result=pd.DataFrame.from_records(data = query.fetchall(), columns=cols)

    if len(result.values) == 0:
        print("Elemento nuevo")
        insert = "INSERT INTO cripto_prices VALUES (\"{}\", \"{}\", {}, {}, \"{}\", {}, {})" \
            .format(jsontic['symbol'],yesterdayDate,jsontic['open'],jsontic['previousClose'],jsontic['toCurrency'],jsontic['circulatingSupply'],jsontic['marketCap'])
        c.execute(insert)
    else:
        print("El elemento existe")


    conn.commit()
    conn.close()

def show_data_table():

    conn = sqlite3.connect('cryptodata.db')
    c = conn.cursor()

    query = c.execute("SELECT * FROM cripto_prices")
    cols = [column[0] for column in query.description]
    result=pd.DataFrame.from_records(data = query.fetchall(), columns=cols)



    st.dataframe(result)
    conn.commit()
    conn.close()



create_db()
show_data_table()
tic = 'BTC-USD'
insert_ticker_data(tic)