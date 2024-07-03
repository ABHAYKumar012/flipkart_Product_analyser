import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.flipkart.com/search?q="

product = input("Enter product: ")

product_name = []
Description = []
price = []
rating = []
try:
    for page in range(1, 6):  # Loop through the first 5 pages
        page_url = url + product + "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=" + str(page)
        r = requests.get(page_url)
        soup = BeautifulSoup(r.text, "html.parser")
        
        box = soup.find("div", class_="DOjaWF gdgoEp")
    
        # Check if box is found
        if box:
            # Extract product names
            proNames = box.find_all("div", class_="KzDlHZ") 
            if proNames:
                for i in proNames:
                    product_name.append(i.text)
            else:
                proNames = box.find_all("a", class_="wjcEIp")  
                for i in proNames:
                    product_name.append(i.text)
    
            # Extract product prices
            proPrice = box.find_all("div", class_="Nx9bqj _4b5DiR")
            if proPrice:
                for i in proPrice:
                    price.append(i.text)
            else:
                proPrice = box.find_all("div", class_="Nx9bqj")
                for i in proPrice:
                    price.append(i.text)
    
            # Extract product descriptions
            proDesc = box.find_all("ul", class_="G4BRas")
            if proDesc:
                for i in proDesc:
                    Description.append(i.text)
            else:
                proDesc = box.find_all("div", class_="NqpwHC")
                for i in proDesc:
                    Description.append(i.text)
    
            # Extract product ratings
            proRate = box.find_all("div", class_="XQDdHH")
            for i in proRate:
                rating.append(i.text)
        else:
            # If box is not found, add placeholders to match the lengths
            product_name.append("N/A")
            price.append("N/A")
            Description.append("N/A")
            rating.append("N/A")
    
    # Ensure all lists are of the same length
    max_length = max(len(product_name), len(Description), len(price), len(rating))
    
    # Fill in the missing values with "N/A" to match lengths
    product_name.extend(["N/A"] * (max_length - len(product_name)))
    Description.extend(["N/A"] * (max_length - len(Description)))
    price.extend(["N/A"] * (max_length - len(price)))
    rating.extend(["N/A"] * (max_length - len(rating)))
    
    # Print lengths to verify
    print(len(product_name))
    print(len(Description))
    print(len(price))
    print(len(rating))
    
    # Create a DataFrame using the scraped data
    df = pd.DataFrame({
        "Product Name": product_name,
        "Price": price,
        "Description": Description,
        "Rating": rating
    })
    # Save the DataFrame to an Excel file
    df.to_excel(f"{product}_data.xlsx", index=False)
    print(f"Data has been saved to {product}_data.xlsx")
except:
    print("No products found for the given search term.")
