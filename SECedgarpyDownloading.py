#importing necessary modules
from requests import get
from SECedgarpyExceptions import ErrorFoundWhileGETRequest
from SECedgarpyProcessing import HEAD
import pandas as pd

#function to download the XLSX file from the lists

def getCSVfile(URLlist: list[str], nameOfFile: str) -> None:
    
    # iterating through every URL in the list
    counter = 0
    for urlelt in URLlist:
        
        # perform HTTP GET request to download the XLSX file
        urlresp = get(urlelt, timeout=5000, headers=HEAD)
        
        # check the status code for the response
        statcode = urlresp.status_code
        
        # handle 404 errors (file not found)
        if statcode == 404:
            print(f"File not found at {urlelt}. Skipping...")
            continue  # Skip this URL and move to the next one
        
        # handle other errors (anything other than 200 or 404)
        elif statcode != 200:
            raise ErrorFoundWhileGETRequest
        
        # if request is successful, save the file
        else:
            # increment the counter for unique file names
            counter += 1
            
            # create the final file name with the counter and .xlsx extension
            FinalNameXLSX = f"{nameOfFile}_{counter}.xlsx"
            FinalNameCSV = f"{nameOfFile}_{counter}.csv"
            
            # open the file in binary write mode and write the content
            with open(FinalNameXLSX, "wb") as f:
                f.write(urlresp.content)
            
            print(f"Downloaded file: {FinalNameXLSX}")
            
            # Convert XLSX to CSV
            try:
                # read the XLSX file
                excel_data = pd.read_excel(FinalNameXLSX)
                
                # save the content as CSV
                excel_data.to_csv(FinalNameCSV, index=False)
                print(f"Converted {FinalNameXLSX} to {FinalNameCSV}")
            
            except Exception as e:
                print(f"Failed to convert {FinalNameXLSX} to CSV: {e}")


def getXLSXfile(URLlist: list[str], nameOfFile: str) -> None:
    
    # iterating through every URL in the list
    counter = 0
    for urlelt in URLlist:
        
        # perform HTTP GET request to download the XLSX file
        urlresp = get(urlelt, timeout=5000, headers=HEAD)
        
        # check the status code for the response
        statcode = urlresp.status_code
        
        # handle 404 errors (file not found)
        if statcode == 404:
            print(f"File not found at {urlelt}. Skipping...")
            continue  # Skip this URL and move to the next one
        
        # handle other errors (anything other than 200 or 404)
        elif statcode != 200:
            raise ErrorFoundWhileGETRequest
        
        # if request is successful, save the file
        else:
            # increment the counter for unique file names
            counter += 1
            
            # create the final file name with the counter and .xlsx extension
            FinalNameXLSX = f"{nameOfFile}_{counter}.xlsx"
            FinalNameCSV = f"{nameOfFile}_{counter}.csv"
            
            # open the file in binary write mode and write the content
            with open(FinalNameXLSX, "wb") as f:
                f.write(urlresp.content)
            
            print(f"Downloaded file: {FinalNameXLSX}")
            
            # Convert XLSX to CSV
            try:
                # read the XLSX file
                excel_data = pd.read_excel(FinalNameXLSX)

                # save the content as CSV
                excel_data.to_csv(FinalNameCSV, index=False)
                print(f"Converted {FinalNameXLSX} to {FinalNameCSV}")
            
            except Exception as e:
                print(f"Failed to convert {FinalNameXLSX} to CSV: {e}")


#to generate the CSV report by filtering and keeping the necessary sheets only

def GenerateCSVreport(nameOfFile):
    
    
    # < ---currently placeholders--- >     
    
    #to read the contents of the XLSX file
    data = pd.read_excel(nameOfFile)
    
    #heading of the sheet which act as the filter of which sheets to keep
    sheetheadings = []
    
    
    print()
