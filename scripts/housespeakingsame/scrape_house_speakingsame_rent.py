#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import asyncio
import aiohttp
from datetime import datetime as dt
from glob import glob
import re
import time
import os

# constants
BASE_URL = "http://house.speakingsame.com/"
SEARCH_URL = "http://house.speakingsame.com/rp.php?q={}%2C+VIC&p={}"

OUTPUT_DIR = "../data/raw/housespeakingsame/rent/"


HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

# Suburb rent value rankings
suburbs = pd.read_csv(sorted(glob("../data/raw/top_rent_suburbs_*.csv"))[-1])

PROXIES_URL = 'https://free-proxy-list.net/'
proxies_response = requests.get("https://apiproxyfree.com/proxyapi")#"?country=AU")
proxy_list = proxies_response.json()
all_proxies = [{"http": "http://{}:{}".format(p['ip'].strip(), p['portPreferred'].strip())} for p in proxy_list]
proxies = [None]

# # Find working proxies
# for i, prox in enumerate(all_proxies[:50]):
#     print(end='.')
#     try:
#         for k in range(3): requests.get(prox['http'], timeout=1)
#         proxies.append(prox)
#     except:continue
#     print(i,end='..',flush=True)


def get(url, delay=10, timeout=180):
    """
    GET request to property search pages with error/timeout handling
    """
    time.sleep(delay)
    while True:
        for i, proxy in enumerate(proxies):
            try:
                # print(proxy, end='..', flush=True)
                print(end='.', flush=True)
                response = requests.get(url, headers=HEADERS, timeout=2) if not proxy else\
                    requests.get(url, headers=HEADERS, proxies=proxy, timeout=2)
            # except requests.exceptions.ProxyError or requests.exceptions.ConnectTimeout: continue
            except: continue
            if response.status_code == 200 and \
                not "/img/pleasewait.jpg" in response.text and\
                    "The property data is from the auction results and realestate websites." in response.text: 
                proxies.insert(0, proxies.pop(i))
                return response
        print(end='|')
        time.sleep(timeout)
        requests.get(BASE_URL)

def get_suburb_page(suburb, page):
    """
    Retrieve all properties from the given suburb and search page
    """
    response = get(SEARCH_URL.format(suburb.replace(' ', '+'), page))
    soup = BeautifulSoup(response.content, "html.parser")
    df = get_page_properties(soup)
    return response, soup, df

def get_page_properties(soup):
    """
    Extracts rent & sold price & date & whether it was an auction
    """
    properties = soup.find("div", id="setFilter").parent.findAll(
        "table", {"width": "100%", "cellspacing": 0, "cellpadding": 0})
    if len(properties) == 0: return # Last page, no data
    
    dfs = []
    for p in properties:
        d = dict()
        link_suffix = p.a['href']
        d['link'] = BASE_URL + link_suffix
        d['address'] = p.a.text
        # row_data = [td for td in p.table.findAll('td')]
        
        rent = p.find("b", string=[re.compile("Rent")])
        if rent: 
            rent = rent.parent.text
            d['rent_price'] = rent.split(' in ')[0].replace('Rent ', '')
            d['rent_date'] = rent.split(' in ')[1]

        type_rooms_ = p.findAll("b", string=re.compile(":"))[0].parent.text # property type & room counts
        colon = type_rooms_.index(':')
        property_type, type_rooms = type_rooms_[:colon], type_rooms_[colon+1:].split()            
        d['property_type'] = property_type
        
        room_types = [im['title'] for im in 
                      p.findAll('img')] # room count types
        
        for room_type, count in zip(room_types, type_rooms):
            d[room_type] = count

        map_link_suffix = p.find("a", string="Map")
        if map_link_suffix: 
            map_link_suffix = map_link_suffix['href']
            d['map_link'] = BASE_URL + map_link_suffix        
            d['lat'] = float(map_link_suffix.split('&')[1].replace('lat=',''))
            d['lng'] = float(map_link_suffix.split('&')[2].replace('lng=',''))
        
        
        agent_ = p.find("b", string=[re.compile("Agent")])
        if agent_: 
            d['agent'] = agent_.parent.text.replace("Agent: ", '')
        
        dfs.append(pd.DataFrame(d, index=[0]))
    return pd.concat(dfs)

def get_suburb(suburb, verbose=True, cd=20):
    """
    Retrieve all properties from a given search page
    """
    page = 0
    dfs = pd.DataFrame(columns=['link'])
    while True:
        if verbose: print(page, end='..', flush=True)
        try:
            response, soup, df = get_suburb_page(suburb, page)
            if not isinstance(df, pd.DataFrame) or \
                df['link'].isin(dfs['link']).all(): 
                    df = None
                    break
            df['page'] = page
            dfs = pd.concat([dfs, df])
            page += 1
            # time.sleep(3)
        except AttributeError:
            if verbose: print(f"Request Timeout, waiting ({cd}s)...")
            time.sleep(cd)
            resp = requests.get(BASE_URL)
            df = pd.DataFrame()
        if not isinstance(df, pd.DataFrame): break
        
    return dfs

def get_suburbs(verbose=True, cd=20, topn=None, start=None, stop=None, save=True):
    """
    Retrieve all properties and search pages of a given suburb
    """
    dfs = []
    if verbose: print("Getting", topn if topn else "all", flush=True)
    # for i, suburb in enumerate(suburbs['suburb'].values[:topn]):
    for i, suburb in enumerate(suburbs['suburb'].values[start:stop]):
        if verbose: print(suburb, end='..', flush=True)
        df = get_suburb(suburb, verbose=verbose, cd=cd)
        df.to_csv(OUTPUT_DIR + f"{suburb}_{dt.now().isoformat()}.csv", index=False)
        dfs.append(df)
    return pd.concat(dfs)

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    start, stop = 0, 200
    df = get_suburbs(start=start, stop=stop)
    df = df.astype({'page': int})
    df.to_csv(OUTPUT_DIR + f'data_{start}-{stop}_{dt.now().isoformat()}.csv', index=False)

