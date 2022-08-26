from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("base_url")

# Make a GET request to fetch the raw HTML content
html_content = requests.get(base_url).text

# Parse the html content
soup = BeautifulSoup(html_content, "lxml")
print(soup.prettify()) # print the parsed data of html
