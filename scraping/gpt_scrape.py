#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import json

# Send a GET request to the website
# url = "view-source:https://www.carrefour.es/supermercado/crema-de-galletas-crunchy-lotus-biscoff-380-g/R-prod720947/p"
url = "view-source:https://www.carrefour.es"
response = requests.get(url)
# If the GET request is successful, the status code will be 200
if response.status_code == 200:
    # Get the content of the response
    page_content = response.content
    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(page_content, "html.parser")
    # Find all product items on the page
    products = soup.find_all("div", class_="product-item")
    # Create a list to store the product information
    product_info = []
    # Loop through each product item
    for product in products:
        # Find the product name, price, and nutrition facts
        name = product.find("h2", class_="product-name").text.strip()
        price = product.find("span", class_="price").text.strip()
        nutrition_facts = product.find("ul", class_="nutrition-facts")
        # Extract the nutrition facts
        nutrition_info = []
        if nutrition_facts:
            for fact in nutrition_facts.find_all("li"):
                nutrition_info.append(fact.text.strip())
        # Create a dictionary to store the product information
        product_dict = {"name": name, "price": price, "nutrition_facts": nutrition_info}
        # Add the product dictionary to the list
        product_info.append(product_dict)
    # Convert the list to a JSON string
    json_string = json.dumps(product_info, indent=4)
    # Save the JSON string to a file
    with open("carrefour_products.json", "w") as file:
        file.write(json_string)
    print("JSON file created successfully.")
else:
    print("Failed to retrieve the webpage. Status code: ", response.status_code)
