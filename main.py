import os
from SECedgarpyExtractor import *
from SECedgarpyProcessing import *
from SECedgarpyDownloading import *
import pandas as pd

def main():
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

    # Initialize an empty DataFrame to store data from all companies
    all_companies_data = pd.DataFrame()

    # Target sheets to extract
    target_sheets = ["consolidated statements of income", "consolidated balance sheets"]

    # Extracting data from the website and placing it in XLSX files
    for company_name, cik in companies:
        # Setting up a directory for each company to save the info in
        company_dir = os.path.join(path, company_name)
        os.makedirs(company_dir, exist_ok=True)
        
        # Navigating to the company directory
        os.chdir(company_dir)
        
        # Extraction of the URLs
        urls = extract10Kurl(cik)
        xlsx_urls = URLtoXLSX(urls)
        
        # Download and convert XLSX files
        download_and_convert_filtered_xlsx(xlsx_urls, f"{company_name}_financial_data", target_sheets)
        
        # Read the CSV file and append to the all_companies_data DataFrame
        csv_files = [f for f in os.listdir() if f.endswith('.csv')]
        if csv_files:
            latest_csv = max(csv_files, key=os.path.getctime)
            company_data = pd.read_csv(latest_csv)
            company_data['Company'] = company_name
            all_companies_data = pd.concat([all_companies_data, company_data], ignore_index=True)
        else:
            print(f"No CSV files found for {company_name}")
        
        # Navigate back to the main directory
        os.chdir(path)

    # Save the combined data to a main XLSX file
    main_xlsx = "all_companies_financial_data.xlsx"
    all_companies_data.to_excel(main_xlsx, index=False)
    print(f"Saved combined data to {main_xlsx}")

    # Convert the main XLSX file to CSV
    main_csv = "all_companies_financial_data.csv"
    all_companies_data.to_csv(main_csv, index=False)
    print(f"Converted combined data to {main_csv}")

    print("Data extraction and compilation complete.")

if __name__ == "__main__":
    main()