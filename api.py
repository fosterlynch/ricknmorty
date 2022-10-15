import requests
import os
from dotenv import load_dotenv

load_dotenv()
apikey = os.getenv("apikey")
apihost = os.getenv("apihost")
initial_url = os.getenv("initial_url")
address = os.getenv("address")
headers = os.getenv("headers")
get_main_info_url = os.getenv("get_main_info_url")
get_price_info_url = os.getenv("get_price_info_url")

querystring = {"location": address}

headers = {"X-RapidAPI-Key": apikey, "X-RapidAPI-Host": apihost}

# response = requests.request(
#     "GET", initial_url, headers=headers, params=querystring
# )


# propertyId = response.json()["payload"]["exactMatch"]["id"]
# propertyId = propertyId.split("_")[1]

# querystring = {"propertyId": propertyId, "listingId": propertyId}

# # response = requests.request(
# #     "GET", get_main_info_url, headers=headers, params=querystring
# # )

# response = requests.request(
#     "GET", get_price_info_url, headers=headers, params=querystring
# )


# houseinfo = response.json()["payload"]["publicRecordsInfo"]
# priceinfo = response.json()["payload"]["propertyHistoryInfo"]
# print(
#     response.json()["payload"]["propertyHistoryInfo"]["events"][0][
#         "price", "mlsDescription", "eventDescription"
#     ]
# )

from urllib.parse import urlparse

metadata = {"isRedfinUrl": None}


def get_price_from_url(url):
    url = urlparse(url)
    metadata.update({"isRedfinUrl": "redfin" in url.netloc})
    print(url)

get_price_from_url(
    "https://www.redfin.com/NY/Rochester/1064-Lake-Ave-14613/home/92804703"
)
