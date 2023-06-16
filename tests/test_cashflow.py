from realestate import House
from pytest import mark

property_type = "multi"
investment_type = "house_hack"
list_price = 100000
rentroll = [800, 800]
insurance = 53
tax_rate = 0.0316
hoa = 0


@mark.parametrize(
    "investment_types, cashflow",
    [("pure_investment", 232.02), ("house_hack", -810.34)],
)
def test_class_gets_correct_cashflow_number(investment_types, cashflow):
    house = House(
        property_type="multi",
        list_price=list_price,
        rentroll=rentroll,
        insurance=insurance,
        tax_rate=tax_rate,
        hoa=hoa,
        investment_type=investment_types,
    )
    assert house.cashflow == cashflow
