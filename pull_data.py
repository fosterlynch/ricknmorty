from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import pprint

load_dotenv()
base_url = os.getenv("base_url")

print("starting data pulls...")
print("------------------------------------------------------------------------------------------------")
# Make a GET request to fetch the raw HTML content
html_content = requests.get(base_url).text

# Parse the html content
soup = BeautifulSoup(html_content, "lxml")
print(soup.title.text) # print the parsed data of html

# title=ToPropertyData

script = soup.findAll('script')
print(pprint.pprint(script))

for link in soup.find_all('a'):
   print(link.get('href'))


# session = requests.Session()
# r = session.get(base_url)
# soup = BeautifulSoup(r.content, "lxml")

# keys = soup.find("input",{"id":"_ctl0_m_hfKeys"})["value"]
# did = session.cookies.get_dict()["Display"]

# soup = BeautifulSoup(r.content, "lxml")

# items = []

# for i in soup.find_all("div",{"class":"multiLineDisplay"}):
#   span = i.find_all("span")
#   item = {
#     "image": span[0].find("img")["src"],
#     "price": span[1].text,
#     "status1": span[4].text,
#     "status2": span[5].text,
#     "address1": span[6].text,
#     "address2": span[7].text,
#     "bedroomNum": span[8].text,
#     "FullBathroomNum": span[10].text,
#     "HalfBathroomNum": span[12].text,
#     "sqft": span[14].text,
#   }
#   if (len(span)>20):
#     item["builtIn"] = span[17].text
#     item["acres"] = span[18].text
#     item["family"] = span[20].text
#     item["description"] = span[21].text
#   elif (len(span)>19):
#     item["builtIn"] = span[17].text
#     item["family"] = span[18].text
#     item["description"] = span[19].text
#   else:
#     item["family"] = span[15].text
#     item["description"] = span[16].text
#   items.append(item)

# print(pprint.pprint(items))
# print(len(items))
