from mortgage import Loan


class HouseExpenses:
    def __init__(
        self,
        price: int,
        monthly_rent: int,
        location: str,
        interest_rate: float,
        hoa_fees: int = 0,
        lawn_care_cost: int = 50,
        insurance_cost: float = 150,
    ) -> None:
        """
        House class expenses. All expenses (meaning not price, rent, location, or interest rate), are measured in monthly time
        increments.

        Args:
            price (int): How much the house costs after down payment applied. This is the loan principal amount.
            monthy_rent (int): How much income the house brings in.
            location (str): Where the house is located. Used to determine tax rate.
            interest_rate (float): mortgage loan interest rate estimation.
        """

        self.price = price
        self.monthly_rent = monthly_rent
        self.location = location
        self.interest_rate = interest_rate
        self.hoa_fees = hoa_fees
        self.lawn_care_cost = lawn_care_cost
        self.insurance_cost = insurance_cost
        self.capex = self.monthly_rent * 0.1
        self.loan = Loan(
            principal=self.price,
            interest=self.interest_rate,
            term=30,
        )
        self.monthly_mortgage = float(self.loan.monthly_payment)
        self.wsge = 0  # this is only true for separately metered buildings
        self.mgmt_fee = self.monthly_rent * 0.1
        self.misc_repair = self.monthly_rent * 0.1
        self.cost_of_vacancy = self.monthly_rent * 0.1
        self.taxes = 500
        self.expenses = sum(  # this one is the fastest, results were noted in 390ac03ba934e0db24ff4455f70047789e1dd427
            [
                self.capex,
                self.cost_of_vacancy,
                self.hoa_fees,
                self.insurance_cost,
                self.lawn_care_cost,
                self.mgmt_fee,
                self.wsge,
                self.misc_repair,
                self.taxes,
                self.monthly_mortgage,
            ]
        )


test = HouseExpenses(150000, 1500, "ROC", 0.07)
expenses = test.expenses()
