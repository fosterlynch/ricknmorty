from dataclasses import dataclass
from realestate import House, Webvalues, TaxRates
from api import fetch_data_with_url

# import matplotlib.pyplot as plt
url = "https://www.redfin.com/NY/Rochester/1064-Lake-Ave-14613/home/92804703"

webdata = fetch_data_with_url(url)


webvalues = Webvalues(
    list_price=webdata.price,
    property_type=webdata.property_type,
    investment_type="house_hack",
    rentroll=[0],
    insurance=53,
    taxes=(webdata.price * 0.4 * webdata.taxrate) / 12,
    hoa=0,
    interest_rate=0.07,
)

house = House(webvalues=webvalues)
print("cashflow is :", house.cashflow())
print("monthly taxes will be", house.taxes)
print("loan amount is: ", house.monthly_payment)
print("budgeted expenses are: ", house._get_all_expenses())
print("parameters: ", house._webvalues)
print("down payment will be:", house.down_payment)