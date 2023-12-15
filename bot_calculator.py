# BOTCalculator - BOT Calculator main class
#
# This module defines the BOTCalculator class, which is main class for managing the BOT Calculator.
#
# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo sasadangelo@gmail.com
#
# SPDX-License-Identifier: MIT
from bot_catalog import BOTCatalog
from bot import BOT
from datetime import date
from purchase import PurchaseData, PurchaseCosts
from bank_fee_policy import BankFeePolicyManager
from tax_fee_policy import TaxFeePolicy
from portfolio import Portfolio
from sales import SalesAmounts

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
class BOTCalculator:
    def calculate(self, bot, purchase_data, bank_fee_policy, portfolio):
        # The number of BOT bought is LOT/100
        quantity = purchase_data.lot/100
        # The BOT duration is the amount of time in days between the issuance and maturity date.
        # The BOT passed durantion is the amount of time between the regulament day (=buy day + 2 business days) and the maturity date
        duration = bot.maturity_date - bot.issuance_date
        passed_duration = purchase_data.purchase_date - bot.issuance_date
        # the teoric price is the price the BOT has in a specific day in the ipothesis of a linear growth from the regulament day and the maturity date
        theoric_price = bot.issuance_price + (100 - bot.issuance_price)*(passed_duration/duration)
        clean_price = purchase_data.purchase_price * quantity
        commission = bank_fee_policy.calculate(clean_price)
        tax = TaxFeePolicy().calculate(bot, purchase_data)
        total_cost = clean_price + commission + tax
        purchase_costs = PurchaseCosts(clean_price, commission, tax, total_cost)
        purchase_price_capital_gain=(clean_price + commission)/quantity-(theoric_price-bot.issuance_price)
        realized_gain_loss = (bot.issuance_price - purchase_price_capital_gain)*quantity
        if portfolio.capital_loss > realized_gain_loss:
            taxable_amount = 0
        else:
            taxable_amount = realized_gain_loss - portfolio.capital_loss
        capital_gain_tax = taxable_amount * 12.5
        refunded_amount = purchase_data.lot - capital_gain_tax
        if (portfolio.capital_loss - realized_gain_loss) < 0:
            remaining_gain_loss = 0
        else:
            remaining_gain_loss = portfolio.capital_loss - realized_gain_loss
        sale_amounts = SalesAmounts(purchase_price_capital_gain, taxable_amount, refunded_amount, capital_gain_tax, remaining_gain_loss)
        return purchase_costs, sale_amounts
        
if __name__ == "__main__":
    catalog = BOTCatalog()
    bot = catalog.get_bot("Bot Zc Fb24 A Eur")
    fee_policy = fee_policy_manager = BankFeePolicyManager().get_bank_fee_policy("Intesa San Paolo", "MOT")
    purchase_data = PurchaseData(date(2023, 3, 1), 96.846, 5000, False)
    portfolio = Portfolio()
    bot_calculator = BOTCalculator()
    purchase_costs, sale_amounts = bot_calculator.calculate(bot, purchase_data, fee_policy, portfolio)
    print("Importo Secco: ", purchase_costs.clean_price)
    print("Commissioni: ", round(purchase_costs.commission,2))
    print("Tasse: ", round(purchase_costs.tax,2))
    print("Totale Costo: ", round(purchase_costs.total_cost,2))
    print()
    print("Importo Rimborsato: ", sale_amounts.refunded_amount)
    print("Tasse Capital Gain: ", round(sale_amounts.capital_gain_tax,2))
    print("Minus Valenza Realizzata: ", round(sale_amounts.remaining_gain_loss,2))
