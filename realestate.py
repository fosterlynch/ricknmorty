from typing import List
from mortgage import Loan
from dataclasses import dataclass, field
import matplotlib.pyplot as plt


@dataclass
class percents:
    capex: float = 0.1
    misc_ex: float = 0.05
    repairs: float = 0.08
    mgmt: float = 0.1
    vacancy: float = 0.05


@dataclass
class utilities:
    """monthly value estimations, rough estimations"""

    water_sewer: int = 120  # eventually these should be distributions
    gas: int = 120  # that way there can be lower and upper bound estimations on profitability
    electric: int = (
        120  # then I can just analyze using the lower bound profitability
    )
    garbage: int = 40


@dataclass
class webvalues:
    list_price: int
    sqft: int
    taxes: int = 100
    insurance: int = 100
    hoa: int = 0
    lawn: int = 50
    rentroll: List = field(default_factory=[0])
    property_type: str = "single"
    investment_type: str = "house_hack"
    interest_rate: float = 0.05
    num_months: int = 360

    def __post_init__(self):
        assert self.property_type in ["single", "multi"]
        assert self.investment_type in ["house_hack", "pure_investment"]


class RealEstate(percents, utilities, webvalues):
    def __init__(
        self, webvalues=webvalues, utilities=utilities, percents=percents
    ):
        """Calculate monthly expenses"""

        self.debug = False
        self.water_sewer = utilities.water_sewer
        self.garbage = utilities.garbage
        self.electric = utilities.electric
        self.gas = utilities.gas

        self.taxes = webvalues.taxes
        self.insurance = webvalues.insurance
        self.hoa = webvalues.hoa
        self.lawn = webvalues.lawn

        self.list_price = webvalues.list_price
        self.property_type = webvalues.property_type
        self.rentroll = webvalues.rentroll
        self.rental_income = sum(webvalues.rentroll)
        self.set_expenses(webvalues.investment_type)

    def compute_payment(self, down_payment_pct):
        self.down_payment = self.list_price * down_payment_pct
        self.principal_amount = self.list_price - self.down_payment
        self.loan = Loan(
            principal=self.principal_amount, interest=0.05, term=30
        )
        self.monthly_payment = float(self.loan.monthly_payment)

    def set_expenses(self, investment_type):
        try:
            assert investment_type in ["house_hack", "pure_investment"]
        except AssertionError:
            print(
                f"AssertionError: investment type: {investment_type} not in ['house_hack','pure_investment']"
            )

        if investment_type == "pure_investment":
            self.rental_income = sum(self.rentroll)
            self.down_payment_pct = 0.2
            self.compute_payment(down_payment_pct=self.down_payment_pct)

            try:
                assert self.rental_income != 0
            except AssertionError:
                print("Warning: Rental property income is 0, this isn't good.")

            self.capex = self.rental_income * percents.capex
            self.mgmt_fees = self.rental_income * percents.mgmt
            self.repairs = self.rental_income * percents.repairs
            self.misc_expenses = self.rental_income * percents.misc_ex
            self.vacancy = self.rental_income * percents.vacancy

            if self.debug:
                # tenant pays for utilities
                print("Soft warning: Assuming tenant is paying for utilities")
                print(
                    "values have been set to 0. To change values, insert a modified utilities class"
                )

            self.water_sewer = 0
            self.garbage = 0
            self.electric = 0
            self.gas = 0

        if investment_type == "house_hack":
            # personal property, variable expences will be a function of mortgage
            self.down_payment_pct = 0.03
            self.compute_payment(down_payment_pct=self.down_payment_pct)

            if self.property_type == "single":
                self.capex = self.monthly_payment * percents.capex
                self.mgmt_fees = 0  # I live there, there is no management fee
                self.misc_expenses = self.monthly_payment * percents.misc_ex
                self.repairs = self.monthly_payment * percents.repairs
                self.vacancy = 0  # I live there, there is no management fee

            if self.property_type == "multi":
                # two scnearios, while i am living there and when i move out
                # when i live there, the rent is lower
                # when i move out, the rent is higher
                self.effective_rent = min(self.rentroll)
                print("RESETTING RENT INCOME BASESD ON MULTIFAMILY HOUSEHACK")
                self.rental_income = sum(self.rentroll) - self.effective_rent

                self.capex = self.rental_income * percents.capex
                self.misc_expenses = self.rental_income * percents.misc_ex
                self.repairs = self.rental_income * percents.repairs
                self.mgmt_fees = self.rental_income * percents.mgmt
                self.vacancy = self.rental_income * percents.vacancy

    def _expenses(self):
        return {
            "capex": self.capex,
            "mgmt": self.mgmt_fees,
            "average misc expenses": self.misc_expenses,
            "repairs": self.repairs,
            "vacancy_cost": self.vacancy,
            "water_sewer": self.water_sewer,
            "garbage": self.garbage,
            "lawn": self.lawn,
            "electric": self.electric,
            "gas": self.gas,
            "hoa": self.hoa,
            "taxes": self.taxes,
            "insurance": self.insurance,
            "monthly_payment": self.monthly_payment,
        }

    def monthly_expenses(self):
        return sum(self._expenses().values())

    def cashflow(self):
        return round(float(self.rental_income - self.monthly_expenses()), 2)

    def roi_as_pct(self):
        return round((self.cashflow() * 12) / self.down_payment, 2) * 100

    def print_numbers(self):
        print(f"cashflow: ${self.cashflow()} / month\n")
        print(f"return on investment: {self.roi_as_pct()} %\n")
        print(f"time to recoup investment: {self.time_to_recoup()}\n")

        print(
            f"Required down payment using {self.down_payment_pct * 100}% down: ${self.down_payment} down\n"
        )

        print(f"rent covers mortgage: {self.covers_mortgage()}\n")
        if self.covers_mortgage() == False:
            self.find_breakeven_rent()

        print(f"rental income: {self.rental_income} $ / month\n")
        print(f"expenses: ${self.monthly_expenses()} / month\n")

        return {
            "cashflow": self.cashflow(),
            "recoup_time": self.time_to_recoup(),
            "expenses": self.monthly_expenses(),
        }

    def find_breakeven_rent(self):
        original_rent = self.rental_income
        while self.covers_mortgage() == False:
            self.rental_income += 1
        pct_different = (
            (self.rental_income - original_rent) / original_rent
        ) * 100
        print(
            f"required rent to cover mortgage is ${self.rental_income} which is {pct_different}% different "
        )
        self.rental_income = sum(self.rentroll)

    def covers_mortgage(self):
        return self.rental_income >= (self.monthly_payment + webvalues.taxes)

    def analyze(self):
        """
        my property can be EITHER

        Single family

        OR

        Multi family


        IF it's single family. Then I should find what rent i could charge that would make me break
        even. which is equivalent to the total expenses i need to account for PLUS my profitability
        margin. which for single family we will claim to be 200 dollars / month.

        IF its multifamily. then i need to run two loan options

            one loan option is if i use it as a primary residence
                if i am a resident, then num_units -= 1

                one way to structure this would be rentroll[rent1,rent2,rent3]
                then that gives me num_units = len(rentroll), total_rent = sum(rentroll),
                as well as subtract one unit (assume low and high, )


            one loan option is if i only buy it as an investment

        !! I need to add my max amount I can put as a down payment, which will then tell me if I can
        buy it with the 20% loan


        """
        print(
            "\n \n \n \n \n"
        )  # this is just here because docker adds a bunch of terminal text
        print("starting analysis --------")
        print("-------------------")

        for housetype in ["pure_investment", "house_hack"]:
            print(
                f"running numbers for '{housetype}' type scenario on {self.property_type} property\n"
            )
            self.set_expenses(housetype)
            self.print_numbers()
            print("---------------")
        self.reset_values()

    def reset_values(self):
        self.set_expenses(webvalues.investment_type)

    def time_to_recoup(self):
        """compute the total time before I gain my investment back in months"""
        if self.cashflow() < 0:
            return None
        months = self.down_payment / abs(self.cashflow())
        if months > 12:
            return (months / 12, "years")
        else:
            return (months, "months")

    def plot_equity(self):
        # TODO: use RealEstate.loan._schedule to iterate over payment types
        print(dir(self.loan))
        balance = self.down_payment
        equity = []
        month = 1
        date = []
        while balance <= self.list_price:
            date.append(month / 12)
            month += 1
            balance += self.monthly_payment
            equity.append(balance)
        plt.scatter(date, equity)

    def plot_debt(self):
        # TODO: use RealEstate.loan._schedule to iterate over payment types
        balance = self.principal_amount
        debt = []
        month = 1
        date = []
        while balance >= 1.4740e-20:
            date.append(month / 12)
            month += 1
            balance -= self.monthly_payment
            debt.append(balance)
        plt.scatter(date, debt)

    def generate_full_report(self):
        """this should be the verbose output where assumptions are listed
        so user knows what to watch out for.

        Full report should be as follows:
            this property cashflows +/- $/month

            the budgeted expenses are _,_,_,_,
        """
        self.analyze()
        # print("monthly payment: ", self.monthly_payment)
        # print("loan summary \n", self.loan.summarize)
        # print("house expenses accounted for", self._expenses())
