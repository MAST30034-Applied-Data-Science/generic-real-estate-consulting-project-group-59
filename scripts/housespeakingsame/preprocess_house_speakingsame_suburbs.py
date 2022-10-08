#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from glob import glob
import pandas as pd
import os
from pathlib import Path

DATA_DIR = "../../data/raw/housespeakingsame/top/"
OUTPUT_DIR = "../../data/curated/housespeakingsame/top/"

def preprocess():
    for p in glob(DATA_DIR + '*.csv'):
        fname = p.split('/')[-1]
        df = pd.read_csv(p)
        df['value'] = df['value'].str.replace(r"\$|,|%", '')
        df.to_csv(OUTPUT_DIR + fname)

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR): Path.mkdir(Path(DATA_DIR), parents=True)
    preprocess()