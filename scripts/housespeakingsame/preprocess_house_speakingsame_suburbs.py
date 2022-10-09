#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from glob import glob
import pandas as pd
import os
from pathlib import Path

DATA_DIR = "../../data/raw/housespeakingsame/top/"
OUTPUT_DIR = "../../data/curated/housespeakingsame/top/"
TURNOVER_PAT = r"([\d\.]+)\s\((\d+)/(\d+)\)" # turnover format pattern

def preprocess():
    for p in glob(DATA_DIR + '*.csv'):
        fname = p.split('/')[-1]
        df = pd.read_csv(p)
        df['value'] = df['value'].str.replace(r"\$|,|%", '')
        if fname=="turnover.csv":
            # special treatment for turnover table
            df[['value', 'nsold', 'nprop']] = df['value'].str.extract(TURNOVER_PAT)
        df.to_csv(OUTPUT_DIR + fname)

if __name__ == "__main__":
#     if not os.path.exists(DATA_DIR): Path.mkdir(Path(DATA_DIR), parents=True)
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    preprocess()
