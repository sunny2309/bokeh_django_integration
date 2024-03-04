from django.shortcuts import render, redirect
import yfinance as yf
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components

tickers = ["AAPL", "NVDA", "GOOGL", "MSFT", "BAC", "META", "AMZN",
            "NFLX", "ADBE", "TSLA", "JPM", "CRM", "CSCO", "NKE", "QCOM"]
names = ['Apple Inc.', 'NVIDIA Corporation', 'Alphabet Inc.', 'Microsoft Corporation',
 'Bank of America Corporation', 'Meta Platforms, Inc.', 'Amazon.com, Inc.',
 'Netflix, Inc.', 'Adobe Inc.', 'Tesla, Inc.', 'JPMorgan Chase & Co.',
 'Salesforce, Inc.', 'Cisco Systems, Inc.', 'NIKE, Inc.', 'QUALCOMM Incorporated']

def index(request):
    return redirect("stock/AAPL")

def retrieve_stock_data(ticker):
    ticker_obj = yf.Ticker(ticker)    
    ticker_info = ticker_obj.info
    ## Historical Data
    hist_df = ticker_obj.history(period="3mo")
    hist_df = hist_df.reset_index()
    
    return hist_df, ticker_info

def create_candlestick_chart(hist_df):
    inc = hist_df.Close > hist_df.Open ## Green Bars
    dec = hist_df.Open > hist_df.Close ## Red Bars

    w = 12*60*60*1300
    fig = figure(x_axis_type="datetime", sizing_mode="stretch_width",
                 tooltips=[('Open', '@Open'), ('High', '@High'),
                            ('Low', '@Low'),  ('Close', '@Close')],
                  height=480)

    fig.segment("Date", "High", "Date", "Low", color="black", source=hist_df)
    fig.vbar("Date", w, "Open", "Close", source=hist_df[inc], color="lawngreen")
    fig.vbar("Date", w, "Open", "Close", source=hist_df[dec], color="tomato")

    fig.xaxis.axis_label="Date"
    fig.yaxis.axis_label="Price ($)"
    return fig

def display_ticker(request, ticker):
    hist_df, info = retrieve_stock_data(ticker)
    p1, p2 = hist_df["Close"].values[-1], hist_df["Close"].values[-2]
    change, prcnt_change = (p2-p1), (p2-p1) / p1

    candlestick_fig = create_candlestick_chart(hist_df)
    scripts, chart_div = components(candlestick_fig)
    #html = file_html(fig, CDN, "Candlestick Chart")
    context = {
        "tickers": zip(tickers, names),
        "ticker": ticker,
        "scripts": scripts,
        "hist_chart_div": chart_div,
        "name": info["longName"],
        "industry": info["industry"],
        "sector": info["sector"],
        "summary": info["longBusinessSummary"],
        "close": f"{p1: .2f} USD",
        "change": f"{change:.2f}",
        "pct_change": f"{prcnt_change*100:.2f}%"
    }
    return render(request, "stock_dashboard/ticker_display.html", context)

