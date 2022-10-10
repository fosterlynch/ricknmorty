

def save_information(classobj):
    for variable, value in vars(classobj).items():
        print(variable, value)



 def plot_equity(
        self,
    ):  # i think this could be part of the visualization class
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

    def plot_debt(
        self,
    ):  # i think this could be part of the visualization class
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