class TaxFeePolicy:
    def calculate(self, bot, purchase_data):
        quantity = purchase_data.lot / 100
        duration = bot.maturity_date - bot.issuance_date
        remaining_duration = bot.maturity_date - purchase_data.purchase_date
        tax = (100 - bot.issuance_price) * quantity * 0.125 * (remaining_duration / duration)
        return tax
