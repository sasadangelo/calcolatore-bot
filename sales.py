class SalesAmounts:
    def __init__(self, purchase_price_capital_gain=0, taxable_amount=0, refunded_amount=0, capital_gain_tax=0, remaining_gain_loss=0):
        self.purchase_price_capital_gain = purchase_price_capital_gain
        self.taxable_amount = taxable_amount
        self.refunded_amount = refunded_amount
        self.capital_gain_tax = capital_gain_tax
        self.remaining_gain_loss = remaining_gain_loss
