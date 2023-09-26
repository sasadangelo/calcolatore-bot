class Commission:
    def calculate(self, price):
        pass  # Da implementare nelle sottoclassi

class CommissionPercentage(Commission):
    def __init__(self, percentage):
        self.percentage = percentage

    def calculate(self, price):
        return price * self.percentage / 100

class CommissionPercentageCap(CommissionPercentage):
    def __init__(self, percentage, min_value=0, max_value=float('inf')):
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
    def __init__(self, percentage, min_value=0, max_value=float('inf'), fixed=0):
        super().__init__(percentage, min_value, max_value)
        self.fixed = fixed

    def calculate(self, price):
        calculated_percentage = super().calculate(price)
        calculated_with_fixed = calculated_percentage + self.fixed
        return calculated_with_fixed
