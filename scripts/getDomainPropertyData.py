
import json 
import os 
from urllib import response 
import requests 

class DomainPropertyReader: 

    def __init__(self, domainAPIKey): 
        
        self.domainAPIKey = domainAPIKey 

    def getProperty(self, propertyID): 

        """Returns the given property """ 

        getPropertyCommand = f"""
        curl -X GET "https://api.domain.com.au/v1/properties/{propertyID}" -H "accept: application/json" -H "X-Api-Key: {self.domainAPIKey}" 
        """ 

        property = json.loads(os.popen(getPropertyCommand).read()) 

        return property 
    
    def getPropertyPriceEstimate(self, propertyID): 

        """Returns the price estimate for the given property """ 

        getPropertyPriceEstimateCommand = f"""
        curl -X GET "https://api.domain.com.au/v1/properties/{propertyID}/priceEstimate" -H "accept: application/json" -H "X-Api-Key: {self.domainAPIKey}" 
        """ 

        propertyPriceEstimate = json.loads(os.popen(getPropertyPriceEstimateCommand).read()) 

        return propertyPriceEstimate 
    
    def getPropertiesByLocation(self, locationTerms): 

        """Returns the properties in a given location """ 

        MAX_PROPERTIES = 20 

        getPropertiesByLocationCommand = f"""
        curl -X GET "https://api.domain.com.au/v1/properties/_suggest?terms={locationTerms}&pageSize={MAX_PROPERTIES}&channel=All" -H "accept: application/json" -H "X-Api-Key: {self.domainAPIKey}" 
        """ 

        propertiesByLocation = json.loads(os.popen(getPropertiesByLocationCommand).read()) 

        return propertiesByLocation 
    

def main(): 

    print(f"Reading the Domain API key \n") 
    domainAPIKeyJSON = json.load(open("domainAPIKey.json")) 
    domainAPIKey = domainAPIKeyJSON["key"] 

    print(f"Creating a Domain property reader with the following API key ") 
    print(f"domainAPIKey = {domainAPIKey} \n") 
    aPropertyReader = DomainPropertyReader(domainAPIKey) 

    examplePropertyID = "RF-8884-AK" 
    print(f"Requesting the following property \n") 
    print(f"{examplePropertyID} \n") 
    aProperty = aPropertyReader.getProperty(propertyID = examplePropertyID) 
    print(aProperty["address"]) 

    outputFileName = "property.json" 
    print(f"Writing the requested property to the following location \n") 
    print(f"{outputFileName} \n") 
    outputFile = open(outputFileName, mode = "w", encoding = "utf-8") 
    json.dump(aProperty, fp = outputFile, ensure_ascii = False, indent = 4) 

    print(f"Requesting the price estimate for the following property \n") 
    print(f"{examplePropertyID} \n") 
    aPropertyPriceEstimate = aPropertyReader.getPropertyPriceEstimate(
        propertyID = examplePropertyID) 
    print(aPropertyPriceEstimate) 

    outputFileName = "propertyPriceEstimate.json" 
    print(f"Writing the requested property price estimate to the following location \n") 
    print(f"{outputFileName} \n") 
    outputFile = open(outputFileName, mode = "w", encoding = "utf-8") 
    json.dump(aPropertyPriceEstimate, fp = outputFile, ensure_ascii = False, indent = 4) 

    exampleLocationTerms = "Rowville" 
    print(f"Requesting properties in the given location \n") 
    print(f"{exampleLocationTerms} \n") 
    aLocationProperties = aPropertyReader.getPropertiesByLocation(
        locationTerms = exampleLocationTerms) 
    print(aLocationProperties) 

    outputFileName = "locationProperties.json" 
    print(f"Writing the requested properties to the following location \n") 
    print(f"{outputFileName} \n") 
    outputFile = open(outputFileName, mode = "w", encoding = "utf-8") 
    json.dump(aLocationProperties, fp = outputFile, ensure_ascii = False, indent = 4) 



if __name__ == "__main__": 

    main() 