from realestate import RealEstate, webvalues
# import matplotlib.pyplot as plt

list_price = 194750
property_type = "single"
taxes = 14000/12
insurance= 100
hoa_fees = 0
rentroll = [0]
investment_type = "primary_residence"



wv = webvalues(property_type=property_type, 
               investment_type=investment_type,
               list_price=list_price,
               rentroll=rentroll,
               insurance=insurance, 
               taxes=taxes, 
               hoa=hoa_fees)

house = RealEstate(webvalues=wv)

house.generate_full_report()
