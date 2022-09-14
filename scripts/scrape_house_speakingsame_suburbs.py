#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import asyncio
import aiohttp
from datetime import datetime as dt

# constants
BASE_URL = "http://house.speakingsame.com/"
SUBURB_SEARCH_URL = "http://house.speakingsame.com/suburbtop.php?sta=vic&cat=RentPrice&name=&page=%s"
TAB_COLS = ['rank', 'suburb', 'value', 'link']
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

def get(url):
    while True:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200: 
            return response  

def parse_row(row_data):
    # Parse byte rank & compile full link
    return [int(''.join(list(row_data[0])[1:])), row_data[1], 
            row_data[2], BASE_URL + row_data[3]]

def get_page(page):
    # Retrieves the suburb ranking table of a page
    page_data = []
    bs_obj = BeautifulSoup(get(SUBURB_SEARCH_URL % page).content, "html.parser")
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

def get_suburbs(verbose=True):
    # Retrieves all pages of the suburbs rankings
    df = pd.DataFrame()
    page = 0
    while True:
        if verbose: print(page, end='..', flush=True)
        page_data = get_page(page)
        if len(page_data) == 0: break # Beyond the last page, stop
        page_df = pd.DataFrame(page_data, columns=TAB_COLS)
        page_df['page'] = page
        df = pd.concat([df, page_df])
        page += 1
    return df

def get_suburb_sales_data(ingredients):
    # Get "Sales Data" table from suburb profile page    
    soup = BeautifulSoup(ingredients, "html.parser")
    heading = soup.find("table", {"style": "font-size:18px"}) # Suburb Post code & (distnace to CBD link)
    sub_pc = heading.find('b').text
    sales_table = soup.find("table", {"style": "font-size:13px", "cellspacing": 10})
    
    table_data = sales_table.findAll("td")
    assert table_data[0].text == "Sales Data"
    cell_data = table_data[2:]
    
    sales_data = []
    for i in range(0, len(cell_data), 3):    
        sales_data.append([cell_data[i].text, cell_data[i+2].text])
    sales_df = pd.DataFrame(sales_data, columns=['key','value'])
    return sales_df

def get_suburbs_sales_data(verbose=True):
    sales_df = pd.DataFrame()
    errors = []
    if verbose: print(len(df['link'].values))
    for i, link in enumerate(df['link'].values):
        if verbose: print(i, end='..')
        try:
            sub_sales_df = get_suburb_sales_data(get(link).content)
            sub_sales_df['link'] = link
            sales_df = pd.concat([sales_df, sub_sales_df])
        except AttributeError:
            # No "Sales Data" table
            errors.append(link)
    if verbose: print(len(errors), "errors")
    return sales_df, errors

async def async_get(client, url):
    async with client.get(url) as response:
        assert response.status == 200        
        return await response.read(), url

async def async_get_links_(client, links):
    resps = await asyncio.wait([async_get(client, link) for link in links])
    return resps

def async_get_links(links):
    loop = asyncio.get_event_loop()
    client = aiohttp.ClientSession(loop=loop)
    resps = loop.run_until_complete(async_get_links_(client, links))
    loop.close()
    return resps

def async_get_suburbs_sales_data(verbose=True):
    resps_ = async_get_links(df['link'].values)
    resps = [x.result() for x in list(list(resps_)[0])]
    sales_df = pd.DataFrame()
    errors = []
    for i, (resp, link) in enumerate(resps):
        try:
            print(i, end='..', flush=True)
            sub_sales_df = get_suburb_sales_data(resp)
            sub_sales_df['link'] = link
            sales_df = pd.concat([sales_df, sub_sales_df])
        except AttributeError:
            # No "Sales Data" table
            errors.append(link)
    if verbose: print(len(errors), "errors")
    return sales_df, errors


if __name__ == "__main__":
    df = get_suburbs()
    df.to_csv(f'../data/raw/top_rent_suburbs_{dt.now().isoformat()}.csv', index=False)
    # resps_ = async_get_links(df['link'].values[:5])
    # resps = [x.result() for x in list(list(resps_)[0])]
    # sales_df, errors = async_get_suburbs_sales_data()