# Scraping Jumia Website - Using BeautifulSoup

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 16:18:22 2023

@author: folashade.ayorinde-akinola
"""
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

products = []   # List to store names of the products
prices = []     # List to store prices of the products
ratings = []    # List to store ratings of the products

url = "https://www.jumia.com.ng/mlp-stay-connected-deals/smartphones/"
all_urls = []

for page in range(1,50):
    next_urls = url + "?page=" + str(page)
    all_urls.append(next_urls)
    
for url in all_urls:
    soup = requests.get(url)
    soup = BeautifulSoup(soup.content, 'html.parser')
    #print(soup)

    scrape = soup.find_all(class_ = "name")
    #print(scrape)

    name = soup.find('div', class_="name")
    price = soup.find('div', class_="prc")
    rate = soup.find('div', class_="stars _s")

    
    for name in scrape:
        if name != None:    # Caters for instances where the name does not exist
            products.append(name.text.strip())
            #print(products)
        else:
            break # Get the text part
      
        if price != None:
            prices.append(price.text.strip())
            #print(prices)
        else:
            break
            
        if rate != None:    # Caters for instances where the rating does not exist - which was causing an error initially
            ratings.append(rate.text.strip())
            #print(ratings)
        else:
            break

    cleaned_products = [data.replace("\n", "") for data in products]
    #print(cleaned_products)
    cleaned_prices = [data.replace("\n", "") for data in prices]
    #print(cleaned_prices)
    cleaned_ratings = [data.replace("\n", "") for data in ratings]
    #print(cleaned_ratings)

    # Structuring and storing data
    #a = {'Product Name': products, 'Price': prices, 'Rating': ratings}
    a = {'Product Name': cleaned_products, 'Price': cleaned_prices, 'Rating': cleaned_ratings}
    df = pd.DataFrame.from_dict(a, orient='index')
    df = df.transpose()
    #print(df)

    # Output the DataFrame to CSV file
    df.to_csv('Assignment.csv', index = False)

    # Data Visualization
    df2 = pd.read_csv("Assignment.csv")

    plt.xlabel("Rating")
    plt.ylabel("Price")
    plt.title("Rating against Price")

    plt.scatter(df2.Rating, df2.Price, marker="*", c = 'purple', alpha = 1)    # Line graph - The labels above apply for this plot only
    #marker: format can be o or * , c: color, alpha: opacity(Range: 0-1)
    plt.show()
