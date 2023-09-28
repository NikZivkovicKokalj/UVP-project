import requests
import pandas as pd
import zipfile
import os
import json
import csv

def get_data():
    folder_url = "https://api.worldbank.org/v2/en/indicator/FP.CPI.TOTL.ZG?downloadformat=csv"
    response = requests.get(folder_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        with open("downloaded_folder.zip", "wb") as file:
            file.write(response.content)

    # Specify the path to the downloaded zip file
    zip_file_path = "downloaded_folder.zip"

    # Specify the folder where you want to extract the contents
    extraction_folder = os.getcwd()

    # Extract the contents of the zip file
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extraction_folder)

    with open('API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_5795712.csv', 'r') as csv_reader:
        inflation_csv = csv.reader(csv_reader)
        years = []
        for i, row in enumerate(inflation_csv):
            if i == 4:
                years = row[5:][:-1]
        csv_reader.seek(0)
        
        countries_JSON = {}

        for index, row in enumerate(inflation_csv):
            if index >= 5:
                countries_JSON[row[0]] = {}
                for i in range(len(years)):
                    countries_JSON[row[0]][years[i]] = row[5 + i]
        
        jsonString = json.dumps(countries_JSON)
        jsonFile = open("inflation.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()





