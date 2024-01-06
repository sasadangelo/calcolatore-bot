from datetime import date

class PurchaseData:
    def __init__(self, purchase_date=date.today(), purchase_price=0.000, lot=0, buy_auction=False):
        self.purchase_date = purchase_date
        self.purchase_price = purchase_price
        self.lot = lot
        self.buy_auction=buy_auction

class PurchaseCosts:
    def __init__(self, clean_price=0.00, commission=0.00, tax=0, total_cost=0.00):
        self.clean_price = clean_price
        self.commission = commission
        self.tax = tax
        self.total_cost = total_cost
