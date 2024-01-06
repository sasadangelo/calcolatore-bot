class Commission:
    def calculate(self, price):
        pass  # Da implementare nelle sottoclassi

class CommissionPercentage(Commission):
    def __init__(self, percentage=0.00):
        self.percentage = percentage

    def calculate(self, price):
        return price * self.percentage / 100

class CommissionPercentageCap(CommissionPercentage):
    def __init__(self, percentage=0.00, min_value=0.00, max_value=float('inf')):
        super().__init__(percentage)
        self.min_value = min_value
        self.max_value = max_value

    def calculate(self, price):
        calculated_percentage = super().calculate(price)
        if calculated_percentage < self.min_value:
            return self.min_value
        elif calculated_percentage > self.max_value:
            return self.max_value
        else:
            return calculated_percentage

class CommissionPercentageCapPlusFixed(CommissionPercentageCap):
    def __init__(self, percentage=0.00, min_value=0.00, max_value=float('inf'), fixed=0.00):
        super().__init__(percentage, min_value, max_value)
        self.fixed = fixed

    def calculate(self, price):
        return super().calculate(price) + self.fixed
