from realestate import RealEstate, webvalues

list_price = 599000
property_type = "multi"
taxes = 453
insurance = 160
hoa_fees = 0
rentroll = [1500, 1500]
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
