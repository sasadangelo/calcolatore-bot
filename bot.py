class BOT:
    def __init__(self, name, isin, issuance_date, issuance_price, maturity_date):
        self.name = name
        self.isin = isin
        self.issuance_date = issuance_date
        self.issuance_price = float(issuance_price.replace(',', '.'))
        self.maturity_date = maturity_date
        self.last_quote = None
