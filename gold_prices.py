import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def get_data():
    """
    gets the price of gold for...
    """
    url = 'https://www.macrotrends.net/1333/historical-gold-prices-100-year-chart'
    response = requests.get(url, headers= {'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table with the correct identifier (inspect the HTML source code)
    table = soup.find('table', {'class': 'table'})

    table_data = []

    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all(['th', 'td']):
            row_data.append(cell.text.strip())
        table_data.append(row_data)


    #0th element is table name 1st element are column names 2nd and forward elements are data
    df = pd.DataFrame(table_data[2:], columns=table_data[1])
    df.to_csv('table_data.csv', index=False)

    gold_prices_JSON = {}
    for index, row in enumerate(table_data):
        if index > 2:
            gold_prices_JSON[row[0]] = {}
            gold_prices_JSON[row[0]]['Average closing price'] = row[1]
            gold_prices_JSON[row[0]]['Annual percentage change'] = row[6]

    jsonString = json.dumps(gold_prices_JSON)
    jsonFile = open("gold_prices.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()
        
#all prices are for ounce of gold



