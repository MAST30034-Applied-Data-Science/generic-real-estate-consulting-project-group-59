#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import geopandas as gpd
import pandas as pd
import requests
import numpy as np
import json
import os
from datetime import datetime as dt
from glob import glob

from ORS_API_key import ORS_API_KEY

OUTPUT_DIR = "../data/raw/ORS/"
PTV_DIR = '../data/raw/PTV/ll_gda94/mapinfo/whole_of_dataset/victoria/PUBLIC_TRANSPORT'
PTV_LAYERS = {
    "tram": "PTV_METRO_TRAM_STOP",
    "train_regional": "PTV_REGIONAL_TRAIN_STATION",
    "train_metro": "PTV_METRO_TRAIN_STATION",
    "bus_regional": "PTV_REGIONAL_BUS_STOP",
    "bus_metro": "PTV_METRO_BUS_STOP",
    "bus_sky": "PTV_SKYBUS_STOP",
    "bus_coach": "PTV_REGIONAL_COACH_STOP"
}

HOUSE_SPEAKING_PATH = sorted(glob("../data/curated/housespeakingsame/*.csv"))[-1]

ORS_URL = "https://api.openrouteservice.org/v2/matrix/"
ORS_TYPES = ['driving-car', 'foot-walking']

HEADERS = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': ORS_API_KEY,
    'Content-Type': 'application/json; charset=utf-8'
}

def read_PTV():
    """
    Reads different layers of the PTV stations dataset
    """
    ptv = dict()
    for name, layer in PTV_LAYERS.items():
        gdf = gpd.read_file(PTV_DIR, layer=layer)
        gdf['suburb'] = gdf['STOP_NAME'].str.extract(r"\((.*)\)")
        ptv[name] = gdf
    return ptv

def read_properties():
    """
    Reads house speakingsame property data
    """
    df = pd.read_csv(HOUSE_SPEAKING_PATH)
    return df

# def gen_body(df, ptv, ptv_types, suburb):#, prop_chunk_size=5000):
#     property_latlongs = df.apply(lambda d: [d['lat'], d['lng']], axis=1).tolist()    
    
#     ptv_latlongs = []
    
#     for ptv_type, ptv_df in ptv.items():
#         if ptv_type in ptv_types:
#             ptv_latlongs = ptv_latlongs + ptv_df.apply(lambda d: [d['LATITUDE'], d['LONGITUDE']], axis=1).tolist()
    
#     bodies = []
#     prop_chunk_size = 3500 - len(ptv_latlongs)
#     for i in range(0, len(property_latlongs), prop_chunk_size):
#         body = {"locations": property_latlongs[i:i+prop_chunk_size] + ptv_latlongs}
#         bodies.append(body)
#     return property_latlongs, ptv_latlongs, bodies
                                                     
def gen_body_matrix(df, coord, chunk_size=500):
    """
    Create coordinates JSON post applications to ORS
    Maps coordinates from dataframe to one coordinate for the matrix endpoint
    """
    property_latlongs = df.apply(lambda d: [d['lng'], d['lat']], axis=1).tolist()    
    bodies = []
    for i in range(0, len(property_latlongs), chunk_size):
        chunk = property_latlongs[i:i+chunk_size]
        body = {"locations": [coord] + chunk, "metrics": ["distance", "duration"],
                "destinations": [0], "sources": [i+1 for i in range(len(chunk))]}
        bodies.append(body)
    return bodies

def get_train_station(ptv, name):
    """
    Retrieves coordinates for a train station
    """    
    sthcrs = ptv['train_metro'].loc[ptv['train_metro']['STOP_NAME']==name]
    sthcrs_coord = list(sthcrs[['LONGITUDE', 'LATITUDE']].values[0])    
    return sthcrs_coord

def map_properties_to_coord(df, coord, chunk_size=500, verbose=True):
    bodies = gen_body_matrix(df, coord, chunk_size)
    responses, n_bodies = [], len(bodies)
    for i, body in enumerate(bodies):
        if verbose: print(f"{i}/{n_bodies}",end='..')
        while True:
            response = requests.post(ORS_URL + ORS_TYPES[0], headers=HEADERS, 
                                 json=body)
            if response.status_code == 200: break
            print(response.content)
        responses.append(response)
    return responses, bodies

def parse_response(response):
    response_json = response.json()
    data = pd.DataFrame({
        "duration": np.array(response_json['durations']).reshape(-1),
        "distance": np.array(response_json['distances']).reshape(-1),
        "destination": response_json['destinations'] * len(response_json['durations']),
        "source": np.array(response_json['sources']).reshape(-1)
    })
    return data

def parse_responses(responses):
    return pd.concat([parse_response(response) for response in responses])

if __name__=="__main__":
    ptv = read_PTV()
    df = read_properties()
    df = df.dropna(subset=['lng','lat']).drop_duplicates(subset=['lng','lat'])
    
    sthcrs_coord = get_train_station(ptv, "Southern Cross Railway Station (Melbourne City)")
    responses, bodies = map_properties_to_coord(df, sthcrs_coord)
    response_df = parse_responses(responses)    
    
    if not os.path.exists(OUTPUT_DIR): os.mkdir(OUTPUT_DIR)
    response_df.to_csv(OUTPUT_DIR + f"sthcrs_{dt.now()}.csv")
