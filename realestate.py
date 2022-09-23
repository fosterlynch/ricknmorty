from typing import List
from mortgage import Loan
from dataclasses import dataclass
import matplotlib.pyplot as plt

@dataclass
class percents:
    capex:float = 0.1
    misc_ex:float = 0.05
    repairs:float = 0.08
    mgmt:float = 0.1
    vacancy:float = 0.05

@dataclass
class utilities:
    """monthly value estimations, rough estimations"""
    water_sewer:int = 120 # eventually these should be distributions
    gas:int = 120 # that way there can be lower and upper bound estimations on profitability
    electric:int = 120 # then I can just analyze using the lower bound profitability
    garbage:int = 40

@dataclass
class webvalues:
    list_price:int
    taxes:int=100
    insurance:int=100
    hoa:int = 0
    lawn:int = 50
    rentroll:List[int] = [0]
    num_units:int = 1
    property_type:str = "single"
    interest_rate:float = .05
    num_months:int = 360

    def __post_init__(self):
        assert self.property_type in ["single", "multi"]
        
class RealEstate(percents, utilities, webvalues):
    def __init__(self, webvalues=webvalues, utilities=utilities, percents=percents):
        '''Calculate monthly expenses'''
        
        self._property_type = webvalues.property_type
        self._rental_income = sum(webvalues.rental_income)
        self._list_price = webvalues.list_price
        
        self.taxes = webvalues.taxes
        self.insurance = webvalues.insurance
        self.hoa = webvalues.hoa
        self.lawn = webvalues.lawn
        
        self.num_units = webvalues.num_units

        self.property_type = self._property_type
        self.rental_income = self._rental_income
        self.list_price = self._list_price
        
        self.set_expenses()

    def compute_payment(self):
        self.down_payment = self.list_price * self.down_payment_pct
        self.principal_amount = self.list_price - self.down_payment
        self.loan = Loan(principal=self.principal_amount, interest=0.05, term=30)
        self.monthly_payment = float(self.loan.monthly_payment)
    
    
    def set_expenses(self):
        if self.property_type == "multi":
            self.down_payment_pct = 0.2
            self.compute_payment()
            
            try:
                assert self.rental_income != 0
            except AssertionError:
                print("Warning: Rental property income is 0, this isn't good.")
            
            self.capex = self.rental_income * percents.capex
            self.mgmt_fees = self.rental_income * percents.mgmt
            self.repairs = self.rental_income * percents.repairs
            self.misc_expenses = self.rental_income * percents.misc_ex
            self.vacancy = self.rental_income * percents.vacancy
        
        
            self.water_sewer = 0
            self.garbage = 0
            self.electric = 0
            self.gas = 0
            
        else:
            # personal property, variable expences will be a function of mortgage
            self.down_payment_pct = 0.03
            self.compute_payment()
            
            self.capex = self.monthly_payment * percents.capex 
            self.mgmt_fees = 0
            self.misc_expenses = self.monthly_payment * percents.misc_ex
            self.repairs = self.monthly_payment * percents.repairs
            self.vacancy = 0
            
            self.water_sewer = utilities.water_sewer
            self.garbage = utilities.garbage
            self.electric = utilities.electric
            self.gas = utilities.gas

            
    def _expenses(self):
        return {"capex":self.capex, 
                "mgmt":self.mgmt_fees, 
                "average misc expenses": self.misc_expenses, 
                "repairs": self.repairs, 
                "vacancy_cost": self.vacancy, 
                "water_sewer":self.water_sewer,
                "garbage":self.garbage,
                "lawn":self.lawn,
                "electric":self.electric,
                "gas":self.gas,
                "hoa":self.hoa,
                "taxes":self.taxes,
                "insurance":self.insurance,
                "monthly_payment":self.monthly_payment
               }
    
    def monthly_expenses(self):
        return sum(self._expenses().values())
    
    def cashflow(self):
        return round(float(self.rental_income - self.monthly_expenses()), 2)

    def effective_rent(self):
        """assuming i live here, create a wrapper for that"""
        self.property_type = "single"
        self.set_expenses()
        cashflow = self.cashflow()
        self.reset_values()
        return cashflow
    
    def roi_as_pct(self):
        return round((self.cashflow() * 12) / self.down_payment, 2) * 100
    
    def print_numbers(self):
        print(f"expenses: ${self.monthly_expenses()} / month")
        print(f"cashflow: ${self.cashflow()} / month")
        print(f"down_payment: ${self.down_payment} down")
        print(f"return on investment: {self.roi_as_pct()} %")
        print(f"time to recoup investment: {self.time_to_recoup()}")
        return {"cashflow": self.cashflow(), "recoup_time": self.time_to_recoup(),"expenses": self.monthly_expenses()}
        
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
        print(f"values for property as a {self.property_type} property")
        self.property_type = "multi"

        self.set_expenses()
        self.print_numbers()
        
        print("------------")

        self.property_type = "single"
        print(f"values for property as a {self.property_type} property")

        self.set_expenses()
        self.print_numbers()
    
        self.reset_values()
        
    def reset_values(self):
        self.property_type = self._property_type
        self.list_price = self._list_price
        self.rental_income = self._rental_income
        self.set_expenses()
        print("resetting back to initialized values")
        
    def time_to_recoup(self):
        """compute the total time before I gain my investment back in months"""
        months = self.down_payment / abs(self.cashflow())
        if months > 12:
            return (months / 12, "years")
        else:
            return (months, "months")
    
    # def plot_equity(self):
    #     # TODO: use RealEstate.loan._schedule to iterate over payment types
    #     print(dir(self.loan))
    #     balance = self.down_payment
    #     equity = []
    #     month = 1
    #     date = []
    #     while balance <= self.list_price:
    #         date.append(month/12)
    #         month += 1
    #         balance += self.monthly_payment
    #         equity.append(balance)
    #     plt.scatter(date, equity)
    
    
    # def plot_debt(self):
    #     # TODO: use RealEstate.loan._schedule to iterate over payment types
    #     balance = self.principal_amount
    #     debt = []
    #     month = 1
    #     date = []
    #     while balance >= 1.4740E-20:
    #         date.append(month/12)
    #         month += 1
    #         balance -= self.monthly_payment
    #         debt.append(balance)
    #     plt.scatter(date, debt)
        
    
    def generate_full_report(self):
        """this should be the verbose output where assumptions are listed so user knows what to watch out for"""
        
        self.analyze()
        print("monthly payment: ", self.monthly_payment)
        print("loan summary \n", self.loan.summarize)
        print("house expenses accounted for", self._expenses())
        