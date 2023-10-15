import requests
import pandas as pd
import zipfile
import os
import json
import csv

def get_data():
    """
    gets the inflation rate of each country for every year since documenting inflation has started in that country
    """
    folder_url = "https://api.worldbank.org/v2/en/indicator/FP.CPI.TOTL.ZG?downloadformat=csv"
    response = requests.get(folder_url)


    folder_path = 'UVP-project\get_data'
    file_name = 'downloaded_folder.zip'


    directory_path = os.path.join(os.getcwd(), folder_path)


    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


    file_path = os.path.join(directory_path, file_name)


    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)

    # Specifying the path to the downloaded zip file and folder where i want to extract contents
    zip_file_path = "downloaded_folder.zip"
    folder = "UVP-project\get_data"

    extraction_folder = os.path.join(os.getcwd(), folder)

    # Extracting the contents of the zip file
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extraction_folder)


    csv_file_path = os.path.join(extraction_folder, 'API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_5871597.csv')

    with open(csv_file_path, 'r') as csv_reader:
        inflation_csv = csv.reader(csv_reader)
        years = []
        for i, row in enumerate(inflation_csv):
            if i == 4:
                years = row[5:][:-1]
        csv_reader.seek(0)

        # as in other files i want file to develop in data folder
        folder_path = 'UVP-project\data'
        file_name = 'inflation.json'


        directory_path = os.path.join(os.getcwd(), folder_path)


        if not os.path.exists(directory_path):
            os.makedirs(directory_path)


        file_path = os.path.join(directory_path, file_name)

        # making content of the file       
        countries_JSON = {}

        for index, row in enumerate(inflation_csv):
            if index >= 5:
                countries_JSON[row[0]] = {}
                for i in range(len(years)):
                    countries_JSON[row[0]][years[i]] = row[5 + i]
        
        jsonString = json.dumps(countries_JSON)
        with open(file_path, "w") as jsonFile:
            jsonFile.write(jsonString)



get_data()








