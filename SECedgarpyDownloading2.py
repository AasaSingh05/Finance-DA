import os
import pandas as pd
from requests import get
from SECedgarpyExceptions import ErrorFoundWhileGETRequest
from SECedgarpyProcessing import HEAD

# Unified function for downloading XLSX, filtering sheets, and converting to CSV
def download_and_convert_filtered_xlsx(URLlist: list[str], nameOfFile: str, target_sheets: list[str]) -> None:
    counter = 0
    for urlelt in URLlist:
        try:
            # Perform HTTP GET request
            urlresp = get(urlelt, timeout=5000, headers=HEAD)
            if urlresp.status_code == 404:
                print(f"File not found at {urlelt}. Skipping...")
                continue
            elif urlresp.status_code != 200:
                raise ErrorFoundWhileGETRequest

            # Increment counter and save the XLSX file
            counter += 1
            FinalNameXLSX = f"{nameOfFile}_{counter}.xlsx"
            with open(FinalNameXLSX, "wb") as f:
                f.write(urlresp.content)
            print(f"Downloaded file: {FinalNameXLSX}")
            
            # Convert to CSV but only for the filtered sheets
            FinalNameCSV = f"{nameOfFile}_{counter}.csv"
            filter_and_convert_to_csv(FinalNameXLSX, FinalNameCSV, target_sheets)

        except Exception as e:
            print(f"Failed to download or process {urlelt}: {e}")

# Function to filter relevant sheets and convert them to CSV
def filter_and_convert_to_csv(xlsx_file_path: str, csv_file_path: str, target_sheets: list[str]) -> None:
    try:
        # Load the Excel file and extract sheet names
        xlsx_file = pd.ExcelFile(xlsx_file_path)
        all_sheet_names = xlsx_file.sheet_names
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

        # If there are matched sheets, concatenate and save to CSV
        if sheets_to_merge:
            merged_sheets = pd.concat(sheets_to_merge, ignore_index=True)
            merged_sheets.to_csv(csv_file_path, index=False)
            print(f"Filtered sheets saved to {csv_file_path}")
        else:
            print("No matching sheets found.")

    except Exception as e:
        print(f"Failed to process and convert {xlsx_file_path}: {e}")
