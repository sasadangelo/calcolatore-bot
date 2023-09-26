from datetime import date

class PurchaseData:
    def __init__(self, purchase_date=None, purchase_price=None, lot=None, buyAuction=False):
        self.purchase_date = purchase_date if purchase_date is not None else date.today()
        self.purchase_price = purchase_price
        self.lot = lot
        self.buyAuction=buyAuction

class PurchaseCosts:
    def __init__(self, clean_price=0, commission=0, tax=0, total_cost=0):
        self.clean_price = clean_price
        self.commission = commission
        self.tax = tax
        self.total_cost = total_cost
