#importing necessary modules
from requests import get
from bs4 import BeautifulSoup
from SECedgarpyExceptions import ErrorFoundWhileGETRequest
from SECedgarpyProcessing import HEAD

#to get all the necessary CIK for the sp500.csv
def CIKExtractor():
    # URL of the Wikipedia page
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
    # Send a GET request to the page
    response = get(url ,timeout=5000 ,headers = HEAD)
    
    if(response.status_code == 404):
        raise FileNotFoundError

    elif(response.status_code != 200):
        raise ErrorFoundWhileGETRequest
    
    else:
        #Parse the page content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table that contains the S&P 500 company data
        table = soup.find('table', {'id': 'constituents'})

        # List to store CIK numbers
        cik_numbers = []

        # Extract each row of the table (excluding the header)
        rows = table.find_all('tr')[1:]  # Skip the header row

        # Loop through each row and get the CIK column (6th column in the table)
        for row in rows:
            # Extract all the cells in the row
            cells = row.find_all('td')
            if len(cells) > 0:
                # The CIK number is in the 6th column (index 5)
                cik = cells[6].text.strip()
                cik_numbers.append(cik)

    #returning the list
    return cik_numbers