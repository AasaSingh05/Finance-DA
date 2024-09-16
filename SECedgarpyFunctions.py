#importing the necessary libraries
from requests import get
import pandas as pd
from SECedgarpyExceptions import ErrorFoundWhileGETRequest

#defining the global Variables to be used
HEAD ={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"}
URL_FORM = "https://www.sec.gov/Archives/edgar/data/" 
TEN_K_FORM = ""

#defining a function for the filter func later
#to filter out and get only the 10-k reports
def filterfunc(a: list) -> bool:
    if(a[0] == "10-K"):
        return True
    else:
        return False 

#to extract the url using the CIK which is passed into the func
def extract10Kurl(cikval: str):

    #defining the empty lists used to store the interim values
    listofforms = []
    urllist = []

    #the url where the data is stored at
    url = f"https://data.sec.gov/submissions/CIK{cikval}.json"
    
    #using the HTTP get request to pull all data from the website
    resp = get(url, timeout=5000, headers=HEAD)
    
    #type convert it to a JSON file
    data = resp.json()

    #to get the ticker, lstriped CIK value, and the actual relevant values
    ticker = str(data["tickers"][0]).lower()
    CIK = str(data["cik"])
    dataform = data["filings"]["recent"]

    #to extract only the needed data from the dataform json
    for subzip in zip (dataform["form"], dataform["accessionNumber"] , dataform["reportDate"]):
        
        #added to the list as an elt
        listofforms.append(list(subzip))

    #filtering through the array to only 10-k files
    finalarr = list(filter(filterfunc, listofforms))
        
    #To iterate and reformat the entries to remove unnecessary chars in the strings
    for elt in finalarr:
        elt[1] = str(elt[1]).replace("-","")
        elt[2] = str(elt[2]).replace("-","")

    #convert the info we have into usable urls for web data scraping
    for finelt in finalarr:
        newurl = URL_FORM + CIK + "/" + finelt[1] + "/"+ ticker + "-" + finelt[2] + ".htm"
        urllist.append(newurl)
      
    #returning the list of all the urls  
    return urllist

#to convert the URL to direct xlsx Files
def URLtoXLSX(URLlist: list[str]):
    
    #to iterate through all the string urls
    for urlelt in URLlist:
        
        #change the url to end in the xlsx file name
        urlelt = urlelt[:-17] + "Financial_Report.xlsx"
        
    #returning the url list of values
    return URLlist

def getXLSXfile(urllist: list[str], nameOfFile):
    
    #iterating through every url we have
    for urlelt in urllist:
        
        #we go through with the HTTP get request
        urlresp = get(urlelt, timeout= 5000, headers = HEAD)
            
        #we get the status code of the request
        statcode = urlresp.status_code
        
        #error handling to check
        if(statcode == 404):
            raise FileNotFoundError
        
        #if anything except for 200 or 404
        elif(statcode != 200):
            raise ErrorFoundWhileGETRequest
        
        #if request is successful
        else:
            
            #open a file with the name
            with (nameOfFile, "wb") as f:
                
                #write all binary into the file as given 
                f.write(urlresp.content)

#to generate the CSV report by filtering and keeping the necessary sheets only
def GenerateCSVreport(nameOfFile):
    
    # < ---currently placeholders--- >     
    '''
    #to read the contents of the XLSX file
    data = pd.read_excel(nameOfFile)
    
    #heading of the sheet which act as the filter of which sheets to keep
    sheetheadings = []
    
    
    print()





#test case (intel CIK)
urllist = extract10Kurl("0000050863")

#Printing all the urls
URLtoXLSX(urllist)
'''