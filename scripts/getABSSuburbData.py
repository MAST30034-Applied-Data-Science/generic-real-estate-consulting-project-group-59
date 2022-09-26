
import os 
import requests 

import pandas 
import geopandas

def downloadFile(url, downloadLocation): 

    # Downloads the given url to the given download location 

    if (os.path.exists(downloadLocation)): 

        return 

    response = requests.get(url) 

    downloadFile = open(downloadLocation, mode = "wb") 

    downloadFile.write(response.content) 

def main(): 

    locationABSURL = "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/allocation-files" 
    
    print(f"Downloading the required ABS location files from thge following URL ") 
    print(f"{locationABSURL}") 

    locationABSFiles = [
        "MB_2021_AUST.xlsx", 
        "SA1_2021_AUST.xlsx", 
        "SA2_2021_AUST.xlsx", 
        "SA3_2021_AUST.xlsx", 
        "SA4_2021_AUST.xlsx", 
        "SAL_2021_AUST.xlsx", 
        "LGA_2021_AUST.xlsx"
    ] 

    for locationABSFile in locationABSFiles: 

        print(f"Downloading the following file ") 
        print(f"{locationABSFile}") 

        # Get the URL of the given file 
        locationABSFileURL = f"{locationABSURL}/{locationABSFile}" 
        downloadLocation = f"../data/raw/{locationABSFile}" 

        # Download the given file to the relevant location 
        downloadFile(locationABSFileURL, downloadLocation) 

    print("Reading the downloaded location files ") 
    meshBlockData = pandas.read_excel("../data/raw/MB_2021_AUST.xlsx") 
    # statisticalArea1Data = pandas.read_excel("../data/raw/SA1_2021_AUST.xlsx") 
    # statisticalArea2Data = pandas.read_excel("../data/raw/SA2_2021_AUST.xlsx") 
    # statisticalArea3Data = pandas.read_excel("../data/raw/SA3_2021_AUST.xlsx") 
    statisticalArea4Data = pandas.read_excel("../data/raw/SA4_2021_AUST.xlsx") 
    localGovernmentAreaData = pandas.read_excel("../data/raw/LGA_2021_AUST.xlsx") 
    suburbData = pandas.read_excel("../data/raw/SAL_2021_AUST.xlsx") 

    print(statisticalArea4Data.head(n = 5)) 
    print(localGovernmentAreaData.head(n = 5)) 

    # Join the mesh block data with the suburb data 
    print(meshBlockData.describe()) 

    meshBlockData.merge(other = suburbData, on = "MB_CODE_2021") 
    meshBlockData.to_csv("../data/raw/suburbData.csv") 

if __name__ == "__main__": 

    main() 
