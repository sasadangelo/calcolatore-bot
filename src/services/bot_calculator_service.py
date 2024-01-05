# BOTCalculator - BOT Calculator main class
#
# This module defines the BOTCalculator class, which is main class for managing the BOT Calculator.
#
# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo sasadangelo@gmail.com
#
# SPDX-License-Identifier: MIT
from datetime import date
from src.services.bot_catalog_service import BOTCatalogService
from src.services.bank_fee_policy_service import BankFeePolicyService
from src.model.purchase import PurchaseData, PurchaseCosts
from src.model.tax_fee_policy import TaxFeePolicy
from src.model.portfolio import Portfolio
from src.model.sales import SalesAmounts

# This class represents the BOT Calculator. It has a calculate method where it gets the following input:
# - BOT Name
# - Purchase Data
# - Bank Fee Policy
# - Portfolio Minus
#
# It calculates the:
# - Purchase Costs
#   - Clean Price
#   - Commission
#   - Tax
#   - Total Cost
# - Sales Amounts
#   - Purchase Price Capital Gain
#   - Taxable Amount
#   - Refunded Amount
#   - Capital Gain Tax
#   - Remaining Gain Loss
class BOTCalculatorService:
    def calculate(self, bot, purchase_data, bank_fee_policy, portfolio):
        # The number of BOT bought is LOT/100
        quantity = purchase_data.lot/100
        clean_price = purchase_data.purchase_price * quantity
        commission = bank_fee_policy.calculate(clean_price)
        tax = TaxFeePolicy().calculate(bot, purchase_data)
        total_cost = clean_price + commission + tax
        purchase_costs = PurchaseCosts(clean_price, commission, tax, total_cost)
        purchase_price_capital_gain=(clean_price + commission)/quantity-(bot.get_theoric_price(purchase_data.purchase_date)-bot.issuance_price) if quantity != 0 else 0.00000
        realized_gain_loss = (bot.issuance_price - purchase_price_capital_gain)*quantity
        if portfolio.capital_loss > realized_gain_loss:
            taxable_amount = 0.00
        else:
            taxable_amount = realized_gain_loss - portfolio.capital_loss
        capital_gain_tax = taxable_amount * 12.5
        refunded_amount = purchase_data.lot - capital_gain_tax
        if (portfolio.capital_loss - realized_gain_loss) < 0:
            remaining_gain_loss = 0.00
        else:
            remaining_gain_loss = portfolio.capital_loss - realized_gain_loss
        sale_amounts = SalesAmounts(purchase_price_capital_gain, realized_gain_loss, taxable_amount, refunded_amount, capital_gain_tax, remaining_gain_loss)
        return purchase_costs, sale_amounts
        
if __name__ == "__main__":
    catalog = BOTCatalogService()
    bot = catalog.get_bot("Bot Zc Fb24 A Eur")
    fee_policy_service = BankFeePolicyService()
    fee_policy = fee_policy_service.get_bank_fee_policy("Intesa San Paolo", "MOT")
    purchase_data = PurchaseData(date(2023, 3, 1), 96.846, 5000, False)
    portfolio = Portfolio()
    bot_calculator = BOTCalculatorService()
    purchase_costs, sale_amounts = bot_calculator.calculate(bot, purchase_data, fee_policy, portfolio)
    print("Importo Secco: ", purchase_costs.clean_price)
    print("Commissioni: ", round(purchase_costs.commission,2))
    print("Tasse: ", round(purchase_costs.tax,2))
    print("Totale Costo: ", round(purchase_costs.total_cost,2))
    print()
    print("Importo Rimborsato: ", sale_amounts.refunded_amount)
    print("Tasse Capital Gain: ", round(sale_amounts.capital_gain_tax,2))
    print("Minus Valenza Realizzata: ", round(sale_amounts.remaining_gain_loss,2))
