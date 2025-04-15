import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
from st_click_detector import click_detector
from datetime import datetime

# Ideas for improvement:
# 1. Add more stock tickers to the list.  #E #?Nikos
# 2. Allow users to input a custom date range for the stock data. #E #?Philip
# 3. Allow users to provide their own tickers, with error handling for tickers not in the S&P500. (Remove the ability to click on the icons) #M #? Nikos
# 4. Show information about the stock (e.g., market cap, P/E ratio) alongside the chart. #M #? Philip
# 5. Investment portfolio tracker: Allow users to input multiple stocks and return their portfolio's current worth. #H #?Niks
# 6. Add a news section to show the latest news related to the selected stock (you can use the news attribute of yfinance.Ticker). #H #?Philip

# Create the images as a href elements with tickers as IDs
import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
from st_click_detector import click_detector
from datetime import datetime

# Create the images as a href elements with tickers as IDs
def show_tickers():
    content = """
        <a href='#' id='MSFT'><img height='60px' width='60px' src='https://banner2.cleanpng.com/20180609/jq/aa8dbj2or.webp'></a>
        <a href='#' id='AAPL'><img height='60px' width='60px' src='https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg'></a>
    """
    return content

# Make the images clickable using st_click_detector
def get_ticker():
    content = show_tickers()
    clicked = click_detector(content)
    return clicked

# Get the stock dataframe for the given ticker using yfinance
def get_dataframe(ticker):
    stock_data = yf.Ticker(ticker)
    df = stock_data.history(period="1y")
    df.reset_index(inplace=True)
    return df

# Create a candlestick chart using plotly
def plot_candlestick(df, ticker):
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])
    fig.update_layout(title=f'{ticker} Stock Price', xaxis_title='Date', yaxis_title='Price (USD)')
    return fig

# Show a plotly chart in Streamlit
def show_plot(fig):
    st.plotly_chart(fig, use_container_width=True)

# Fetch and display the stock data for the selected date range
def get_dataframe_with_dates(ticker, start_date, end_date):
    stock_data = yf.Ticker(ticker)
    df = stock_data.history(start=start_date, end=end_date)
    df.reset_index(inplace=True)
    return df

# Fetch and display basic stock information
def show_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    # Extract key info safely
    market_cap = info.get("marketCap", "N/A")
    pe_ratio = info.get("trailingPE", "N/A")
    name = info.get("shortName", ticker)
    sector = info.get("sector", "N/A")
    industry = info.get("industry", "N/A")

    st.subheader(f"{name} - Overview")
    st.markdown(f"""
        - **Sector:** {sector}  
        - **Industry:** {industry}  
        - **Market Cap:** {market_cap:,}  
        - **P/E Ratio:** {pe_ratio}  
    """)

# Main Streamlit app
ticker = get_ticker()

if ticker != "":
    current_year = datetime.now().year
    start_date_default = datetime(current_year, 1, 1)
    end_date_default = datetime(current_year, 12, 31)

    st.subheader("Select Date")
    start_date = st.date_input("Start Date", value=start_date_default)
    end_date = st.date_input("End Date", value=end_date_default)

    if start_date >= end_date:
        st.error("End date must be after the start date.")
    else:
        df = get_dataframe_with_dates(ticker, start_date, end_date)
        fig = plot_candlestick(df, ticker)

        show_plot(fig)         
        show_stock_info(ticker)  