
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
        curl -X GET "https://api.domain.com.au/v1/properties/_suggest?terms=\"{locationTerms}\"&pageSize={MAX_PROPERTIES}&channel=All" -H "accept: application/json" -H "X-Api-Key: {self.domainAPIKey}" 
        """ 

        propertiesByLocation = json.loads(os.popen(getPropertiesByLocationCommand).read()) 

        return propertiesByLocation 
    

def main(): 

    print(f"Reading the Domain API key \n") 
    domainAPIKeyJSONFile = open("domainAPIKey.json")
    domainAPIKeyJSON = json.load(domainAPIKeyJSONFile) 
    domainAPIKeyJSONFile.close() 
    domainAPIKey = domainAPIKeyJSON["key"] 

    print(f"Creating a Domain property reader with the following API key ") 
    print(f"domainAPIKey = {domainAPIKey} \n") 
    aPropertyReader = DomainPropertyReader(domainAPIKey) 

    print(f"Reading the given list of suburbs \n") 
    victoriaSuburbsFile = open("victoriaSuburbs.txt") 
    victoriaSuburbs = [suburb[:-1] for suburb in victoriaSuburbsFile] 
    victoriaSuburbsFile.close() 
    print(victoriaSuburbs) 

    locationPropertiesFolder = "../data/raw/locationProperties" 
    
    # Ensure the location properties folder exists 
    if not os.path.exists(locationPropertiesFolder): 

        os.makedirs(locationPropertiesFolder) 

    print(f"Writing the requested suburb properties to the following folder \n") 
    print(f"{locationPropertiesFolder} \n") 

    # Save the requested property IDs 
    outputIDFileName = f"../data/raw/propertyIDs.txt" 
    print(f"Writing the saved property IDs to the following location \n") 
    print(f"{outputIDFileName} \n") 
    outputIDFile = open(outputIDFileName, mode = "w") 

    for suburb in victoriaSuburbs: 

        print(f"Requesting properties from the following suburb \n") 
        print(f"{suburb} \n") 

        suburbProperties = aPropertyReader.getPropertiesByLocation(
            locationTerms = suburb) 

        suburbPropertiesFolder = f"../data/raw/locationProperties/{suburb}" 

        # Ensure the suburb properties folder exists 
        if not os.path.exists(suburbPropertiesFolder): 

            os.makedirs(suburbPropertiesFolder) 

        print(f"Writing the requested suburb properties to the following folder \n") 
        print(f"{suburbPropertiesFolder} \n") 
        
        # Save the requested property IDs from the given suburb 
        for property in suburbProperties: 

            # Ensure that the returned property is in the relevant suburb 
            if property["addressComponents"]["suburb"] != suburb: 

                continue 
            
            # Save the property ID 
            propertyID = property["id"] 
            outputIDFile.write(f"{propertyID}\n") 

            # Save the requested property in the relevant suburb folder 
            outputFileName = f"{suburbPropertiesFolder}/{propertyID}.json" 
            print(f"Writing the requested property to the following location \n") 
            print(f"{outputFileName} \n") 
            outputFile = open(outputFileName, mode = "w", encoding = "utf-8") 
            json.dump(property, fp = outputFile, ensure_ascii = False, indent = 4) 
            outputFile.close() 
    
    # Close the property ID file after completion 
    outputIDFile.close() 

if __name__ == "__main__": 

    main() 