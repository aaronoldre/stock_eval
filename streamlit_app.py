from datetime import datetime 
import streamlit as st
import pandas as pd
import yfinance as yf

# Title
st.title(":dollar: Stock as Compenstation Evaluator :chart:")
st.write("use to find high points in RSUs and Options when they vest")

# prompt user for stocks and write to data frame
df = pd.DataFrame({'Ticker', 'Grant Date', 'Num Shares', 'Grant Type', 'Current Value'})
# loop back until all options added button pressed

# pull up ticker prices
start_date = datetime(2020, 1, 1) 
end_date = datetime.today()

stock_data = yf.download('ADPT', start = start_date, 
				end = end_date) 
# math 

# chart worth, and number of shares, find best day to have sold

st.write("this is all for funsies")