from realestate import House
from pytest import mark


property_type = "multi"
investment_type = "house_hack"
list_price = 100000
rentroll = [800, 800]
insurance = 53
taxes = 537
hoa = 0


DOWN_PAYMENT = [("pure_investment", 25000), ("house_hack", 3000)]


@mark.parametrize(
    "investment_type, value",
    [("pure_investment", 498.98), ("house_hack", 645.34)],
)
def test_class_has_correct_monthly_mortgage(investment_type, value):
    house = House(
        property_type="multi",
        list_price=list_price,
        rentroll=rentroll,
        insurance=insurance,
        taxes=taxes,
        hoa=hoa,
        investment_type=investment_type,
    )
    assert house.mortgage_payment == value


@mark.parametrize(
    "investment_type, value", [("pure_investment", 0.25), ("house_hack", 0.03)]
)
def test_class_has_correct_down_payment_percentages(investment_type, value):
    house = House(
        property_type="multi",
        list_price=list_price,
        rentroll=rentroll,
        insurance=insurance,
        taxes=taxes,
        hoa=hoa,
        investment_type=investment_type,
    )
    assert house.down_payment_pct == value


@mark.parametrize("investment_type, down_payment_amount", DOWN_PAYMENT)
def test_class_has_correct_down_payment_value(
    investment_type, down_payment_amount
):
    house = House(
        property_type="multi",
        list_price=list_price,
        rentroll=rentroll,
        insurance=insurance,
        taxes=taxes,
        hoa=hoa,
        investment_type=investment_type,
    )
    assert house.down_payment == down_payment_amount
