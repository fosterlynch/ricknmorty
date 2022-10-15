from regex import W
from realestate import House, Webvalues

# import matplotlib.pyplot as plt

webvalues = Webvalues(
    list_price=318000,
    property_type="multi",
    investment_type="house_hack",
    rentroll=[0, 0],
    insurance=53,
    taxes=400,
    hoa=0,
    interest_rate=0.07,
)

house = House(webvalues=webvalues)
print("loan amount is: ", house.monthly_payment)
print("down payment will be:", house.down_payment)
print("parameters: ", house._webvalues)
print("cashflow is :", house.cashflow())
print("expenses are: ", house._get_all_expenses())

"""
layout to figure out if this house is a good deal

things to ignore for now
------
* area


i want to know
-------

*. how much is my loan?

*. how much should i budget?
    budget -> fx(mortgage | rental income)
        Operating Exenses:
            [ ] taxes (not a function, a known value)
            [ ] property insurance
            [ ] off site management
            [ ] Repairs and maintenance
            [ ] water/sewer/gas/electricity (Utilities)
            [ ] capex
            [ ] misc expenses
            [ ] lawn

*. how will this change my financial future?
    current loss of value is 800/month

    what is my breakeven income/month?
        its possible i could lose money each month but its still better than
        renting 800/month

        what if i lose 800/month?
            its a question of how much of that goes to my principal amount?
            if 800/month is "lost" part of that may be a budget set aside.

*. given an invesment target, what price should I buy the house for?


ideal financial future,

    get paid to live where i live, plus have the ability to
rent that unit out after I leave.
    have good appreciation of my asset over time
    have a quality property that was worth the amount of money I spent.

    make net $200 / unit after budgeted expenses
        duplex means I may still negatively cashflow until it is rented out

helpful vizualizations:

    map of how good of a deal the property is compared to other properties









"""
