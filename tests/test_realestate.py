from realestate import House
from pytest import mark


property_type = "multi"
investment_type = "house_hack"
list_price = 100000
rentroll = [800, 800]
insurance = 53
taxes = 537
hoa = 0
address = "123 main street, rochester, NY 14607"

INVESTMENT_TYPES = ["pure_investment", "house_hack"]
INVESTMENT_PERCENTS = {"pure_investment": 0.25, "house_hack": 0.03}
DOWN_PAYMENT = {"pure_investment": 25000, "house_hack": 3000}


@mark.parameterize(percents)
def test_class_has_correct_down_payment_percentages():
    house = House(
        property_type="multi",
        list_price=list_price,
        rentroll=rentroll,
        insurance=insurance,
        taxes=taxes,
        hoa=hoa,
        investment_type=key,
    )
    assert house.down_payment_pct == val


# @mark.parameterize()
# def test_class_has_correct_down_payment_value():
#     house = House(
#         property_type="multi",
#         list_price=list_price,
#         rentroll=rentroll,
#         insurance=insurance,
#         taxes=taxes,
#         hoa=hoa,
#         investment_type=key,
#     )
#     assert house.down_payment == val


@mark.parametrize("investment_types", INVESTMENT_TYPES)
def test_class_does_not_mutate_values(investment_types):
    house = House(
        property_type="multi",
        list_price=list_price,
        rentroll=rentroll,
        insurance=insurance,
        taxes=taxes,
        hoa=hoa,
        investment_type=investment_types,
    )
    assert house.investment_type == investment_types
    assert house.rentroll == rentroll
    assert house.property_type == property_type
    assert house.insurance == insurance
    assert house.taxes == taxes
    assert house.hoa == hoa
