
import json 
import os 
from urllib import response 
import requests 

from getDomainPropertyData import DomainPropertyReader 

def main(): 

    MAX_DOMAIN_PROPERTY_REQUESTS_PER_DAY = 500 

    print(f"Reading the Domain API key \n") 
    domainAPIKeyJSONFile = open("domainAPIKey.json")
    domainAPIKeyJSON = json.load(domainAPIKeyJSONFile) 
    domainAPIKeyJSONFile.close() 
    domainAPIKey = domainAPIKeyJSON["key"] 

    print(f"Creating a Domain property reader with the following API key ") 
    print(f"domainAPIKey = {domainAPIKey} \n") 
    aPropertyReader = DomainPropertyReader(domainAPIKey) 

    print(f"Reading the given property IDs \n") 
    propertyIDFile = open("../data/raw/propertyIDs.txt") 
    propertyIDs = [propertyID[:-1] for propertyID in propertyIDFile] 
    propertyIDFile.close() 
    print(propertyIDs[:5]) 

    propertiesFolder = "../data/raw/properties" 
    
    # Ensure the properties folder exists 
    if not os.path.exists(propertiesFolder): 

        os.makedirs(propertiesFolder) 

    print(f"Writing the requested properties to the following folder \n") 
    print(f"{propertiesFolder} \n") 

    # Save the requested properties 
    outputPropertyFileName = f"../data/raw/properties.csv" 
    print(f"Writing the saved properties to the following location \n") 
    print(f"{outputPropertyFileName} \n") 
    outputPropertyFile = open(outputPropertyFileName, mode = "a") 

    # Get the property column names 
    propertyColNames = [
        "id", "canonicalUrl", "lat", "lon", 
        "addressId", "bathrooms", "bedrooms", "carSpaces", 
        "created", "numFeatures", "isResidential", "numPhotos", 
        "planNumber", "postcode", "propertyCategory", "state", "status", 
        "streetAddress", "streetName", "streetNumber", "streetTypeLong", 
        "suburb"
    ] 

    # Get the property header 
    propertyHeader = "" 

    for colName in propertyColNames: 

        propertyHeader += f"{colName}," 

    propertyHeader = propertyHeader[:-1] 

    if (os.path.getsize(outputPropertyFileName) == 0): 
        
        outputPropertyFile.write(f"{propertyHeader}\n") 

    # Get the given properties 
    numDomainPropertyRequests = 0 

    for propertyID in propertyIDs: 

        propertyJSONFileName = f"{propertiesFolder}/{propertyID}.json" 

        if (os.path.exists(propertyJSONFileName)): 

            print(f"The given property is already stored at the following location \n") 
            print(f"{propertyJSONFileName} \n") 

            continue 

        print(f"Requesting the following property ID \n") 
        print(f"{propertyID} \n") 

        property = aPropertyReader.getProperty(propertyID) 
        numDomainPropertyRequests += 1 

        if "type" in property: 

            print(f"{property} \n\n") 
            print(f"The maximum number of property requests have been exceeded \n") 
            print(f"Domain API maximum number of property requests per day: {MAX_DOMAIN_PROPERTY_REQUESTS_PER_DAY} \n") 
            print(f"Number of requests completed: {numDomainPropertyRequests} \n") 

            break 

        # Save the requested property 
        print(f"Writing the requested property to the following location \n") 
        print(f"{propertyJSONFileName} \n") 
        propertyJSONFile = open(
            propertyJSONFileName, mode = "w", encoding = "utf-8") 
        json.dump(property, fp = propertyJSONFile, 
        ensure_ascii = False, indent = 4) 
        propertyJSONFile.close() 

        # Get the property line 
        propertyCanonicalUrl = property["canonicalUrl"] 
        propertyLat = property["addressCoordinate"]["lat"] 
        propertyLon = property["addressCoordinate"]["lon"] 
        propertyAddressID = property["addressId"] 
        propertyBathrooms = property["bathrooms"] 
        propertyBedrooms = property["bedrooms"] 
        propertyCarSpaces = property["carSpaces"] 
        propertyCreated = property["created"] 
        propertyFeatures = " ".join(property["features"]) 
        propertyIsResidential = property["isResidential"] 
        propertyPhotos = " ".join(
            [photo["fullUrl"] for photo in property["photos"]]
        ) 
        propertyPlanNumber = property["planNumber"] 
        propertyPostcode = property["postcode"] 
        propertyCategory = property["propertyCategory"] 
        propertyState = property["state"] 
        propertyStatus = property["status"] 
        propertyStreetAddress = property["streetAddress"] 
        propertyStreetName = property["streetName"] 
        propertyStreetNumber = property["streetNumber"] 
        propertyStreetTypeLong = property["streetTypeLong"] 
        propertySuburb = property["suburb"] 

        propertyLine = f"{propertyID},{propertyCanonicalUrl},{propertyLat},{propertyLon},{propertyAddressID},{propertyBathrooms},{propertyBedrooms},{propertyCarSpaces},{propertyCreated},{propertyFeatures},{propertyIsResidential},{propertyPhotos},{propertyPlanNumber},{propertyPostcode},{propertyCategory},{propertyState},{propertyStatus},{propertyStreetAddress},{propertyStreetName},{propertyStreetNumber},{propertyStreetTypeLong},{propertySuburb}" 

        outputPropertyFile.write(f"{propertyLine}\n") 
        
    # Close the property ID file after completion 
    propertyIDFile.close() 

    # Close the output property file after completion 
    outputPropertyFile.close() 

if __name__ == "__main__": 

    main() 
