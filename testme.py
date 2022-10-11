from realestate import House, Webvalues

# import matplotlib.pyplot as plt

list_price = 318000
property_type = "multi"
taxes = 400
insurance = 53
hoa_fees = 0
rentroll = [800, 0]
investment_type = "house_hack"
# sqft = 1500
# address = "123 main street, rochester, NY 14607"


webvalues = Webvalues(
    list_price=list_price,
    property_type=property_type,
    investment_type=investment_type,
    rentroll=rentroll,
    insurance=insurance,
    taxes=taxes,
    hoa=hoa_fees,
)

house = House(webvalues=webvalues)
house.run_scenarios()