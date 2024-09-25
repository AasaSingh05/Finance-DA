import os
import pandas as pd
from SECedgarpyExtractor import *
from SECedgarpyProcessing import *
from SECedgarpyDownloading import download_and_convert_filtered_xlsx

# Get current working directory
cwd = os.getcwd()
directory = "SP500 output"

# Creating a path to store all the values
path = os.path.join(cwd, directory)
os.makedirs(path, exist_ok=True)

# Navigating to the new directory
os.chdir(path)

# Extracting the CIK numbers for the SP500 companies
print("Getting all SP500 companies in a csv file")
GetAllSP500CSV()
companies = CIKExtractor()

# Function to convert XLSX to CSV
def xlsx_to_csv(xlsx_file, csv_file):
    try:
        # Specifying the engine manually to handle format issues
        df = pd.read_excel(xlsx_file, engine='openpyxl')
        df.to_csv(csv_file, index=False)
        print(f"Converted {xlsx_file} to {csv_file}")
    except Exception as e:
        print(f"Failed to convert {xlsx_file}: {str(e)}")

# Initialize an empty DataFrame to store data from all companies
all_companies_data = pd.DataFrame()

# Target sheets to extract
target_sheets = ["consolidated statements of income", "consolidated balance sheets"]

# Extracting data from the website and placing it in XLSX files
for company in companies:
    # Setting up a directory for each company to save the info in
    newcomp = company[0]
    newpath = os.path.join(path, newcomp)
    os.makedirs(newpath, exist_ok=True)
    
    # Navigating to the directory
    os.chdir(newpath)
    
    # Extraction of the URLs
    urls = extract10Kurl(company[1])
    xlsx_urls = URLtoXLSX(urls)
    
    # Download and convert XLSX files
    download_and_convert_filtered_xlsx(xlsx_urls, f"{newcomp}_financial_data", target_sheets)
    
    # Read the CSV file and append to the all_companies_data DataFrame
    csv_files = [f for f in os.listdir() if f.endswith('.csv')]
    if csv_files:
        latest_csv = max(csv_files, key=os.path.getctime)
        company_data = pd.read_csv(latest_csv)
        company_data['Company'] = newcomp
        all_companies_data = pd.concat([all_companies_data, company_data], ignore_index=True)
    else:
        print(f"No CSV files found for {newcomp}")
    
    # Navigate back to the main directory
    os.chdir(path)

# Save the combined data to a main XLSX file
main_xlsx = "all_companies_financial_data.xlsx"
all_companies_data.to_excel(main_xlsx, index=False)
print(f"Saved combined data to {main_xlsx}")

# Convert the main XLSX file to CSV
main_csv = "all_companies_financial_data.csv"
xlsx_to_csv(main_xlsx, main_csv)

print("Data extraction and compilation complete.")
