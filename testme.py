from realestate import RealEstate, webvalues

# import matplotlib.pyplot as plt

list_price = 274900
property_type = "multi"
taxes = 4206 / 12
insurance = 100
hoa_fees = 0
rentroll = [1247, 1247]
investment_type = "house_hack"
sqft = 1500


wv = webvalues(
    sqft=sqft,
    property_type=property_type,
    investment_type=investment_type,
    list_price=list_price,
    rentroll=rentroll,
    insurance=insurance,
    taxes=taxes,
    hoa=hoa_fees,
)

house = RealEstate(webvalues=wv)

house.generate_full_report()
