import os
import sys
import requests
from typing import List

from dotenv import load_dotenv
from urllib.parse import urlparse, ParseResult

load_dotenv()
apikey = os.getenv("apikey")
apihost = os.getenv("apihost")
initial_url = os.getenv("initial_url")
address = os.getenv("address")
headers = os.getenv("headers")
get_main_info_url = os.getenv("get_main_info_url")
get_price_info_url = os.getenv("get_price_info_url")


headers = {"X-RapidAPI-Key": apikey, "X-RapidAPI-Host": apihost}

# def lookup_properties_by_address(address):

#     querystring = {"location": address}

#     response = requests.request(
#         "GET", initial_url, headers=headers, params=querystring
#     )

#     propertyId = response.json()["payload"]["exactMatch"]["id"]
#     propertyId = propertyId.split("_")[1]

#     querystring = {"propertyId": propertyId, "listingId": propertyId}

#     response = requests.request(
#         "GET", get_main_info_url, headers=headers, params=querystring
#     )
#     return response.json()["payload"]


def _get_address_from_url(url: ParseResult) -> List:
    return url.path.split("/")[1:4]


def _get_property_id_from_url(url: ParseResult) -> str:
    return url.path.split("/")[-1]


def _fetch_from_url(propertyId) -> requests.models.Response:
    querystring = {"propertyId": propertyId, "listingId": propertyId}
    response = requests.request(
        "GET", get_price_info_url, headers=headers, params=querystring
    )
    print(type(response))
    return response


def get_price_info(response):
    payload = response.json()["payload"]["propertyHistoryInfo"]["events"][0]
    price = payload["price"]
    mlsDescription = payload["mlsDescription"]
    eventDescription = payload["eventDescription"]
    return price, mlsDescription, eventDescription


def get_property_details(response) -> dict:
    houseinfo = response.json()["payload"]["publicRecordsInfo"]["basicInfo"]
    return houseinfo


def get_taxes(response) -> dict:
    taxes = response.json()["payload"]["publicRecordsInfo"]["taxInfo"]
    return taxes


def fetch_data_with_url(url: str) -> dict:
    url = urlparse(url)
    assert "redfin" in url.netloc  # supporting only redfin for now
    metadata = {}
    address = _get_address_from_url(url)
    propertyId = _get_property_id_from_url(url)
    response = _fetch_from_url(propertyId)
    try:
        assert response.status_code == 200
    except AssertionError as err:
        sys.exit(err)
    price, mlsDescription, eventDescription = get_price_info(response)
    houseinfo = get_property_details(response)
    taxInfo = get_taxes(response)
    metadata.update(
        {
            "isRedfinUrl": "redfin" in url.netloc,
            "address": address,
            "propertyId": propertyId,
            "price": price,
            "mlsDescription": mlsDescription,
            "eventDescription": eventDescription,
            "taxInfo": taxInfo,
            "houseinfo": houseinfo,
        }
    )
    return metadata
