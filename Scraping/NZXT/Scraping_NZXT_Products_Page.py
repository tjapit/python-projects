# Importing packages
import requests                 # Requesting html page
from openpyxl import Workbook   # Read and write Excel
from bs4 import BeautifulSoup   # Parsing html

# Requesting access to NZXT product page, and storing product names
nzxt_cases_page = 'https://www.nzxt.com/products'
r = requests.get(nzxt_cases_page)   # Requesting access to url
print(r)    # Checking for status code, 200 means good, 40X means error

soup = BeautifulSoup(r.content, 'html.parser')  # Parsing html
product_html = soup.find_all('h3', class_='prod-name')
print(len(product_html))    # Number of products in the page
print(type(product_html))   # type should be <class 'bs4.element.ResultSet'>

product_name = [''] * len(product_html)     # Initializing an array for the product name to be concatenated
for i in range(len(product_html)):          # Looping over the length of the product count from the page (1:52 or 0:51)
    product_name[i] = product_html[i].text  # Storing the text from the Tag of the ResultSet to a var


# Creating an excel file, and writing into it
wb = Workbook()     # Creating a new workbook
file_path = 'F:/Python Projects/NZXT_Products.xlsx'  # Specifying file path and name (NOTE: PATH NAME USE FORWARD SLASH)
sheet = wb.active   # Specifying active Sheet

for i in range(len(product_name)):
    sheet.cell(row=i+1, column=1).value = product_name[i]   # NOTE: Python : 0-indexing
                                                            #       openpyxl: 1-indexing

wb.save(file_path)  # Always save to make the change, otherwise the file won't be created


