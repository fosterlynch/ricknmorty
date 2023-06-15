from realestate import House
from pytest import mark


property_type = "multi"
investment_type = "house_hack"
list_price = 100000
rentroll = [800, 800]
insurance = 53
taxes = 537
hoa = 0

INVESTMENT_TYPES = ["pure_investment", "house_hack"]


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


@mark.parametrize("investment_type", INVESTMENT_TYPES)
def test_class_list_price_equals_offer_price_on_init(investment_type):
    house = House(
        property_type="multi",
        list_price=list_price,
        rentroll=rentroll,
        insurance=insurance,
        taxes=taxes,
        hoa=hoa,
        investment_type=investment_type,
    )
    assert house.list_price == house.offer_price


def test_class_finds_correct_offer_price():
    pass


def test_class_runs_both_scenarios():
    pass


def test_class_runs_analysis_correctly():
    pass


def test_class_has_correct_properties():
    """
    house_expenses
    monthly_expenses
    cashflow
    roi_as_pct
    covers_mortgage
    time_to_recoup
    """
    pass


def test_class_finds_correct_breakeven_rent():
    pass


def test_class_sets_income_correctly_for_each_case():
    pass


def test_class_sets_expenses_correctly_for_each_case():
    pass


def test_class_returns_to_defaults_after_scenario_running():
    pass
