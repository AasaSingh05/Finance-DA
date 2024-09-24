from SECedgarpyExtractor import *
from SECedgarpyProcessing import *
from SECedgarpyDownloading import *


#Extracting the CIK numbers for the first 500 companies on the NYSE

print("Getting all sp500 companies in a csv file")
GetAllSP500CSV()
companies = CIKExtractor()

#Extracting data from the website and placing it in a XLSX file
urls = []
for company in companies:
    data = extract10Kurl(company[1])
    urls.append(data)
    
print("Data extracted")

# fileURL = URLtoXLSX(urls)

# ReqList = []

# for subzip in list(zip()):    
    

# #Converting the XLSX file to  CSV file
# # GenerateCSVreport(getXLSXfile(fileURL))
# print("Required CSV file in #location")