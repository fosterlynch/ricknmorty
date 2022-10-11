class House:
    def __init__(self):
        self.sqft = sqft
        self.list_price = list_price


class Investment(House):
    def __init__(self):
        self.down_payment_pct = 0.2

    def compute_expenses(self):
        pass


class PersonalProperty(House):
    def __init__(self):
        self.down_payment_pct = 0.03

    def compute_expenses(self):
        pass