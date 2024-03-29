import os
import requests
import logging
from typing import List

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
    # mlsDescription: dict = field(default_factory={})
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
        elif self.property_type == "Multi-Family (2-4 Unit)":
            self.property_type = "multi"


def _get_address_from_url(url: ParseResult) -> List:
    return url.path.split("/")[1:4]


def _get_property_id_from_url(url: ParseResult) -> str:
    return url.path.split("/")[-1]


def _fetch_from_url(propertyId) -> requests.models.Response:
    querystring = {"propertyId": propertyId, "listingId": propertyId}
    logging.debug(f"url querystring is {querystring}")
    response = requests.get(
        get_price_info_url, headers=headers, params=querystring
    )
    return response


def get_price_info(response):
    print(
        response.json()["payload"]["propertyHistoryInfo"]["events"][0].keys()
    )
    payload = response.json()["payload"]["propertyHistoryInfo"]["events"][0]
    logging.debug(f"json response is {payload}")
    price = int(payload["price"])
    # mlsDescription = payload["mlsDescription"]
    eventDescription = payload["eventDescription"]
    return price, eventDescription


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
    try:
        assert response.status_code == 200
    except AssertionError as err:  #
        print(err)
        sys.exit(err)
    price, eventDescription = get_price_info(response)
    houseinfo = get_property_details(response)
    taxInfo = get_taxes(response)
    county = get_county(response)
    if "redfin" in url.netloc:
        return RedFin(
            propertyId=propertyId,
            price=price,
            # mlsDescription=mlsDescription,
            eventDescription=eventDescription,
            taxInfo=taxInfo,
            houseinfo=houseinfo,
            address=address,
            county=county,
            url=url,
        )
