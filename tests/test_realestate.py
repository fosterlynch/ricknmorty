from numbers import Real
from realestate import RealEstate, webvalues, utilities, percents
# from mortgage import Loan

# example house values

property_type = "multi"
investment_type = "house_hack"
list_price = 200000
rentroll = [800, 800]
insurance = 53
taxes = 537
hoa_fees = 0
address = "123 main street, rochester, NY 14607"

wv = webvalues(
    property_type=property_type,
    investment_type=investment_type,
    list_price=list_price,
    rentroll=rentroll,
    insurance=insurance,
    taxes=taxes,
    hoa=hoa_fees,
    address=address
)

bills = utilities()

house = RealEstate(webvalues=wv)

def test_class_has_correct_down_payment_percentages():
    canon = {"pure_investment":0.2, "house_hack":0.03}

    for key, val in canon.items():
        wv.investment_type = key
        house = RealEstate(wv)
        assert house.down_payment_pct == val
        
# def test_class_sets_expenses_correctly():

# def test_class_has_correct_loan_amount():
#     monthly_paynment = Loan(
#             principal=list_price, interest=0.05, term=30
#         ).monthly_payment

#     assert house.monthly_payment == monthly_paynment

#     def compute_payment(self, down_payment_pct: float):
#         """
#         Compute monthly mortgage based on down payment percent, list price,
#         and some internal variables inside Loan package
#         sets self.monthly_payment to estimated $'s owed to bank per month

#         Args:
#             down_payment_pct (float): _description_
#         """
#         self.down_payment = self.list_price * down_payment_pct
#         self.principal_amount = self.list_price - self.down_payment
#         self.loan = Loan(
#             principal=self.principal_amount, interest=0.05, term=30
#         )
#         self.monthly_payment = float(self.loan.monthly_payment)


# def test_class_has_correct_expenses():
#     assert house.monthly_expenses() == 0


# def test_class_keeps_correct_values():
#     assert house.cashflow() == 0