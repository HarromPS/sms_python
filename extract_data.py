from bs4 import BeautifulSoup
import ast
import re

# read the HTML data file
def import_prices(crop):
    html_content = open(f"data_file_{crop}.txt",'r')
    # parse HTML
    soup = BeautifulSoup(html_content, "lxml")

    # finding our data 
    market_price_summary = soup.find("div", class_="mandi_highlight")
    if market_price_summary:
        price_type=[crop]
        for items in market_price_summary.findAll("h4"):
            price_type.append(str(items.text))

        price=[]
        for items in market_price_summary.findAll("p"):
            price.append(str(items.text))

        res=list(zip(price_type,price))
        return res


# Function to extract tuples from the content
def extract_tuples(content):
    # Use regex to find all tuples in the content
    pattern = r"\((.*?)\)"
    matches = re.findall(pattern, content)

    # Convert matches into tuples
    tuples = []
    for match in matches:
        try:
            # Safely evaluate each match as a tuple
            tuples.append(ast.literal_eval(f"({match})"))
        except Exception as e:
            print(f"Error evaluating tuple: {e}")

    return tuples


def extract_data():

    # Read the content of the file
    try:
        with open("./save.txt", "r") as f:
            content = f.read()  # Read the entire file content as a string

        # Extract tuples from the content
        data_list = extract_tuples(content)

        # Print the output
        # print(data_list)
        return data_list

    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")