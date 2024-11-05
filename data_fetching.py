import requests
import os
from extract_data import import_prices
from dotenv import load_dotenv
load_dotenv()

# set the working directory to the scripts directory 
os.chdir(os.path.dirname(os.path.abspath(__file__)))

'''
# url
url = os.getenv("url")
params = {
    "api-key": os.getenv("api_key"),
    "format": "json",
    # "offset": 0,
    # "limit": 10,
    "filters[state.keyword]":"",
    "filters[district]":"",
    "filters[market]":"",
    "filters[commodity]":"",
    "filters[variety]":"",
    "filters[grade]":"29/10/2024"
}
headers = {
    "accept": "application/json"
}
'''

def fetch_data():
    list_of_commodities = [
        "soyabean",
        "green-gram-moong-whole",
        "black-gram-urd-beans-whole",
        "sesamum-sesamegingellytil",
        "kabuli-chana-chickpeas-white",
        "wheat",
        "jowar-sorghum"
    ]

    opening_url = os.getenv("opening_url")
    closing_url = os.getenv("closing_url")

    data=[]
    for crops in list_of_commodities:
        url = opening_url + crops + closing_url
        
        # Making a GET request
        # response = requests.get(url, headers=headers, params=params)
        response = requests.get(url)

        # Check if request was successful
        if response.status_code == 200:   
            filename = f"data_file_{crops}.txt"  # Create a unique filename per crop
            with open(filename, 'w') as data_file:
                data_file.write(response.text)  # Write response content to the file

            print("Successful")
            prices = import_prices(crops)
            if(prices is not None):
                data.append(prices)
        else:
            print(f"Request failed with status code {response.text}")

    save = open("./save.txt",'w')
    for items in data:
        save.write(str(items))
        
    save.close()

# strings = "hello"
# len - number
# print(strings[-2:-1])  

# 5-2 = 3 start
# 5-1 = 4 stop
