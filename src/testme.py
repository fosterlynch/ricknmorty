from realestate import House

from api import fetch_data_with_url
from api import RedFin
from taxes import find_tax_rate
import sqlite3
import json


with open("devurls.json", "r") as J:  # noqa: W1514
    urls = json.load(J)

for url in urls:
    # if url == "https://www.redfin.com/AZ/Phoenix/5721-N-41st-Dr-85019/home/28042104":
    if (
        url
        == "https://www.redfin.com/NY/Rochester/476-Alexander-St-14605/home/72474945?600390594"
    ):
        try:
            redfin_webdata = fetch_data_with_url(url)
            print(redfin_webdata)
        except KeyError as err:
            print(url, "key error is ", err)
            pass

## for dev purposes to reduce API calls
# redfin_webdata = RedFin(
#     propertyId="72545602",
#     price=89000,
#     eventDescription="Price Changed",
#     taxInfo={
#         "taxableLandValue": 6500,
#         "taxableImprovementValue": 136400,
#         "rollYear": 2022,
#         "taxesDue": 1747.09,
#     },
#     houseinfo={
#         "beds": 4,
#         "baths": 3.0,
#         "propertyTypeName": "Multi-Family (2-4 Unit)",
#         "numStories": 2.5,
#         "yearBuilt": 1903,
#         "sqFtFinished": 1852,
#         "totalSqFt": 1852,
#         "lotSqFt": 4478,
#         "apn": "261400A12175000010770000000",
#         "propertyLastUpdatedDate": 1686656514952,
#         "displayTimeZone": "US/Eastern",
#     },
#     address=["NY", "Rochester", "195-Henrietta-St-14620"],
#     county="Monroe County",
# )

conn = sqlite3.connect("taxrates.sqlite")
taxrate = find_tax_rate(conn, redfin_webdata)


house = House(
    tax_rate=taxrate,
    list_price=redfin_webdata.price,
    rentroll=[1120, 1200],
    property_type=redfin_webdata.property_type,
    investment_type="pure_investment",
    max_down_payment=45000,
    hoa=0,
)

# house.run_scenarios()
house.analyze()
