import unittest
from datetime import date
from src.services.bot_catalog_service import BOTCatalogService
from src.model.bot import BOT
from src.model.purchase import PurchaseData
from src.model.bank_fee_policy import BankFeePolicyManager
from src.model.portfolio import Portfolio
from src.services.bot_calculator_service import BOTCalculatorService

class TestBOTCalculator(unittest.TestCase):
    def setUp(self):
        self.catalog = BOTCatalogService()
        self.fee_policy_manager = BankFeePolicyManager()
        self.calculator = BOTCalculatorService()

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
