
import os

def getProperty(propertyID): 

    # Get the given property through the Domain API 
    getPropertyCommand = f"""
    curl -X GET "https://api.domain.com.au/v1/properties/{propertyID}" -H "accept: application/json" -H "X-Api-Key: key_64e2ab5553a5da99db9f14c597e302b6"
    """ 

    os.system(getPropertyCommand) 

def main(): 

    propertyID = "RF-8884-AK" 

    getProperty(propertyID) 

if __name__ == "__main__": 

    main() 
