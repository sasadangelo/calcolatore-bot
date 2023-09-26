import unittest
from datetime import date
from bot_catalog import BOTCatalog
from bot import BOT
from purchase import PurchaseData
from bank_fee_policy import BankFeePolicyManager
from portfolio import Portfolio
from bot_calculator import BOTCalculator

class TestBOTCalculator(unittest.TestCase):
    def setUp(self):
        self.catalog = BOTCatalog()
        self.fee_policy_manager = BankFeePolicyManager()
        self.calculator = BOTCalculator()

    def test_calculate_fb24_bot(self):
        bot = self.catalog.get_bot("Bot Zc Fb24 A Eur")
        purchase_data = PurchaseData(date(2023, 3, 1), 96.846, 5000, False)
        portfolio = Portfolio()
        purchase_costs, sale_amounts = self.calculator.calculate(
            bot, 
            purchase_data, 
            self.fee_policy_manager.get_bank_fee_policy("Intesa San Paolo", "MOT"), portfolio)
        
        self.assertAlmostEqual(purchase_costs.clean_price, 4842.3, places=2)
        self.assertAlmostEqual(purchase_costs.commission, 15.12, places=2)
        self.assertAlmostEqual(purchase_costs.tax, 18.72, places=2)
        self.assertAlmostEqual(purchase_costs.total_cost, 4876.14, places=2)

        self.assertAlmostEqual(sale_amounts.refunded_amount, 5000, places=2)
        self.assertAlmostEqual(sale_amounts.capital_gain_tax, 0, places=2)
        self.assertAlmostEqual(sale_amounts.remaining_gain_loss, 7.15, places=2)

if __name__ == '__main__':
    unittest.main()
