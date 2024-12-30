from datetime import date
import math
##import matplotlib.pyplot as plt 
import pandas as pd
import streamlit as st
import yfinance as yf 


def diff_month(d1, d2):
    """
    Calculate the difference in months between two datetime objects.

    Parameters:
    d1 (datetime): The first date.
    d2 (datetime): The second date.

    Returns:
    int: The difference in months between d1 and d2. Positive if d1 is later than d2, 
         negative if d1 is earlier than d2, and zero if they are in the same month and year.
    """
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def shares_current_value(ticker, num_shares, grant_date, grant_type):
    """
    Calculate the current value and remaining shares of a stock grant based on its type and vesting schedule.

    Parameters:
    ticker (str): The stock ticker symbol.
    num_shares (int): The total number of shares granted.
    grant_date (date): The date the stock grant was issued.
    grant_type (str): The type of stock grant. Either 'RSUs' (Restricted Stock Units) or 'Options'.

    Returns:
    tuple: A tuple containing:
        - num_shares (int): The number of shares currently vested or available.
        - current_value (float): The current value of the vested shares.
    
    Notes:
    - For 'RSUs':
      - Shares vest in quarterly increments over 4 years starting 1 year from the grant date.
    - For 'Options':
      - Shares vest monthly over 48 months starting from the grant date after first year.
      - The current value is calculated as the difference between the current strike price and grant price, 
        multiplied by the number of vested shares, only if the strike price exceeds the grant price.
    - Uses Yahoo Finance to fetch stock prices via the `yfinance` library.
    """
    strike_price_df = yf.download(ticker, start = date.today(), multi_level_index = False)
    strike_price = strike_price_df['Open'].iloc[0]
    if grant_type == 'RSUs':
        if grant_date.replace(year = grant_date.year+1) <= date.today() < grant_date.replace(year = grant_date.year+2):
            num_shares = math.floor(num_shares/4)
        elif date.today() <= grant_date.replace(year = grant_date.year+3):
            num_shares = math.floor(num_shares/2)
        elif date.today() <= grant_date.replace(year = grant_date.year+4):
            num_shares = math.floor(3*num_shares/4)
        elif date.today() >= grant_date.replace(year = grant_date.year+4):
            num_shares = num_shares
        else:
            num_shares = 0
        current_value = num_shares * strike_price
        return num_shares, current_value
    elif grant_type == 'Options':
        grant_price_df =  yf.download(ticker, start = grant_date, multi_level_index = False)
        grant_price = grant_price_df['Open'].iloc[0]
        if diff_month(date.today(), grant_date) >= 48:
            num_shares = num_shares
        elif diff_month(date.today(), grant_date) < 12:
            num_shares = 0
        else:
            num_months = diff_month(date.today(), grant_date)
            num_shares = math.floor(num_months * num_shares/48)
        current_value = strike_price - grant_price
        if current_value > 0:
            current_value = current_value * num_shares
            return num_shares, current_value
        else:
            return num_shares, 0

            
# Title
st.title(":dollar: Stock as Compenstation Evaluator :chart:")
st.write("use to find high points in RSUs and Options when they vest")

# create dataframe to store stock values and write it to the session state
df = pd.DataFrame({'Ticker':[], 'Grant Date':[], 'Num Shares':[], 'Grant Type':[], 'Vested Shares':[], 'Current Value':[]})

if "data" not in st.session_state:
    st.session_state.data = df

# prompt user for stocks and write to data frame    
ticker = st.text_input('Enter Stock Ticker')
grant_date = st.date_input('Stock Grant Date')
num_shares = st.number_input('Enter Number of Shares', 0)
grant_type = st.selectbox('Grant Type', ['RSUs', 'Options'], help="RSUs vest 1/4th on a yearly schedule. Options vest 1/4th on the first year and 1/48th every month following")

if st.button('Add Stock'):
    if ticker and grant_date and num_shares and grant_type:
        vested_shares, current_value = shares_current_value(ticker, num_shares, grant_date, grant_type)
        new_row = pd.Series({'Ticker':ticker, 'Grant Date':grant_date, 'Num Shares':num_shares, 'Grant Type':grant_type, 'Vested Shares': vested_shares, 'Current Value': current_value})
        if len(st.session_state.data) == 0:
            st.session_state.data = new_row.to_frame().T
        else:
            st.session_state.data = pd.concat([st.session_state.data, new_row.to_frame().T], ignore_index= True)
    else:
        st.error("Please fill out all fields!")
    
# loop back until all options added button pressed
#st.button('chart')
# pull up ticker prices
# start_date = datetime(2020, 1, 1) 
#end_date = date.today()

# try:
#     stock_data = yf.download(ticker, start = start_date, 
# 				end = end_date) 
    
#     st.line_chart(stock_data)
# except:
#     st.write('Enter values to seach')
# math 

# chart worth, and number of shares, find best day to have sold

st.write("this is all for funsies")
