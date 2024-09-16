#importing the necessary libraries
from requests import get

#defining the global Variables to be used
HEAD ={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"}
URL_FORM = "https://www.sec.gov/Archives/edgar/data/" 

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

#test case (intel CIK)
urllist = extract10Kurl("0000050863")

#Printing all the urls
print(urllist)