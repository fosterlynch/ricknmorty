from realestate import RealEstate, webvalues

# import matplotlib.pyplot as plt

list_price = 200000
property_type = "multi"
taxes = 537
insurance = 53
hoa_fees = 0
rentroll = [800, 800]
investment_type = "house_hack"
# sqft = 1500
address = "123 main street, rochester, NY 14607"


wv = webvalues(
    property_type=property_type,
    investment_type=investment_type,
    list_price=list_price,
    rentroll=rentroll,
    insurance=insurance,
    taxes=taxes,
    hoa=hoa_fees,
    address=address
)

house = RealEstate(webvalues=wv)
house.analyze()