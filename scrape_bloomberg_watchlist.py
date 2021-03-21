# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 22:53:29 2021

@author: rjlo_
"""

#Scraping Bloomberg Watchlist Data

import pandas as pd
from bs4 import BeautifulSoup as Soup
import requests

# Note: Save the webpage beforehand to prevent having to make calls to the site
#       and to make sure the data needed is captured
#CONTENT = requests.get(enter_filename_here).text

# Open html file
filename = '20210320 Watchlist - Bloomberg - Bloomberg Markets.html'

with open(filename, encoding='utf-8') as f:
    soup = Soup(f, 'html.parser')

# Find table and headers
watchlist = soup.find('div', class_='dataTable__8f870b0b')

watchlist_headers = soup.find_all('div', {'class':'headerName__94318091'})

# Save column names and add column headers for additional info
header_list = [i.text for i in watchlist_headers]

header_list.append('FUND')
header_list.append('TICKER')

# Find rows and save them to a list
df_row_list = []

watchlist_rows = watchlist.find_all('div', class_='row__41b7db30')

# Depending on the row in the watchlist, either save the name and ticker symbol
# or save the actual data
for row in watchlist_rows:
    row_entry = row.find_all('div', class_='lotInformation__e4d47742')
    
    if row_entry == []:
        active_fund = row.find('div', class_='secondaryInformation__bc34d044').text
        ticker_symbol = row.find('a', class_='primaryLink__50c3fb85').text
        #print(active_fund)
        #print(ticker_symbol)
    else:
        row_text = [i.text for i in row_entry]
        row_text.append(active_fund)
        row_text.append(ticker_symbol)
        df_row_list.append(row_text)
        #print(row_text)

# Create DataFrame out of saved data and header names
df = pd.DataFrame(df_row_list, columns = header_list)

# Create copy of the DataFrame for useful columns
reduced_df = df[['SYMBOL','LOTS','PRICE','CHANGE','TOTAL GAIN','1D GAIN','FUND','TICKER']].copy()

# Rename 'SYMBOL' in the original header list to 'DATE'
reduced_df.rename(columns={'SYMBOL':'DATE'}, inplace=True)

# Check DataFrame info
print(reduced_df.info())

# Create a CSV file for further analysis/processing
reduced_df.to_csv('Bloomberg_Watchlist_Data.csv')

