
import json
from urllib import response 
import requests 

class DomainPropertyReader: 

    def __init__(self, domainAPIKey): 
        
        self.domainAPIKey = domainAPIKey 
    
    def getProperty(self, propertyID): 

        """Returns the given property """ 

        url = f"https://api.domain.com.au/v1/properties/{propertyID}" 
        headers = {"X-Api-Key" : self.domainAPIKey} 
        print(f"url = {url} \n") 

        response = requests.get(url, headers) 
        
        return response 

    def getAuthentication(self): 

        """Returns the authentication status of the given API key """ 

        url = f"https://api.domain.com.au/v1/me" 
        headers = {"X-Api-Key" : self.domainAPIKey} 
        print(f"url = {url} \n") 

        response = requests.get(url, headers) 
        
        return response 

def main(): 

    print(f"Reading the Domain API key \n") 
    domainAPIKeyJSON = json.load(open("domainAPIKey.json")) 
    domainAPIKey = domainAPIKeyJSON["key"] 

    print(f"Creating a Domain property reader with the following API key ") 
    print(f"domainAPIKey = {domainAPIKey} \n") 
    aPropertyReader = DomainPropertyReader(domainAPIKey) 

    print(f"Getting the authentication status of the given API key \n") 
    authenticationStatus = aPropertyReader.getAuthentication()  
    print(authenticationStatus.content) 

    print(f"Requesting a property \n") 
    aProperty = aPropertyReader.getProperty(propertyID = "RF-8884-AK") 
    print(aProperty.content) 

if __name__ == "__main__": 

    main() 