from SECedgarpyExtractor import CIKExtractor
from SECedgarpyProcessing import extract10Kurl, URLtoXLSX
from SECedgarpyDownloading import getXLSXfile, GenerateCSVreport


#Extracting the CIK numbers for the first 500 companies on the NYSE
companies = CIKExtractor()
print("Extracted first 500 companies on the NYSE")

#Extracting data from the website and placing it in a XLSX file
urls = list()
for company in companies:
    data = extract10Kurl(company)
    urls.append(data)
    
    
print("Data extracted")

fileURL = URLtoXLSX(urls)

#Converting the XLSX file to  CSV file
# GenerateCSVreport(getXLSXfile(fileURL))
print("Required CSV file in #location")