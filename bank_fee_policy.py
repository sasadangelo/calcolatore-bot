import csv
from commission import CommissionPercentageCapPlusFixed

class BankFeePolicy:
    def __init__(self, bank_name):
        self.bank_name = bank_name
        self.fee_policies = {}

    def add_market_policy(self, market, commission):
        self.fee_policies[market] = commission

    def get_market_policy(self, market):
        return self.fee_policies[market]

class BankFeePolicyManager:
    def __init__(self):
        self.bank_policies = {}
        self.__load_commissions("data/bank_fee_policy.csv")

    def add_policy(self, bank_name, market, commission):
        if bank_name not in self.bank_policies:
            self.bank_policies[bank_name] = BankFeePolicy(bank_name)
        self.bank_policies[bank_name].add_market_policy(market, commission)

    def get_bank_fee_policy(self, bank_name, market):
        if bank_name in self.bank_policies and market in self.bank_policies[bank_name].fee_policies:
            return self.bank_policies[bank_name].get_market_policy(market)
        else:
            return None

    def __load_commissions(self, csv_file):
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                bank_name = row['Bank']
                market = row['Market']
                percentage = float(row['Percentage'])
                min_value = float(row['Min']) if row['Min'] else 0
                max_value = float(row['Max']) if row['Max'] else float('inf')
                fixed = float(row['Fixed']) if row['Fixed'] else 0

                # Crea oggetti Commission in base ai dati CSV
                commission = CommissionPercentageCapPlusFixed(percentage, min_value, max_value, fixed)

                # Crea oggetti BankCommissionPolicy se necessario
                if bank_name not in self.bank_policies:
                    self.bank_policies[bank_name] = BankFeePolicy(bank_name)
                
                # Aggiungi la CommissionPolicy al BankCommissionPolicy
                self.bank_policies[bank_name].add_market_policy(market, commission)


if __name__ == "__main__":
    fee_policy_manager = BankFeePolicyManager()

    # Recupera una politica di commissione specifica
    bank_name = "Intesa San Paolo"
    market = "MOT"
    policy = fee_policy_manager.get_bank_fee_policy(bank_name, market)
    if policy:
        print(f"Bank: {bank_name}, Market: {market}, Commission: {policy.calculate(100)}")
    else:
        print(f"Policy not found for Bank: {bank_name}, Market: {market}")
