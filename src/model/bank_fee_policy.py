from src.model.commission import CommissionPercentageCapPlusFixed

class BankFeePolicy:
    def __init__(self, bank_name):
        self.bank_name = bank_name
        self.fee_policies = {}

    def add_market_policy(self, market, commission):
        self.fee_policies[market] = commission

    def get_market_policy(self, market):
        return self.fee_policies[market]