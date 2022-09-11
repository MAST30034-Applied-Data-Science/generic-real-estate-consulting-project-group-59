
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

def main(): 

    print(f"Reading the Domain API key \n") 
    domainAPIKeyJSON = json.load(open("domainAPIKey.json")) 
    domainAPIKey = domainAPIKeyJSON["key"] 

    print(f"Creating a Domain property reader with the following API key ") 
    print(f"domainAPIKey = {domainAPIKey} \n") 
    aPropertyReader = DomainPropertyReader(domainAPIKey) 

    print(f"Requesting a property \n") 
    aProperty = aPropertyReader.getProperty(propertyID = "RF-8884-AK") 
    print(aProperty["address"]) 

    outputFileName = "property.json" 
    print(f"Writing the requested property to the following location \n") 
    print(f"{outputFileName} \n") 
    outputFile = open(outputFileName, mode = "w", encoding = "utf-8") 
    json.dump(aProperty, fp = outputFile, ensure_ascii = False, indent = 4) 

if __name__ == "__main__": 

    main() 