from dataclasses import dataclass
from realestate import House, Webvalues, TaxRates
from api import fetch_data_with_url
from api import RedFin



# url = (
#     "https://www.redfin.com/NY/Rochester/187-Wisconsin-St-14609/home/92816944"
# )
# redfin_webdata = fetch_data_with_url(url)
# print(redfin_webdata)

#  get price information -> ```fetch_data_with url````
# just so i dont have to keep grabbing data off the vpn i've verified its grabbing info fine for now
RedFin(
    propertyId="92816944",
    price=149900,
    mlsDescription="Active",
    eventDescription="Listed",
    taxInfo={
        "taxableLandValue": 5900,
        "taxableImprovementValue": 95100,
        "rollYear": 2022,
        "taxesDue": 1251.78,
    },
    houseinfo={
        "beds": 4,
        "baths": 2.0,
        "propertyTypeName": "Multi-Family (2-4 Unit)",
        "numStories": 1.7,
        "yearBuilt": 1925,
        "sqFtFinished": 1275,
        "totalSqFt": 1275,
        "lotSqFt": 4640,
        "apn": "261400A10772000030110000000",
        "propertyLastUpdatedDate": 1683333557722,
        "displayTimeZone": "US/Eastern",
    },
    address=["NY", "Rochester", "187-Wisconsin-St-14609"],
    county="Monroe",
)

def get_tax_rate(RedFin):


# print(response.json())
# webvalues = Webvalues(  # why pass it into another dataclass?
#     list_price=webdata.price,
#     property_type=webdata.property_type,
#     investment_type="house_hack",
#     rentroll=[0],
#     insurance=53,
#     taxes=(webdata.price * 0.4 * webdata.taxrate) / 12,
#     hoa=0,
#     interest_rate=0.07,
# )

# house = House(webvalues=webvalues)
# print("cashflow is :", house.cashflow())
# print("monthly taxes will be", house.taxes)
# print("loan amount is: ", house.monthly_payment)
# # print("budgeted expenses are: ", house._get_all_expenses())
# print("parameters: ", house._webvalues)
# print("down payment will be:", house.down_payment)
