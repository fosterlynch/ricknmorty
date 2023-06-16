from typing import List
from mortgage import Loan
from dataclasses import dataclass, field

MORTGAGE_NUM_MONTHS = 360
MORTGAGE_INTEREST_RATE = 0.07


class Percents:
    """default percents to estimate expenses that are variable to rental income"""

    capex: float = 0.1
    misc_ex: float = 0.05
    repairs: float = 0.08
    mgmt: float = 0.1
    vacancy: float = 0.05


@dataclass
class Utilities:
    """Rough estimations for fixed expenses"""

    water_sewer: int = 120
    gas: int = 120
    electric: int = 120
    garbage: int = 40


@dataclass
class Expenses(Utilities):
    insurance: int = 100
    hoa: int = 0
    lawn: int = 50
    mortgage_payment: int = 1500
    capex: int = 200
    mgmt_fees: int = 200
    misc_repairs: int = 100
    repairs: int = 200
    vacancy_cost: int = 200


@dataclass
class HouseValues:
    """These values will be specified by the user,
    these are the most important"""

    tax_rate: float
    list_price: int = 100
    rentroll: List = field(default_factory=lambda: [0])  # init = false?
    property_type: str = "single"
    investment_type: str = "house_hack"
    max_down_payment: int = 65000

    def __post_init__(self):
        assert self.property_type in ["single", "multi"]
        assert self.investment_type in ["house_hack", "pure_investment"]
        self.rental_income = sum(self.rentroll)
        self.n_units = len(self.rentroll)


class House(HouseValues, Expenses):
    """The responsibility of the RealEstate Class is to generate a financial
    profile for the given property of interest.
    """

    def __init__(
        self,
        tax_rate: float,
        list_price: int = 100000,
        rentroll: List = field(default_factory=lambda: [0]),
        insurance: int = 100,
        hoa: int = 0,
        property_type: str = "single",
        investment_type: str = "house_hack",
        max_down_payment: int = 65000,
    ):
        HouseValues.__init__(
            self,
            tax_rate,
            list_price,
            rentroll,
            property_type,
            investment_type,
            max_down_payment,
        )
        Expenses.__init__(self, insurance=insurance, hoa=hoa)
        self.debug = False
        self.offer_price = self.list_price
        self.set_income_and_expenses()

    def test_inheritance(self):
        print(
            "testing webvalues list price should be 269000",
            self.list_price,
        )

    def set_income_and_expenses(self):
        self.set_income(
            self.rentroll,
            self.investment_type,
            self.property_type,
        )
        self.set_expenses_by_type(self.investment_type, self.property_type)

    def set_income(self, rentroll, investment_type, property_type):
        if investment_type == "house_hack":
            if property_type == "multi":
                effective_rent = min(rentroll)
                self.rental_income = sum(rentroll) - effective_rent
                self.n_units = len(self.rentroll) - 1
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
        self.calculate_monthly_property_taxes()
        if investment_type == "pure_investment":
            self.set_expenses_investment()

        if investment_type == "house_hack":
            self.set_expenses_house_hack()

    def set_expenses_investment(self):
        self.down_payment_pct = 0.25
        self.set_monthly_mortgage(down_payment_pct=self.down_payment_pct)

        if self.debug:
            try:
                assert self.rental_income != 0
            except AssertionError:
                print("Warning: Rental property income is 0, this isn't good.")

        self.capex = round(self.rental_income * Percents.capex, 2)
        self.mgmt_fees = round(self.rental_income * Percents.mgmt, 2)
        self.repairs = round(self.rental_income * Percents.repairs, 2)
        self.misc_repairs = round(self.rental_income * Percents.misc_ex, 2)
        self.vacancy_cost = round(self.rental_income * Percents.vacancy, 2)

        # tenant pays these
        self.water_sewer = 0
        self.garbage = 0
        self.electric = 0
        self.gas = 0

    def set_expenses_house_hack(self):
        # personal property, variable expences will be a function of mortgage
        self.down_payment_pct = 0.03
        self.set_monthly_mortgage(down_payment_pct=self.down_payment_pct)

        if self.property_type == "single":
            self.capex = round(self.mortgage_payment * Percents.capex, 2)
            self.mgmt_fees = 0  # I live there, there is no management fee
            self.misc_repairs = round(
                self.mortgage_payment * Percents.misc_ex, 2
            )
            self.repairs = round(self.mortgage_payment * Percents.repairs, 2)
            self.vacancy_cost = 0  # I live there, there is no management fee

        if self.property_type == "multi":
            # year one while i live there, my rent is reduced, year two my mortgage is still low, but my rent increases

            self.capex = round(
                self.rental_income * Percents.capex, 2
            )  # if this is zero, then it is wrong
            self.mgmt_fees = round(self.rental_income * Percents.mgmt, 2)
            self.misc_repairs = round(self.rental_income * Percents.misc_ex, 2)
            self.repairs = round(self.rental_income * Percents.repairs, 2)
            self.vacancy_cost = round(self.rental_income * Percents.vacancy, 2)

    def set_monthly_mortgage(self, down_payment_pct):
        """
        Compute monthly mortgage based on down payment percent, list price,
        and some internal variables inside Loan package
        sets self.mortgage_payment to estimated $'s owed to bank per month

        Args:
            down_payment_pct (float): _description_
        """
        self.down_payment = self.offer_price * self.down_payment_pct
        # if self.down_payment >= self.max_down_payment:
        # logging.warning(
        #     f"price of house would exceed what I can afford \n max down payment is {self.max_down_payment}, but required downpayment is {self.down_payment}"
        # )
        self.principal_amount = self.offer_price - self.down_payment
        self.loan = Loan(
            principal=self.principal_amount,
            interest=MORTGAGE_INTEREST_RATE,
            term=int(MORTGAGE_NUM_MONTHS / 12),
        )
        self.mortgage_payment = float(self.loan.monthly_payment)

    def calculate_monthly_property_taxes(self):
        self.taxes = round((self.offer_price * 0.6 * self.tax_rate) / 12, 2)

    def find_offer_price(self):
        print("finding offer price")
        while self.cashflow < (100 * self.n_units):
            self.offer_price -= 50
            self.set_income_and_expenses()
        print(
            f"offer price should be {self.offer_price} which is {round(((self.offer_price - self.list_price)/self.list_price) * 100,2)} different from original list price"
        )

    def run_scenarios(self):
        for investment_type in ["pure_investment", "house_hack"]:
            self.investment_type = investment_type
            self.set_income(
                self.rentroll, self.investment_type, self.property_type
            )
            self.set_expenses_by_type(self.investment_type, self.property_type)
            self.analyze()
        self.set_income_and_expenses()

    def analyze(self):
        print("starting analysis --------")
        print("-------------------")
        self.find_offer_price()

        if self.covers_mortgage == False:
            print("finding break")
            self.find_breakeven_rent()

        print(
            f"property is type '{self.investment_type}' type scenario on {self.property_type} property"
        )
        print(f"cashflow: ${self.cashflow} / month")
        print(f"return on investment: {self.roi_as_pct} %")
        print(f"time to recoup investment: {self.time_to_recoup}\n")

        print(
            f"Required down payment using {self.down_payment_pct * 100}% down: ${self.down_payment} down\n"
        )

        print(f"rental income: {self.rental_income} $ / month\n")
        print(f"rent covers mortgage: {self.covers_mortgage}\n")
        print(f"expenses: ${self.house_expenses} / month\n")

        return {
            "cashflow": self.cashflow,
            "ROI": self.roi_as_pct,
            "recoup_time": self.time_to_recoup,
            "downpayment_amount": self.down_payment,
            "rental_income": self.rental_income,
            "expenses": self.monthly_expenses,
        }

    @property
    def house_expenses(self):
        return {
            "capex": self.capex,
            "mgmt": self.mgmt_fees,
            "average misc expenses": self.misc_repairs,
            "repairs": self.repairs,
            "vacancy_cost": self.vacancy_cost,
            "water_sewer": self.water_sewer,
            "garbage": self.garbage,
            "lawn": self.lawn,
            "electric": self.electric,
            "gas": self.gas,
            "hoa": self.hoa,
            "taxes": self.taxes,
            "insurance": self.insurance,
            "mortgage_payment": self.mortgage_payment,
        }

    @property
    def monthly_expenses(self):
        return round(sum(self.house_expenses.values()), 2)

    @property
    def cashflow(self):
        return round(float(self.rental_income - self.monthly_expenses), 2)

    @property
    def roi_as_pct(self):
        return round((self.cashflow * 12) / self.down_payment, 2) * 100

    @property
    def covers_mortgage(self):
        return self.rental_income >= (self.mortgage_payment + self.taxes)

    @property
    def time_to_recoup(self):
        """compute the total time before I gain my investment back in months"""

        if self.cashflow < 0:
            return None
        months = self.down_payment / abs(self.cashflow)
        if months > 12:
            return (months / 12, "years")
        else:
            return (months, "months")

    def find_breakeven_rent(self):
        """
        Given current rental income, find how much rent
        would need to be charged in order to cover taxes and morgage.

        """
        original_rent = self.rental_income

        while self.covers_mortgage == False:
            self.rental_income += 1

        rental_increase = self.rental_income
        self.rental_income = original_rent

        if self.rental_income != 0:
            pct_different = (
                (rental_increase - original_rent) / original_rent
            ) * 100

            print(
                f"additional rent required rent to cover mortgage is ${rental_increase} which is an {pct_different}% increase"  # noqa: E501
            )

        print(
            f"Required rent to cover costs is {self.rental_income + rental_increase}"  # noqa: E501
        )
