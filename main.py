from SECedgarpyExtractor import *
from SECedgarpyProcessing import *
from SECedgarpyDownloading import *
import os

#get current working directory
cwd = os.getcwd()
directory = "SP500 output"

#creating a path to store all the values
path = os.path.join(cwd,directory)
os.mkdir(path)

#navigating to the new directory
os.chdir(path)

#Extracting the CIK numbers for the first 500 companies on the NYSE
print("Getting all sp500 companies in a csv file")
GetAllSP500CSV()
companies = CIKExtractor()

#Extracting data from the website and placing it in a XLSX file
urls = []
for company in companies:
    
    #setting up a directory for each company to save the info in
    newdir = path
    newcomp = company[0]
    
    #creates a new path for every company for the files to be saved in
    newpath = os.path.join(newdir,newcomp)
    os.mkdir(newpath)
    
    #navigating to the directory
    os.chdir(newpath)
    
    #Extraction of the urls
    data = extract10Kurl(company[1])
    urls.append(data)
    