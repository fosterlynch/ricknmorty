from realestate import House, Webvalues

# import matplotlib.pyplot as plt

list_price = 318000
property_type = "multi"
taxes = 400
insurance = 53
hoa_fees = 0
rentroll = [0, 0]
investment_type = "house_hack"
# sqft = 1500
# address = "123 main street, rochester, NY 14607"
my_monthly_buget = 1200
interest_rate = 0.07

webvalues = Webvalues(
    list_price=list_price,
    property_type=property_type,
    investment_type=investment_type,
    rentroll=rentroll,
    insurance=insurance,
    taxes=taxes,
    hoa=hoa_fees,
    interest_rate=interest_rate,
)

house = House(webvalues=webvalues)
print("numbers are :", house.analyze())
