import os
import requests
import schedule
import time
# from twilio.rest import Client
from data_fetching import fetch_data
from extract_data import extract_data
from dotenv import load_dotenv
load_dotenv()


def send_sms(message):
    # your API secret from (Tools -> API Keys) page
    apiSecret = os.getenv("api_key")

    message = {
        "secret": apiSecret,
        "mode": "devices",
        "device": os.getenv("device"),
        "sim": 1,
        "priority": 1,
        "phone": os.getenv("recipient_number"),
        "message": message
    }

    r = requests.post(url = os.getenv("url"), params = message)
    
    # do something with response object
    result = r.json()
    if(result["status"]==200):
        print("Sent")
    else:
        print("Error")


def getMessage(data):
    # Initialize lists to hold prices
    crop = []
    average_prices = []
    lowest_prices = []
    costliest_prices = []

    # Iterate through the data to extract prices
    for i in range(len(data)):
        if data[i][0] == 'Average Price':
            average_prices.append(data[i][1])
        elif data[i][0] == 'Lowest Market Price':
            lowest_prices.append(data[i][1])
        elif data[i][0] == 'Costliest Market Price':
            costliest_prices.append(data[i][1])
        else:
            crop.append(data[i][0])

    # Prepare message output for up to 7 items
    message_lines = []
    num_items = min(7, len(average_prices))  # Ensure we don't exceed available items

    for i in range(num_items):
        message_lines.append(
            f"{crop[i]}:\n"
            f"Average Price: {average_prices[i]}\n"
            f"Lowest Market Price: {lowest_prices[i]}\n"
            f"Costliest Market Price: {costliest_prices[i]}\n"
        )

    # Join the messages into a single string
    final_message = "\n".join(message_lines)

    # Print or send the message
    # print(final_message)
    return final_message




def job():
    # get all the data first 
    fetch_data()

    # filter data to be send 
    data = extract_data()

    # extract the message from the data 
    message = getMessage(data)

    # send the sms 
    send_sms(message)

# Schedule job weekly
schedule.every().week.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)