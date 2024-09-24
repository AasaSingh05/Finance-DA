#importing necessary modules
from requests import get
from bs4 import BeautifulSoup
from SECedgarpyExceptions import ErrorFoundWhileGETRequest, ExtractionError
from SECedgarpyProcessing import HEAD
import pandas as pd

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

#to get all the necessary CIK for the sp500.csv
def CIKExtractor() -> list:
    # List to store CIK numbers
    companyList = []
    
    try:
        # Send a GET request to the page
        response = get(url, timeout=5000, headers=HEAD)

        if (response.status_code == 404):
            raise FileNotFoundError

        elif(response.status_code != 200):
            raise ErrorFoundWhileGETRequest

        else:
            # Parse the page content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the table that contains the S&P 500 company data
            table = soup.find('table', {'id': 'constituents'})

            if table is None:
                raise ValueError

            # Extract each row of the table (excluding the header)
            rows = table.find_all('tr')[1:]  # Skip the header row

            # Loop through each row and get the CIK column (6th column in the table)
            for row in rows:
                # Extract all the cells in the row
                cells = row.find_all('td')
                if len(cells) > 0:
                    # The company name (security) is in the 2nd column (index 1)
                    companyName = cells[1].text.strip()
                    # The CIK number is in the 6th column (index 5)
                    cik = cells[6].text.strip()
                    # Append the tuple (company name, CIK number) to the list
                    companyList.append((companyName, cik))

    except FileNotFoundError as fnf:
        print(fnf)
    except ErrorFoundWhileGETRequest as e:
        print(f"GET request error: {e}")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Returning the list
    return companyList


def GetAllSP500CSV():
    # Read the tables from the Wikipedia page
    try:
        tables = pd.read_html(url)

        # Check if any tables were extracted
        if not tables:
            raise ExtractionError("No tables found on the Wikipedia page.")

        # Extract the table containing the S&P 500 companies data
        sp500_table = tables[0]

        # Save the table to a CSV file
        sp500_table.to_csv("sp500_companies.csv", index=False)
        print("S&P 500 companies data saved to sp500_companies.csv successfully.")

    except ExtractionError as e:
        print(f"Extraction error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")