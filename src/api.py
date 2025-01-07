import os
import requests
import logging
from typing import List
import sys
from dataclasses import dataclass, field
from dotenv import load_dotenv
from urllib.parse import urlparse, ParseResult

load_dotenv()
apikey = os.getenv("apikey")
apihost = os.getenv("apihost")
initial_url = os.getenv("initial_url")
get_main_info_url = os.getenv("get_main_info_url")
get_price_info_url = os.getenv("get_price_info_url")

headers = {"X-RapidAPI-Key": apikey, "X-RapidAPI-Host": apihost}
assert get_main_info_url is not None
assert get_price_info_url is not None


@dataclass
class RedFin:
    propertyId: str = field(default_factory=str)
    price: int = field(default_factory=str)
    eventDescription: dict = field(default_factory={})
    taxInfo: dict = field(default_factory={})
    houseinfo: dict = field(default_factory={})
    address: List = field(default_factory=[])
    county: str = field(default_factory=str)
    url: str = field(default_factory=str)

    def __post_init__(self):
        self.property_type = self.houseinfo["propertyTypeName"]
        if self.property_type == "Single Family Residential":
            self.property_type = "single"
        elif "Multi-Family" in self.property_type:
            self.property_type = "multi"


def _get_address_from_url(url: ParseResult) -> List:
    return url.path.split("/")[1:4]


def _get_property_id_from_url(url: ParseResult) -> str:
    return url.path.split("/")[-1]


def _fetch_from_url(propertyId) -> requests.models.Response:
    querystring = {"propertyId": propertyId, "listingId": propertyId}
    logging.debug(f"url querystring is {querystring}")
    response = requests.get(get_price_info_url, headers=headers, params=querystring)
    return response


def get_price_info(response):
    # print(response.json()["payload"]["propertyHistoryInfo"]["events"][0].keys())
    payload = response.json()["payload"]["propertyHistoryInfo"]["events"][0]
    price = int(payload["price"])
    return price


def get_event_description(response):
    payload = response.json()["payload"]["propertyHistoryInfo"]["events"][0]
    eventDescription = payload["eventDescription"]
    return eventDescription


def get_property_details(response) -> dict:
    houseinfo = response.json()["payload"]["publicRecordsInfo"]["basicInfo"]
    return houseinfo


def get_county(response):
    county = response.json()["payload"]["publicRecordsInfo"]["countyName"]
    return county


def get_taxes(response) -> dict:
    taxes = response.json()["payload"]["publicRecordsInfo"]["taxInfo"]
    return taxes


def fetch_data_with_url(url: str) -> RedFin:
    url = urlparse(url)
    address = _get_address_from_url(url)
    propertyId = _get_property_id_from_url(url)
    response = _fetch_from_url(propertyId)
    print(f"response {response}")
    try:
        assert response.status_code == 200
    except AssertionError as err:  #
        print(err)
        sys.exit(err)
    eventDescription = get_event_description(response)

    if eventDescription == "Contingent":
        price = 0
    else:
        price = get_price_info(response)
    houseinfo = get_property_details(response)
    taxInfo = get_taxes(response)
    county = get_county(response)
    if "redfin" in url.netloc:
        return RedFin(
            propertyId=propertyId,
            price=price,
            eventDescription=eventDescription,
            taxInfo=taxInfo,
            houseinfo=houseinfo,
            address=address,
            county=county,
            url=url,
        )
