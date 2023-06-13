from realestate import House, Webvalues

from api import fetch_data_with_url
from api import RedFin
from taxes import find_tax_rate
import sqlite3
import json


def calculate_annual_property_taxes(
    assessed_value: float, tax_rate: float
) -> float:
    return assessed_value * 0.6 * tax_rate


with open("devurls.json", "r") as J:  # noqa: W1514
    urls = json.load(J)

for url in urls:
    redfin_webdata = fetch_data_with_url(url)

    conn = sqlite3.connect("taxrates.sqlite")
    taxrate = find_tax_rate(conn, redfin_webdata)

    annual_taxes = calculate_annual_property_taxes(
        redfin_webdata.price, taxrate
    )

    webvalues = Webvalues(  # why pass it into another dataclass?
        list_price=redfin_webdata.price,
        property_type=redfin_webdata.property_type,
        investment_type="pure_investment",
        max_down_payment=45000,
        rentroll=[0],
        insurance=53,
        taxes=annual_taxes / 12,
        hoa=0,
        interest_rate=0.07,
    )

    house = House(webvalues=webvalues)
    house.analyze()
