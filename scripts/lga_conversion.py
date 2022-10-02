#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from glob import glob
from xlsx2csv import Xlsx2csv

PATHS = glob("../data/raw/lga_conversion/*.xlsx")

for path in PATHS:
    print(path)
    output = path.replace(".xlsx", ".csv")
    Xlsx2csv(path, otuputencoding="utf-8").convert(output)
