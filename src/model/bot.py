from enum import Enum
from datetime import datetime

class BOTType(Enum):
    ANNUALE =  "ANNUALE"
    SEMESTRALE =  "SEMESTRALE"
    TRIMESTRALE =  "TRIMESTRALE"

class BOT:
    def __init__(self, name="", isin="", issuance_date=datetime.now().date(), issuance_price=0.000, maturity_date=datetime.now().date()):
        self.name = name
        self.isin = isin
        self.issuance_date = issuance_date
        self.issuance_price = issuance_price
        self.maturity_date = maturity_date
        self.last_quote = None

        # Calcola il campo type in base alla durata
        if 355 <= self.get_duration() <= 370:
            self.type = BOTType.ANNUALE
        elif 170 <= self.get_duration() <= 190:
            self.type = BOTType.SEMESTRALE
        elif 85 <= self.get_duration() <= 95:
            self.type = BOTType.TRIMESTRALE
    
    def get_duration(self):
        return (self.maturity_date - self.issuance_date).days

    def get_remaining_duration(self, date=datetime.now().date()):
        return (self.maturity_date - date).days

    def get_passed_duration(self, date=datetime.now().date()):
        return (date - self.issuance_date).days

    def get_theoric_price(self, date=datetime.now().date()):
        return self.issuance_price + (100 - self.issuance_price)*(self.get_passed_duration(date)/self.get_duration())