from ctypes import util
from typing import List
from mortgage import Loan
from dataclasses import dataclass, field
import matplotlib.pyplot as plt


@dataclass
class percents:
    """default percents to estimate expenses that are variable to rental income"""

    capex: float = 0.1
    misc_ex: float = 0.05
    repairs: float = 0.08
    mgmt: float = 0.1
    vacancy: float = 0.05
    down_payment_pct: float = (
        0.03  # this is not an expense, I should move this
    )
    # somewhere else


@dataclass
class utilities:
    """Rough estimations for fixed expenses"""

    water_sewer: int = 120
    gas: int = 120
    electric: int = 120
    garbage: int = 40


@dataclass
class webvalues:
    """These values will be specified by the user, these are the most important """

    list_price: int
    rentroll: List = field(default_factory=lambda: [0])
    insurance: int = 100
    taxes: int = 100
    hoa: int = 0
    lawn: int = 50
    property_type: str = "single"
    investment_type: str = "house_hack"
    interest_rate: float = 0.05
    num_months: int = 360

    def __post_init__(self):
        assert self.property_type in ["single", "multi"]
        assert self.investment_type in ["house_hack", "pure_investment"]


class RealEstate(webvalues, utilities, percents):
    """The responsibility of the RealEstate Class is to generate a financial
    profile for the given property of interest


    Args:
        percents (_type_): _description_
        utilities (_type_): _description_
        webvalues (_type_): _description_
    """

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

        self.rental_income = sum(self.rentroll)

        self.set_income(
            self.rentroll,
            self.investment_type,
            self.property_type,
        )

        self.set_expenses_by_type(
            self.investment_type,
            self.property_type,
        )

    def set_income(self, rentroll, investment_type, property_type):
        if investment_type == "house_hack":
            if property_type == "multi":
                effective_rent = min(rentroll)
                self.rental_income = sum(rentroll) - effective_rent
        else:
            self.rental_income = sum(rentroll)

    def set_expenses_by_type(self, investment_type, property_type):
        """
        set expenses takes in rental income, investment type, and property type
        and then sets class expense attributes to correct value based on the
        amount of rental income that is generated.

        returns none

        Args:
            rental_income (_type_): _description_
            investment_type (_type_): _description_
            property_type (_type_): _description_
        """
        if investment_type == "pure_investment":
            self.set_expenses_investment()

        if investment_type == "house_hack":
            self.set_expenses_house_hack()

    def set_expenses_investment(self):
        self.down_payment_pct = 0.2
        self.set_monthly_payment(down_payment_pct=self.down_payment_pct)

        if self.debug:
            try:
                assert self.rental_income != 0
            except AssertionError:
                print("Warning: Rental property income is 0, this isn't good.")

        self.capex = self.rental_income * percents.capex
        self.mgmt_fees = self.rental_income * percents.mgmt
        self.repairs = self.rental_income * percents.repairs
        self.misc_expenses = self.rental_income * percents.misc_ex
        self.vacancy = self.rental_income * percents.vacancy

        # tenant pays these
        self.water_sewer = 0
        self.garbage = 0
        self.electric = 0
        self.gas = 0

    def set_expenses_house_hack(self):
        # personal property, variable expences will be a function of mortgage
        self.down_payment_pct = 0.03
        self.set_monthly_payment(down_payment_pct=self.down_payment_pct)

        if self.property_type == "single":
            self.capex = self.monthly_payment * percents.capex
            self.mgmt_fees = 0  # I live there, there is no management fee
            self.misc_expenses = self.monthly_payment * percents.misc_ex
            self.repairs = self.monthly_payment * percents.repairs
            self.vacancy = 0  # I live there, there is no management fee

        if self.property_type == "multi":
            # year one while i live there, my rent is reduced, year two my mortgage is still low, but my rent increases

            self.capex = self.rental_income * percents.capex
            self.mgmt_fees = self.rental_income * percents.mgmt
            self.misc_expenses = self.rental_income * percents.misc_ex
            self.repairs = self.rental_income * percents.repairs
            self.vacancy = self.rental_income * percents.vacancy

    def set_monthly_payment(self, down_payment_pct: float):
        """
        Compute monthly mortgage based on down payment percent, list price,
        and some internal variables inside Loan package
        sets self.monthly_payment to estimated $'s owed to bank per month

        Args:
            down_payment_pct (float): _description_
        """
        self.down_payment = self.list_price * down_payment_pct
        self.principal_amount = self.list_price - self.down_payment
        self.loan = Loan(
            principal=self.principal_amount, interest=0.05, term=30
        )
        self.monthly_payment = float(self.loan.monthly_payment)

    def _get_all_expenses(self):
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
        return sum(self._get_all_expenses().values())

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

        print(f"rental income: {self.rental_income} $ / month\n")

        print(f"rent covers mortgage: {self.covers_mortgage()}\n")
        if self.covers_mortgage() == False:
            self.find_breakeven_rent()

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

        rental_increase = self.rental_income
        self.rental_income = original_rent

        pct_different = (
            (rental_increase - original_rent) / original_rent
        ) * 100

        print(
            f"additional rent required rent to cover mortgage is ${rental_increase} which is an {pct_different}% increase"
        )
        print(
            f"total charged rentroll would be {self.rental_income + rental_increase}"
        )

    def covers_mortgage(self):
        return self.rental_income >= (self.monthly_payment + webvalues.taxes)

    def run_scenarios(self):
        """"""
        print(
            "\n \n \n \n \n"
        )  # this is just here because docker adds a bunch of terminal text
        print("starting analysis --------")
        print("-------------------")

        for investment_type in ["pure_investment", "house_hack"]:
            # for housetype in ["house_hack", "pure_investment"]:
            print(
                f"running numbers for '{investment_type}' type scenario on {self.property_type} property\n"
            )
            self.set_income(self.rentroll, investment_type, self.property_type)
            self.set_expenses_by_type(investment_type, self.property_type)
            self.print_numbers()
            print("---------------")
        self.reset_values()

    def reset_values(self):
        self.set_income(
            self.rentroll, webvalues.investment_type, webvalues.property_type
        )
        self.set_expenses_by_type(
            webvalues.investment_type, webvalues.property_type
        )

    def time_to_recoup(self):
        """compute the total time before I gain my investment back in months"""
        if self.cashflow() < 0:
            return None
        months = self.down_payment / abs(self.cashflow())
        if months > 12:
            return (months / 12, "years")
        else:
            return (months, "months")

    def generate_full_report(self):
        """this should be the verbose output where assumptions are listed
        so user knows what to watch out for.

        Full report should be as follows:
            this property cashflows +/- $/month

            the budgeted expenses are _,_,_,_,
        """
        self.run_scenarios()
        # print("monthly payment: ", self.monthly_payment)
        # print("loan summary \n", self.loan.summarize)
        # print("house expenses accounted for", self._expenses())