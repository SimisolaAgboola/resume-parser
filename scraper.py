import requests
from bs4 import BeautifulSoup
import csv

# URL of the Wikipedia page containing the list
url = "https://en.wikipedia.org/wiki/List_of_academic_fields"

# Fetch the webpage content
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the element containing the list
    table_elements = soup.find_all("table", class_="multicol")
    list_elements = soup.find_all("div", class_="div-col")

    #Open csv file for writing
    with open("college_majors.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
    
        # Process table elements
        if table_elements:
            for table_element in table_elements:
                # Extract the list items from table elements
                list_items = table_element.find_all("li")
                # Write the list items to a CSV or TXT file
                for item in list_items:
                    writer.writerow([item.text.strip()])

        # Process div elements
        if list_elements:
            for list_element in list_elements:
                # Extract the list items from div elements
                list_items = list_element.find_all("li")
                # Write the list items to a CSV or TXT file
                for item in list_items:
                    writer.writerow([item.text.strip()])
        
        print("List extracted and saved successfully.")
else:
    print("Failed to fetch webpage. Status code:", response.status_code)
