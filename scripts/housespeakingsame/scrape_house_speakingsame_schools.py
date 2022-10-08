#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from pathlib import Path

URL = "http://house.speakingsame.com/topschool.php?sta=vic"
OUTPUT_DIR = "../../data/raw/housespeakingsame/schools/"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
COLUMNS = ['suburb', 'type', 'name', 'rank']

def get(url):
    while True:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response  

def scrape_page():
    bs_obj = BeautifulSoup(get(URL).content, "html.parser")
    tab = bs_obj.find("table", {"cellspacing": "0", "cellpadding": "5", "width": "100%"})
    rows = tab.findAll("tr")
    
    data = []
    for row in rows[1:]: # First row is headers
        row_data_ = row.findAll("td")
        row_data = [c.text for c in row_data_]
        row_data[0] = ''.join(list(row_data[0])[1:]) # Parse byte prefix in suburb
        data.append(row_data)
        
    df = pd.DataFrame(data, columns=COLUMNS)
    df['rank'] = df['rank'].apply(lambda x: int(x) if x else None)
    return df

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR): Path.mkdir(Path(OUTPUT_DIR), parents=True)
    print("Obtaining Suburb Top Schools...")
    df = scrape_page()
    df.to_csv(OUTPUT_DIR + "top_schools.csv", index=False)
