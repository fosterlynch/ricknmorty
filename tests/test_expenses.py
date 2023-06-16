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
    "investment_types, expenses",
    [
        (
            "pure_investment",
            {
                "capex": 160.0,
                "mgmt": 160.0,
                "average misc expenses": 80.0,
                "repairs": 128.0,
                "vacancy_cost": 80.0,
                "water_sewer": 0,
                "garbage": 0,
                "lawn": 50,
                "electric": 0,
                "gas": 0,
                "hoa": 0,
                "taxes": 158.0,
                "insurance": 53,
                "mortgage_payment": 498.98,
            },
        ),
        (
            "house_hack",
            {
                "capex": 80.0,
                "mgmt": 80.0,
                "average misc expenses": 40.0,
                "repairs": 64.0,
                "vacancy_cost": 40.0,
                "water_sewer": 120,
                "garbage": 40,
                "lawn": 50,
                "electric": 120.0,
                "gas": 120.0,
                "hoa": 0,
                "taxes": 158.0,
                "insurance": 53,
                "mortgage_payment": 645.34,
            },
        ),
    ],
)
def test_class_computes_correct_expenses(investment_types, expenses):
    house = House(
        property_type="multi",
        list_price=list_price,
        rentroll=rentroll,
        insurance=insurance,
        tax_rate=0.0316,
        hoa=hoa,
        investment_type=investment_types,
    )
    assert house.house_expenses == expenses


@mark.parametrize(
    "investment_types,total_expense",
    [("pure_investment", 1367.98), ("house_hack", 1610.34)],
)
def test_class_computes_correct_total_expense(investment_types, total_expense):
    house = House(
        property_type="multi",
        list_price=list_price,
        rentroll=rentroll,
        insurance=insurance,
        tax_rate=0.0316,
        hoa=hoa,
        investment_type=investment_types,
    )
    assert house.monthly_expenses == total_expense
