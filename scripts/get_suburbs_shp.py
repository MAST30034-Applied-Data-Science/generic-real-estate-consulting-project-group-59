#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import urlretrieve
import os
import zipfile

DOWNLOAD_URL = "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SAL_2021_AUST_GDA2020_SHP.zip"
OUTPUT_DIR = "../data/raw/suburbs/"
FNAME = "SAL_2021_AUST_GDA2020_SHP.zip"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

urlretrieve(DOWNLOAD_URL, OUTPUT_DIR + FNAME)

with zipfile.ZipFile(OUTPUT_DIR + FNAME, 'r') as zip_ref:
    zip_ref.extractall(OUTPUT_DIR)

