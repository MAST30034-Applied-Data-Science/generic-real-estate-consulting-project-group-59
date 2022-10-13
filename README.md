# Generic Real Estate Consulting Project
This Generic Real Estate Consulting Project is focusing on investgating and predicting the rent price.

This project is also including:
1. Internal and external features in predicting rental prices
2. Top 10 suburbs with the highest predicted growth rate?
3. Liveable and affordable suburbs

# Contributors Group 59
* Terry Chow 1138391
* Zhiquan Lai 1118797
* Manish Khilari 1173214
* Jiajia Guo 1135319
* Arjun Rajkumar 910941

# Requirements
using pip exec requirement.txt to install environment

# Instructions to Reproduce

## [House SpeakingSame](http://house.speakingsame.com/)

1. `/scripts/scrape_house_speakingsame_suburbs.py` outputs to `/data/raw/top_rent_suburbs_<dt>.csv`
2. `/scripts/scrape_house_speakingsame_rent.py` outputs multiple suburbs to `/data/raw/housespeakingsame/rent/<suburb>_<dt>.csv`
3. `/scripts/scrape_house_speakingsame_buy.py` outputs multiple suburbs to `/data/raw/housespeakingsame/buy/<suburb>_<dt>.csv`
4. `/scripts/preprocess_house_speakingsame.py` outputs to `/data/curated/housespeakingsame/<dt>.csv`

## Crime Data
run notebooks/crime.ipynb will contain both download and analysis

## PTV Data
1. Run notebooks/PTVdataProcessing.ipynb to download and see analysis of data.
2. Run ipynb file in PTV_visualisations folders to get vistualisation.

notes: The download link is temporary link from https://datashare.maps.vic.gov.au/. It might be expired anytime in the future

Instruction to reorder the PTV data:
1. go to https://datashare.maps.vic.gov.au/
2. search "Public Transport a collection of PTV datasets"
3. Projection: Geographicals on GDA94. Buffer: No buffer. File Format: ESRI File Geodatabase. Area: Custom Cookie-  VICTORIA_BUFF
4. The data will be sent by email.

## Domain Property Data 

Welcome to the Domain Property Data API. 

### Setup Instructions 

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
