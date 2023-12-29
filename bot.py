from enum import Enum

class BOTType(Enum):
    ANNUALE =  "ANNUALE"
    SEMESTRALE =  "SEMESTRALE"

class BOT:
    def __init__(self, name, isin, issuance_date, issuance_price, maturity_date):
        self.name = name
        self.isin = isin
        self.issuance_date = issuance_date
        self.issuance_price = float(issuance_price.replace(',', '.'))
        self.maturity_date = maturity_date
        self.last_quote = None

        # Calcola il campo type in base alla durata
        duration = (self.maturity_date - self.issuance_date).days
        if 355 <= duration <= 370:
            self.type = BOTType.ANNUALE
        elif 170 <= duration <= 190:
            self.type = BOTType.SEMESTRALE