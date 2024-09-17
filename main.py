from SECedgarpyExtractor import CIKExtractor
import SECedgarpyProcessing 
import SECedgarpyDownloading 


#Extracting the CIK numbers for the first 500 companies on the NYSE
companies = CIKExtractor()
print("Extracted first 500 companies on the NYSE")

#Extracting data from the website and placing it in a XLSX file
data = SECedgarpyProcessing(companies)
print("Data extracted")

#Converting the XLSX file to  CSV file
SECedgarpyDownloading(data)
print("Required CSV file in #location")