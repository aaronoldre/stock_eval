from datetime import datetime 
import streamlit as st
import pandas as pd
##import yfinance as yf

# Title
st.title(":dollar: Stock as Compenstation Evaluator :chart:")
st.write("use to find high points in RSUs and Options when they vest")

# prompt user for stocks and write to data frame
df = pd.DataFrame({'Ticker':[], 'Grant Date':[], 'Num Shares':[], 'Grant Type':[], 'Current Value':[]})

if not df.empty:
    st.dataframe(df)

    
ticker = st.text_input('Enter Stock Ticker')
start_date = st.date_input('Stock Grant Date')
num_shares = st.number_input('Enter Number of Shares', 0)
grant_type = st.selectbox('Grant Type', ['RSUs', 'Options'], help="RSUs vest 1/4th on a yearly schedule. Options vest 1/4th on the first year and 1/48th every month following")
new_row = {'Ticker':ticker, 'Grant Date':start_date, 'Num Shares':num_shares, 'Grant Type':grant_type}
if st.button('Add Stock'):
    
    df_new = df._append(new_row, ignore_index=True)
    st.write('second time')
    st.dataframe(df)
# loop back until all options added button pressed

# pull up ticker prices
# start_date = datetime(2020, 1, 1) 
end_date = datetime.today()

# try:
#     stock_data = yf.download(ticker, start = start_date, 
# 				end = end_date) 
    
#     st.line_chart(stock_data)
# except:
#     st.write('Enter values to seach')
# math 

# chart worth, and number of shares, find best day to have sold

st.write("this is all for funsies")