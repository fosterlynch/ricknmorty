from dataclasses import dataclass
from realestate import House, Webvalues, TaxRates
from api import fetch_data_with_url

# import matplotlib.pyplot as plt
url = "https://www.redfin.com/WA/Seattle/1221-Minor-Ave-98101/unit-708/home/2078423?600390594=copy_variant&231528114=control&1778901559=variant&utm_nooverride=1"

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
# print("budgeted expenses are: ", house._get_all_expenses())
print("parameters: ", house._webvalues)
print("down payment will be:", house.down_payment)