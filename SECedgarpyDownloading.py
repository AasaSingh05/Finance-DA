#importing necessary modules
from requests import get
from SECedgarpyExceptions import ErrorFoundWhileGETRequest
from SECedgarpyProcessing import HEAD

#function to download the XLSX file from the lists
def getXLSXfile(URLlist: list[str], nameOfFile: str) -> None:
    
    #iterating through every url we have
    for urlelt in URLlist:
        
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
URLlist = extract10Kurl("0000050863")

#Printing all the urls
URLtoXLSX(URLlist)
'''