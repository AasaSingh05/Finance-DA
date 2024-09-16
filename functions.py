#importing the necessary files
#to use HTTP requests
from requests import get

#global vars used
DEC_DATA_URL = "https://data.sec.gov"
HEADER = {"header": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"}

#class created for the error handling
class ErrorFoundWhileGETRequest:
    pass

#writing the functions needed for the code
def JSONfinder(cikval: str):
    
    #using the cik to find the full api val to get the json file needed
    url = DEC_DATA_URL + "/submissions/CIK" + cikval +".json"
    
    #using HTTP get to get all info into a json file 
    r = get(url, timeout=4000, headers=HEADER)
    
    #to check if request is successful or not
    if( r.status_code == 200 ):
        pass
    elif( r.status_code == 404 ):
        raise FileNotFoundError
    else:
        print(f"SECAPI failed with the following code error: {r.status_code}")
        raise ErrorFoundWhileGETRequest

    #returns the json no matter what
    return r.json()

#to get each company's table in the website
def getCompanySub(cik):
    
    #total data found with JSONfinder
    data = JSONfinder(cik)
    
    #for rn print the data
    print(data)
    
getCompanySub("0000050863")