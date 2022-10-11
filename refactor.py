from dataclasses import dataclass
from sre_parse import _OpInType

@dataclass
class Expenses:
    capex: int
    misc: int
    mgmt: int
    water: int
    sewer: int
    gas: int
    electric: int
    insurance: int
    accounting: int
    legal: int

@dataclass
class Income:
    rent:int

@dataclass
class Listing:
    pass


class House(Expenses, Income):
    def __init__(self, list_price, sqft):
        self.sqft = sqft
        self.list_price = list_price

class MultiFamily(House):
    def __init__(self) -> None:
        self.down_payment_pct = 0.2

class SingleFamily(House):
    def __init__(self) -> None:
        self.down_payment_pct = 0.03


class Investment(House):
    def __init__(self):
        self.down_payment_pct = 0.2

    def cashflow(self):
        return self.rent - self.


class PersonalProperty(House):
    def __init__(self):
        self.down_payment_pct = 0.03

    def compute_expenses(self):
        pass

