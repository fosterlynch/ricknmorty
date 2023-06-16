from realestate import House, HouseValues, Expenses

from api import fetch_data_with_url
from api import RedFin
from taxes import find_tax_rate
import sqlite3
import json


# with open("devurls.json", "r") as J:  # noqa: W1514
#     urls = json.load(J)
# for url in urls:
# redfin_webdata = fetch_data_with_url(urls[0])
# print(redfin_webdata)
redfin_webdata = RedFin(
    propertyId="72545602",
    price=269900,
    eventDescription="Price Changed",
    taxInfo={
        "taxableLandValue": 6500,
        "taxableImprovementValue": 136400,
        "rollYear": 2022,
        "taxesDue": 1747.09,
    },
    houseinfo={
        "beds": 4,
        "baths": 3.0,
        "propertyTypeName": "Multi-Family (2-4 Unit)",
        "numStories": 2.5,
        "yearBuilt": 1903,
        "sqFtFinished": 1852,
        "totalSqFt": 1852,
        "lotSqFt": 4478,
        "apn": "261400A12175000010770000000",
        "propertyLastUpdatedDate": 1686656514952,
        "displayTimeZone": "US/Eastern",
    },
    address=["NY", "Rochester", "195-Henrietta-St-14620"],
    county="Monroe County",
)
conn = sqlite3.connect("taxrates.sqlite")
taxrate = find_tax_rate(conn, redfin_webdata)


house = House(
    list_price=redfin_webdata.price,
    rentroll=[1000, 1000, 1000],
    property_type=redfin_webdata.property_type,
    investment_type="pure_investment",
    max_down_payment=45000,
    tax_rate=taxrate,
    hoa=0,
)

house.run_scenarios()
