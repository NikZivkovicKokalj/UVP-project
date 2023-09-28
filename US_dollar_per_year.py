import pandas as pd
import requests
import json

def get_data():
    #download text file from url
    text_url = "https://www.federalreserve.gov/paymentsystems/files/coin_calprint.txt"
    response = requests.get(text_url)

    #if requests == 200 the requests has succeded
    if response.status_code == 200:
        data = str(response.content).replace("\\t\\t\\t", "\\t")
        data = data.replace("\\r", "")
        lines = data.split("\\n")[:-1]
        #i will make a dictionary in which i will store {year : {volume : x (in billions), value : y (in billions)}, year2...}
        dollars_JSON = {}
        for index, line in enumerate(lines): 
            if index >= 4:
                words = line.split('\\t')
                dollars_JSON[words[0]] = {}
                dollars_JSON[words[0]]['volume'] = words[1]
                dollars_JSON[words[0]]['value'] = words[2]

        jsonString = json.dumps(dollars_JSON)
        jsonFile = open("US_dollar_per_year.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()