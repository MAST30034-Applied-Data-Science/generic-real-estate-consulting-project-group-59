#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import re
import os
from glob import glob
from datetime import datetime as dt

OUTPUT_DIR = "../data/curated/housespeakingsame/"

sub_rent_paths = glob('../data/raw/housespeakingsame/rent/*.csv')
sub_buy_paths = glob('../data/raw/housespeakingsame/buy/*.csv')

def parse_date(x):
    if pd.notna(x):
        x = x.strip()
        n = len(x.split())
        if n==3: return dt.strptime(x, "%d %b %Y")
        elif n==2: return dt.strptime(x, "%b %Y")
        else: return dt.strptime(x, "%Y")
    else: return x

def land_building_size(x):
    if pd.isna(x): return x, x
    lb = x.split('|')
    if len(lb)==2: return int(lb[0]), int(lb[1].replace("Building size: ", ''))
    else: return int(lb[0]), np.nan

def cast_int(x):
    if pd.isna(x): return x
    try: return int(x)
    except ValueError: return np.nan

def parse_list(x):
    if pd.isna(x): return x, x, x, x
    is_over = 'over' in x
    x = re.sub("list|over|\$|,", '', x)
    l = x.split('-')
    if len(l)==2: 
        minlist, maxlist = float(l[0]), float(l[1])
        lis = (minlist+maxlist)/2
    else:
        minlist, maxlist, lis = np.nan, np.nan, float(l[0])
    return lis, is_over, minlist, maxlist
    

def prepo(df):
    df['suburb'] = df['link'].str.findall("q=[^\&]*").apply(lambda x: x[0].replace('q=','').replace('+', ' '))
    df['sold_price'] = df['sold_price_'].str.replace('\$|,|undisclosed','').apply(lambda x: float(x) if x else np.nan)
    df['sold_date'] = df['sold_date_'].apply(parse_date)
    df = df.drop(['sold_is_auction_', 'last_sold_is_auction_'], axis=1)
    df[['land_size', 'building_size']] = df['land_size_'].str.replace(',|\ssqm','').apply(land_building_size).tolist()    
    df['bed'] = df['Bed rooms_'].apply(cast_int)
    df['bath'] = df['Bath rooms_'].apply(cast_int)
    df['car'] = df['Car spaces_'].apply(cast_int)
    df['rent_price'] = df['rent_price_'].str.lower().str.replace('\$|,|undisclosed|pw', '').apply(lambda x: float(x) if x else np.nan)
    df['rent_date'] = df['rent_date_'].apply(parse_date)
    df['last_sold_price'] = df['last_sold_price_'].str.replace('Sold|\$|,', '').astype(float)
    df['last_sold_date'] = df['last_sold_date_'].apply(parse_date)
    df[['list', 'is_over', 'minlist', 'maxlist']] = df['list_text_'].str.lower().apply(parse_list).tolist()
    return df

if __name__=="__main__":
    bdf = pd.concat([pd.read_csv(csv) for csv in sub_buy_paths]).drop_duplicates(subset=['link'])
    rdf = pd.concat([pd.read_csv(csv) for csv in sub_rent_paths]).drop_duplicates(subset=['link'])
    
    bdf['source'] = "sold"
    rdf['source'] = "rent"
    
    rawdf = pd.concat([bdf, rdf])
    
    rawdf.columns = ['link', 'address', 'map_link', 'lat', 'lng', 'sold_price_', 'sold_date_',
           'sold_is_auction_', 'land_size_', 'property_type', 'Bed rooms_',
           'last_sold_price_', 'last_sold_date_', 'last_sold_is_auction_', 'agent',
           'rent_price_', 'rent_date_', 'Bath rooms_', 'Car spaces_', 'page',
           'list_text_', 'source']
    df = prepo(rawdf)
    print(df.shape)
    
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
        
    df.to_csv(OUTPUT_DIR + f"{dt.now()}.csv", index=False)
