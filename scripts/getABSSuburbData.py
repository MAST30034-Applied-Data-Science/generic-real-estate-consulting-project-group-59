
from operator import sub
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

    downloadFolder = "../data/raw" 

    meshBlockName = "MB_2021_AUST" 
    print(f"Reading {meshBlockName} ") 

    if (os.path.exists(f"{downloadFolder}/{meshBlockName}.csv")): 

        print(f"{downloadFolder}/{meshBlockName}.csv found ") 
    else: 

        print(f"Creating {downloadFolder}/{meshBlockName}.csv ")
        meshBlockData = pandas.DataFrame(pandas.read_excel(f"{downloadFolder}/{meshBlockName}.xlsx")) 
        meshBlockData.to_csv(f"{downloadFolder}/{meshBlockName}.csv") 
    
    meshBlockData = pandas.DataFrame(pandas.read_csv(f"{downloadFolder}/{meshBlockName}.csv")) 

    statisticalArea1Name = "SA1_2021_AUST" 
    print(f"Reading {statisticalArea1Name} ") 

    if (os.path.exists(f"{downloadFolder}/{statisticalArea1Name}.csv")): 

        print(f"{downloadFolder}/{statisticalArea1Name}.csv found ") 
    else: 

        print(f"Creating {downloadFolder}/{statisticalArea1Name}.csv ")
        statisticalArea1Data = pandas.DataFrame(pandas.read_excel(f"{downloadFolder}/{statisticalArea1Name}.xlsx")) 
        statisticalArea1Data.to_csv(f"{downloadFolder}/{statisticalArea1Name}.csv") 
    
    statisticalArea1Data = pandas.DataFrame(pandas.read_csv(f"{downloadFolder}/{statisticalArea1Name}.csv")) 

    statisticalArea2Name = "SA2_2021_AUST" 
    print(f"Reading {statisticalArea2Name} ") 

    if (os.path.exists(f"{downloadFolder}/{statisticalArea2Name}.csv")): 

        print(f"{downloadFolder}/{statisticalArea2Name}.csv found ") 
    else: 

        print(f"Creating {downloadFolder}/{statisticalArea2Name}.csv ")
        statisticalArea2Data = pandas.DataFrame(pandas.read_excel(f"{downloadFolder}/{statisticalArea2Name}.xlsx")) 
        statisticalArea2Data.to_csv(f"{downloadFolder}/{statisticalArea2Name}.csv") 
    
    statisticalArea2Data = pandas.DataFrame(pandas.read_csv(f"{downloadFolder}/{statisticalArea2Name}.csv")) 

    statisticalArea3Name = "SA3_2021_AUST" 
    print(f"Reading {statisticalArea3Name} ") 

    if (os.path.exists(f"{downloadFolder}/{statisticalArea3Name}.csv")): 

        print(f"{downloadFolder}/{statisticalArea3Name}.csv found ") 
    else: 

        print(f"Creating {downloadFolder}/{statisticalArea3Name}.csv ")
        statisticalArea3Data = pandas.DataFrame(pandas.read_excel(f"{downloadFolder}/{statisticalArea3Name}.xlsx")) 
        statisticalArea3Data.to_csv(f"{downloadFolder}/{statisticalArea3Name}.csv") 
    
    statisticalArea3Data = pandas.DataFrame(pandas.read_csv(f"{downloadFolder}/{statisticalArea3Name}.csv")) 

    statisticalArea4Name = "SA4_2021_AUST" 
    print(f"Reading {statisticalArea4Name} ") 

    if (os.path.exists(f"{downloadFolder}/{statisticalArea4Name}.csv")): 

        print(f"{downloadFolder}/{statisticalArea4Name}.csv found ") 
    else: 

        print(f"Creating {downloadFolder}/{statisticalArea4Name}.csv ")
        statisticalArea4Data = pandas.DataFrame(pandas.read_excel(f"{downloadFolder}/{statisticalArea4Name}.xlsx")) 
        statisticalArea4Data.to_csv(f"{downloadFolder}/{statisticalArea4Name}.csv") 
    
    statisticalArea4Data = pandas.DataFrame(pandas.read_csv(f"{downloadFolder}/{statisticalArea4Name}.csv")) 

    localGovernmentAreaName = "LGA_2021_AUST" 
    print(f"Reading {localGovernmentAreaName} ") 

    if (os.path.exists(f"{downloadFolder}/{localGovernmentAreaName}.csv")): 

        print(f"{downloadFolder}/{localGovernmentAreaName}.csv found ") 
    else: 

        print(f"Creating {downloadFolder}/{localGovernmentAreaName}.csv ")
        localGovernmentAreaData = pandas.DataFrame(pandas.read_excel(f"{downloadFolder}/{localGovernmentAreaName}.xlsx")) 
        localGovernmentAreaData.to_csv(f"{downloadFolder}/{localGovernmentAreaName}.csv") 
    
    localGovernmentAreaData = pandas.DataFrame(pandas.read_csv(f"{downloadFolder}/{localGovernmentAreaName}.csv")) 

    suburbName = "SAL_2021_AUST" 
    print(f"Reading {suburbName} ") 

    if (os.path.exists(f"{downloadFolder}/{suburbName}.csv")): 

        print(f"{downloadFolder}/{suburbName}.csv found ") 
    else: 

        print(f"Creating {downloadFolder}/{suburbName}.csv ")
        suburbData = pandas.DataFrame(pandas.read_excel(f"{downloadFolder}/{suburbName}.xlsx")) 
        suburbData.to_csv(f"{downloadFolder}/{suburbName}.csv") 
    
    suburbData = pandas.DataFrame(pandas.read_csv(f"{downloadFolder}/{suburbName}.csv")) 

    print(statisticalArea4Data.head(n = 5)) 
    print(localGovernmentAreaData.head(n = 5)) 

    # Join the suburb data with the LGA and SA2 data 
    suburbData = suburbData.merge(
        right = localGovernmentAreaData[["MB_CODE_2021","LGA_CODE_2021", "LGA_NAME_2021"]], 
        on = "MB_CODE_2021")
    
    suburbData.to_csv(f"{downloadFolder}/suburbData.csv") 

if __name__ == "__main__": 

    main() 
