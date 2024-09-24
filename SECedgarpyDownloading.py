#importing necessary modules
from requests import get
from SECedgarpyExceptions import ErrorFoundWhileGETRequest
from SECedgarpyProcessing import HEAD
import pandas as pd
import os

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

# Define the XLSX file path
xlsx_file_path = 'input.xlsx'

# Target sheet names (in lowercase and with spaces)
target_sheets = ["consolidated statements of income", "consolidated balance sheets"]

# Load the Excel file and extract sheet names
xlsx_file = pd.ExcelFile(xlsx_file_path)
all_sheet_names = xlsx_file.sheet_names

# Convert sheet names to lowercase and replace "_" with " " for comparison
formatted_sheet_names = [sheet_name.lower().replace("_", " ") for sheet_name in all_sheet_names]

# Initialize an empty list to hold dataframes of the matched sheets
sheets_to_merge = []

# Loop through each formatted sheet name and match with target list
for original_sheet, formatted_sheet in zip(all_sheet_names, formatted_sheet_names):
    if formatted_sheet in target_sheets:
        # Parse the matching sheet and append to the list
        sheet = xlsx_file.parse(original_sheet)
        sheets_to_merge.append(sheet)
        print(f'Sheet {original_sheet} matched and added for merging')

# Concatenate all matched sheets if there are any matches
if sheets_to_merge:
    merged_sheets = pd.concat(sheets_to_merge, ignore_index=True)
    
    # Derive the CSV filename from the XLSX file name
    csv_file_name = os.path.splitext(os.path.basename(xlsx_file_path))[0] + '.csv'
    
    # Save the merged sheets to a single CSV file
    merged_sheets.to_csv(csv_file_name, index=False)
    
    print(f'Matched sheets have been saved to {csv_file_name}')
else:
    print("No matching sheets found.")

