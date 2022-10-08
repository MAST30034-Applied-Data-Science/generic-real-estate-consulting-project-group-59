# Generic Real Estate Consulting Project
Groups should generate their own suitable `README.md`.


# Domain Property Data 

Welcome to the Domain Property Data API. 

# Preliminary Setup
1. Navigate to `/scripts/`
2. Execute `get_suburbs_shp.py`
3. Obtain ORS data (through download)
4. Execute `/notebooks/PTVdataProcessing.ipynb`

# HouseSpeakingSame Data

1. Navigate to `/scripts/housespeakingsame`
2. Execute `scrape_house_speakingsame_suburbs.py`
3. Execute `preprocess_house_speakingsame_suburbs.py`
4. Execute `scrape_house_speakingsame_schools.py`

# Crime Data
crime.ipynb will contain both download and analysis

# PTV Data
1. Run PTVdataProcessing.ipynb to download and see analysis of data.
2. Run ipynb file in PTV_visualisations folders to get vistualisation.

notes: The download link is temporary link from https://datashare.maps.vic.gov.au/. It might be expired anytime in the future

Instruction to reorder the PTV data:
1. go to https://datashare.maps.vic.gov.au/
2. search "Public Transport a collection of PTV datasets"
3. Projection: Geographicals on GDA94. Buffer: No buffer. File Format: ESRI File Geodatabase. Area: Custom Cookie-  VICTORIA_BUFF
4. The data will be sent by email within one bussiness day.

## Setup Instructions 

Setup instructions for the Domain Property API can be found below. 

1. Create a Domain Developer account for API access. Domain API access instructions can be found at [Domain Group: Developer Portal](https://developer.domain.com.au/). 

2. Navigate to the following location. 

- > scripts 

2. Ensure that the following files are present. 

- > domainAPIKey.json 
- > victoriaSuburbs.txt 
- > getDomainPropertyData.py 

3. Update the following file with the new API key. 

- > domainAPIKey.json 

4. Confirm that the following output files have been generated within the same folder. 

- > property.json 


# Instructions to Reproduce

## [House SpeakingSame](http://house.speakingsame.com/)

1. `/scripts/scrape_house_speakingsame_suburbs.py` outputs to `/data/raw/top_rent_suburbs_<dt>.csv`
2. `/scripts/scrape_house_speakingsame_rent.py` outputs multiple suburbs to `/data/raw/housespeakingsame/rent/<suburb>_<dt>.csv`
3. `/scripts/scrape_house_speakingsame_buy.py` outputs multiple suburbs to `/data/raw/housespeakingsame/buy/<suburb>_<dt>.csv`
4. `/scripts/preprocess_house_speakingsame.py` outputs to `/data/curated/housespeakingsame/<dt>.csv`

