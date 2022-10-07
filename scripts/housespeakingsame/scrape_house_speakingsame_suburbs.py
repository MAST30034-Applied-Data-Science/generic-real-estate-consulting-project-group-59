#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

# constants
BASE_URL = "http://house.speakingsame.com/"
TABLE_URLS = {
    # "rent" : "http://house.speakingsame.com/suburbtop.php?sta=vic&cat=RentPrice&name=",
    # "sold" : "http://house.speakingsame.com/suburbtop.php?sta=vic&cat=HomePrice&name=",
    # "turnover" : "http://house.speakingsame.com/suburbtop.php?sta=vic&cat=Housing+Turnover&name=Last+12+months",
    "income" : "http://house.speakingsame.com/suburbtop.php?sta=vic&cat=Median+household+income&name=Weekly+income",
    "occupation" : "http://house.speakingsame.com/suburbtop.php?sta=vic&cat=Occupation&name=Professionals",
    "education" : "http://house.speakingsame.com/suburbtop.php?sta=vic&cat=Education&name=University+or+other+Tertiary+Institution",
    "flats" : "http://house.speakingsame.com/suburbtop.php?sta=vic&cat=Type+of+Dwelling&name=Flat",
    "houses" : "http://house.speakingsame.com/suburbtop.php?sta=vic&cat=Type+of+Dwelling&name=Separate+house",
    "owned" : "http://house.speakingsame.com/suburbtop.php?sta=vic&cat=Nature+of+Occupancy&name=Fully+Owned",
    "rented" : "http://house.speakingsame.com/suburbtop.php?sta=vic&cat=Nature+of+Occupancy&name=Rented",
    "purchased" : "http://house.speakingsame.com/suburbtop.php?sta=vic&cat=Nature+of+Occupancy&name=Purchasing",
}

TAB_COLS = ['rank', 'suburb', 'value', 'link']
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
OUTPUT_DIR = "../../data/raw/housespeakingsame/top/"
TIMEOUT_TEXT = "Please input suburb name, postcode or address"

def get(url, delay=20):
    while True:
        time.sleep(delay)
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            if TIMEOUT_TEXT not in response.text: 
                return response  
            else: print("timed out",end="..")

def parse_row(row_data):
    # Parse byte rank & compile full link
    return [int(''.join(list(row_data[0])[1:])), row_data[1], 
            row_data[2], BASE_URL + row_data[3]]

def get_page(url, page):
    # Retrieves the suburb ranking table of a page
    page_data = []
    bs_obj = BeautifulSoup(get(url + f"&page={page}").content, "html.parser")
    # Find suburbs table & rowdata object
    tab = bs_obj.find("table", {"cellspacing": "0", "cellpadding": "0", "width": "100%", "style": None})
    rows = tab.findAll("tr")
    for row in rows[1:]: # First row is headers
        row_data_ = row.findAll("td")
        row_data = [c.text for c in row_data_] # Unpack rank, suburb, price
        # Append link suffix
        suffix = row_data_[1].find("a")['href']
        row_data += [suffix]
        # Parse row data
        parsed_row_data = parse_row(row_data)
        page_data.append(parsed_row_data)
    return page_data

def get_suburbs(url, verbose=True):
    # Retrieves all pages of the suburbs rankings
    df = pd.DataFrame()
    page = 0
    while True:
        if verbose: print(page, end='..', flush=True)
        page_data = get_page(url, page)
        if len(page_data) == 0: break # Beyond the last page, stop
        page_df = pd.DataFrame(page_data, columns=TAB_COLS)
        page_df['page'] = page
        df = pd.concat([df, page_df])
        page += 1
    return df

def get_all(verbose=True):
    for name, url in TABLE_URLS.items():
        if verbose: print('\n' + name)
        df = get_suburbs(url, verbose)
        df.to_csv(OUTPUT_DIR + name + ".csv", index=False)

# def get_suburb_sales_data(ingredients):
#     # Get "Sales Data" table from suburb profile page    
#     soup = BeautifulSoup(ingredients, "html.parser")
#     # heading = soup.find("table", {"style": "font-size:18px"}) # Suburb Post code & (distnace to CBD link)
#     # sub_pc = heading.find('b').text
#     sales_table = soup.find("table", {"style": "font-size:13px", "cellspacing": 10})
#     
#     table_data = sales_table.findAll("td")
#     assert table_data[0].text == "Sales Data"
#     cell_data = table_data[2:]
#     
#     sales_data = []
#     for i in range(0, len(cell_data), 3):    
#         sales_data.append([cell_data[i].text, cell_data[i+2].text])
#     sales_df = pd.DataFrame(sales_data, columns=['key','value'])
#     return sales_df
# 
# def get_suburbs_sales_data(verbose=True):
#     sales_df = pd.DataFrame()
#     errors = []
#     if verbose: print(len(df['link'].values))
#     for i, link in enumerate(df['link'].values):
#         if verbose: print(i, end='..')
#         try:
#             sub_sales_df = get_suburb_sales_data(get(link).content)
#             sub_sales_df['link'] = link
#             sales_df = pd.concat([sales_df, sub_sales_df])
#         except AttributeError:
#             # No "Sales Data" table
#             errors.append(link)
#     if verbose: print(len(errors), "errors")
#     return sales_df, errors



if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR): os.mkdir(OUTPUT_DIR)
    print("Obtaining Suburb Top Ranks for...")
    df = get_all()
