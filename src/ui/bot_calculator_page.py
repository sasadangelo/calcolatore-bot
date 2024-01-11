import streamlit as st
from datetime import datetime
from src.services.bot_catalog_service import BOTCatalogService
from src.services.bot_calculator_service import BOTCalculatorService
from src.model.portfolio import Portfolio
from src.model.bot import BOT
from src.model.quote import Quote
from src.ui.page import Page
from src.ui.helper import Helper

class BOTCalculatorPage(Page):
    ISIN_KEY = "isin"
    ISSUANCE_DATE_KEY = "issuance_date"
    ISSUANCE_PRICE_KEY = "issuance_price"
    METURITY_DATE_KEY = "maturity_date"
    LAST_PRICE_KEY = "last_price"
    PURCHASE_DATE_KEY = "purchase_date"
    PURCHASE_PRICE_KEY = "purchase_price"
    COMMISSIONS_KEY = "commissions"
    MIN_COMMISSIONS_KEY = "min_commissions"
    MAX_COMMISSIONS_KEY = "max_commissions"
    FIXED_COSTS_KEY = "fixed_costs"
    LOT_KEY = "lot"
    QUANTITY_KEY = "quantity"
    DURATION_KEY = "duration"
    REMAINING_DURATION_KEY = "remaining_duration"
    ELAPSED_DURATION_KEY = "elapsed_duration"
    THEORIC_PRICE_KEY = "theoric_price"
    CLEAN_PRICE_KEY = "clean_price"
    TOTAL_COMMISSIONS_KEY = "total_commissions"
    TAX_KEY = "tax"
    TOTAL_COSTS_KEY = "total_costs"
    PURCHASE_PRICE_CAPITAL_GAIN_KEY = "purchase_price_capital_gain"
    REALIZED_GAIN_LOSS_KEY = "realized_gain_loss"
    TAXABLE_AMOUNT_KEY = "taxable_amount"
    CAPITAL_GAIN_TAX = "capital_gain_tax"
    REMAINING_GAIN_LOSS_KEY = "remaining_gain_loss"
    REFUNDED_AMOUNT_KEY = "refunded_amount"
    GROSS_TOTAL_GAIN_KEY = "gross_total_gain"
    NET_TOTAL_GAIN_KEY = "net_total_gain"
    GROSS_YIELD_KEY = "gross_yield"
    NET_YIELD_KEY = "net_yield"

    BOT_NOT_IN_CATALOG = "BOT non in Catalogo"

    def __init__(self):
        self.catalog = BOTCatalogService()
        self.bot_names = [bot.name for bot in self.catalog.get_active_bot_list()] + [BOTCalculatorPage.BOT_NOT_IN_CATALOG]

    def render(self):
        st.title("Calcolatore BOT")

        bot = st.session_state.bot
        index = self.bot_names.index(bot.name) if bot.name != "" else 0
        selected_bot_name = st.selectbox("Seleziona un BOT", self.bot_names, index)
        if selected_bot_name != st.session_state.bot.name:
            if selected_bot_name != BOTCalculatorPage.BOT_NOT_IN_CATALOG:
                bot = self.catalog.get_bot(selected_bot_name)
            else:
                bot = BOT()
            st.session_state.bot = bot
        purchase_data = st.session_state.purchase_data
        commissions_policy = st.session_state.commissions_policy

        last_price = bot.last_quote.last_price if bot and bot.last_quote else 0.000

        # Anagrafica Titolo
        with st.container(border=True):
            st.markdown("<h2 style='font-size: 20px;'>Anagrafica Titolo</h2>", unsafe_allow_html=True)
            st.text_input("ISIN", value=bot.isin, key=BOTCalculatorPage.ISIN_KEY, max_chars=12, disabled=True, help=Helper.get_help(BOTCalculatorPage.ISIN_KEY))
            bot.issuance_date = st.date_input("Data di Emissione:", value=bot.issuance_date, key=BOTCalculatorPage.ISSUANCE_DATE_KEY, disabled=(selected_bot_name != BOTCalculatorPage.BOT_NOT_IN_CATALOG), help=Helper.get_help(BOTCalculatorPage.ISSUANCE_DATE_KEY))
            bot.issuance_price = st.number_input("Prezzo di Emissione:", value=bot.issuance_price, key=BOTCalculatorPage.ISSUANCE_PRICE_KEY, disabled=(selected_bot_name != BOTCalculatorPage.BOT_NOT_IN_CATALOG), format="%.3f", step=0.001, help=Helper.get_help(BOTCalculatorPage.ISSUANCE_PRICE_KEY))
            bot.maturity_date = st.date_input("Data di Scadenza:", value=bot.maturity_date, key=BOTCalculatorPage.METURITY_DATE_KEY, disabled=(selected_bot_name != BOTCalculatorPage.BOT_NOT_IN_CATALOG), help=Helper.get_help(BOTCalculatorPage.METURITY_DATE_KEY))
            last_price = st.number_input("Quotazione:", value=last_price, key=BOTCalculatorPage.LAST_PRICE_KEY, disabled=True, format="%.3f", step=0.001, help=Helper.get_help(BOTCalculatorPage.LAST_PRICE_KEY))

        # Dati di Acquisto
        with st.container(border=True):
            st.markdown("<h2 style='font-size: 20px;'>Dati di Acquito</h2>", unsafe_allow_html=True)
            market_type = st.radio("Mercato", ["MOT", "Asta"], index=0)
            if market_type == "MOT":
                purchase_data.buy_auction = False
                purchase_data.purchase_date = st.date_input("Data di Acquisto (Regolamento):", value=purchase_data.purchase_date, key=BOTCalculatorPage.PURCHASE_DATE_KEY, disabled=False, help=Helper.get_help(BOTCalculatorPage.PURCHASE_DATE_KEY))
                purchase_data.purchase_price = st.number_input("Prezzo di Acquisto:", value=purchase_data.purchase_price, key=BOTCalculatorPage.PURCHASE_PRICE_KEY, disabled=False, format="%.3f", step=0.001, help=Helper.get_help(BOTCalculatorPage.PURCHASE_PRICE_KEY))
                commissions_policy.percentage = st.number_input("Commissioni (% sul Prezzo di Acquisto):", value=commissions_policy.percentage, key=BOTCalculatorPage.COMMISSIONS_KEY, disabled=False, format="%.2f", step=0.001, help=Helper.get_help(BOTCalculatorPage.COMMISSIONS_KEY))
            else:
                purchase_data.buy_auction = True
                purchase_data.purchase_date = bot.issuance_date
                purchase_data.purchase_price = bot.issuance_price
                purchase_data.purchase_date = st.date_input("Data di Acquisto (Regolamento):", value=purchase_data.purchase_date, key=BOTCalculatorPage.PURCHASE_DATE_KEY, disabled=True, help=Helper.get_help(BOTCalculatorPage.PURCHASE_DATE_KEY))
                purchase_data.purchase_price = st.number_input("Prezzo di Acquisto (EUR):", value=purchase_data.purchase_price, key=BOTCalculatorPage.PURCHASE_PRICE_KEY, disabled=True, format="%.3f", step=0.001, help=Helper.get_help(BOTCalculatorPage.PURCHASE_PRICE_KEY))
                commissions_policy.percentage = st.number_input("Commissioni (% sul Prezzo Nominale):", value=commissions_policy.percentage, key=BOTCalculatorPage.COMMISSIONS_KEY, disabled=False, format="%.2f", step=0.001, help=Helper.get_help(BOTCalculatorPage.COMMISSIONS_KEY))

            commissions_policy.min_value = st.number_input("Min. Commissioni (EUR):", value=commissions_policy.min_value, key=BOTCalculatorPage.MIN_COMMISSIONS_KEY, disabled=False, format="%.2f", step=0.01, help=Helper.get_help(BOTCalculatorPage.MIN_COMMISSIONS_KEY))
            if commissions_policy.max_value == float('inf'):
                temp_max_commissions = st.number_input("Max. Commissioni (EUR)", value=None, key=BOTCalculatorPage.MAX_COMMISSIONS_KEY, disabled=False, format="%.2f", step=0.001, help=Helper.get_help(BOTCalculatorPage.MAX_COMMISSIONS_KEY))
            else:
                temp_max_commissions = st.number_input("Max. Commissioni (EUR)", value=commissions_policy.max_value, key=BOTCalculatorPage.MAX_COMMISSIONS_KEY, disabled=False, format="%.2f", step=0.001, help=Helper.get_help(BOTCalculatorPage.MAX_COMMISSIONS_KEY))
            if temp_max_commissions != None:
                commissions_policy.max_value = temp_max_commissions
            else:
                commissions_policy.max_value = float('inf')

            commissions_policy.fixed = st.number_input("Costi Fissi (EUR)", value=commissions_policy.fixed, key=BOTCalculatorPage.FIXED_COSTS_KEY, disabled=False, format="%.2f", step=0.01, help=Helper.get_help(BOTCalculatorPage.FIXED_COSTS_KEY))
            purchase_data.lot = st.number_input("Lotto (Importo Nominale in EUR)", value=purchase_data.lot, key=BOTCalculatorPage.LOT_KEY, min_value=0, disabled=False, format="%d", step=1000, help=Helper.get_help(BOTCalculatorPage.LOT_KEY))
        bot_calculator = BOTCalculatorService()
        portfolio = Portfolio()
        purchase_costs, sale_amounts = bot_calculator.calculate(bot, purchase_data, commissions_policy, portfolio)

        # Informazioni BOT
        with st.container(border=True):
            st.markdown("<h2 style='font-size: 20px;'>Informazioni BOT</h2>", unsafe_allow_html=True)
            quantity = purchase_data.lot//100
            duration = bot.get_duration() if bot else 0
            remaining_duration = bot.get_remaining_duration(purchase_data.purchase_date) if bot else 0
            passed_duration = bot.get_passed_duration(purchase_data.purchase_date) if bot else 0
            theoric_price = bot.get_theoric_price(purchase_data.purchase_date) if bot else 0.00
            st.number_input("Quantità:", value=quantity, key=BOTCalculatorPage.QUANTITY_KEY, disabled=True, format="%d", step=1, help=Helper.get_help(BOTCalculatorPage.QUANTITY_KEY))
            st.number_input("Durata totale (giorni):", value=duration, key=BOTCalculatorPage.DURATION_KEY, disabled=True, format="%d", step=1, help=Helper.get_help(BOTCalculatorPage.DURATION_KEY))
            st.number_input("Durata residua (giorni):", value=remaining_duration, key=BOTCalculatorPage.REMAINING_DURATION_KEY, disabled=True, format="%d", step=1, help=Helper.get_help(BOTCalculatorPage.REMAINING_DURATION_KEY))
            st.number_input("Durata trascorsa (giorni):", value=passed_duration, key=BOTCalculatorPage.ELAPSED_DURATION_KEY, disabled=True, format="%d", step=1, help=Helper.get_help(BOTCalculatorPage.ELAPSED_DURATION_KEY))
            theoric_price = st.number_input("Prezzo Teorico (EUR):", value=theoric_price, key=BOTCalculatorPage.THEORIC_PRICE_KEY, disabled=True, format="%.3f", step=0.001, help=Helper.get_help(BOTCalculatorPage.THEORIC_PRICE_KEY))

        # Importi Acquisto (Costi)
        with st.container(border=True):
            st.markdown("<h2 style='font-size: 20px;'>Importi Acquisto (Costi)</h2>", unsafe_allow_html=True)
            st.number_input("Importo Secco (EUR):", value=purchase_costs.clean_price, key=BOTCalculatorPage.CLEAN_PRICE_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(BOTCalculatorPage.CLEAN_PRICE_KEY))
            st.number_input("Commissioni + Costi Fissi (EUR):", value=purchase_costs.commission, key=BOTCalculatorPage.TOTAL_COMMISSIONS_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(BOTCalculatorPage.TOTAL_COMMISSIONS_KEY))
            st.number_input("Imposte (EUR):", value=purchase_costs.tax, key=BOTCalculatorPage.TAX_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(BOTCalculatorPage.TAX_KEY))
            st.number_input("Importo Totale da Pagare (EUR):", value=purchase_costs.total_cost, key=BOTCalculatorPage.TOTAL_COSTS_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(BOTCalculatorPage.TOTAL_COSTS_KEY))

        # Importi Vendita/Scadenza
        with st.container(border=True):
            st.markdown("<h2 style='font-size: 20px;'>Importi Vendita/Scadenza</h2>", unsafe_allow_html=True)
            st.number_input("Prezzo di Carico per il Capital Gain (EUR):", value=sale_amounts.purchase_price_capital_gain, key=BOTCalculatorPage.PURCHASE_PRICE_CAPITAL_GAIN_KEY, disabled=True, format="%.5f", step=0.00001, help=Helper.get_help(BOTCalculatorPage.PURCHASE_PRICE_CAPITAL_GAIN_KEY))
            st.number_input("Plus  (+)  Minus  (-) Valenza Realizzata (EUR):", value=sale_amounts.realized_gain_loss, key=BOTCalculatorPage.REALIZED_GAIN_LOSS_KEY, disabled=True, format="%.2f", step=0.00001, help=Helper.get_help(BOTCalculatorPage.REALIZED_GAIN_LOSS_KEY))
            st.number_input("Imponibile (EUR):", value=sale_amounts.taxable_amount, key=BOTCalculatorPage.TAXABLE_AMOUNT_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(BOTCalculatorPage.TAXABLE_AMOUNT_KEY))
            st.number_input("Imposta sulla Plus Valenza (EUR):", value=sale_amounts.capital_gain_tax, key=BOTCalculatorPage.CAPITAL_GAIN_TAX, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(BOTCalculatorPage.CAPITAL_GAIN_TAX))
            st.number_input("Minus Valenza Rimanente (EUR):", value=sale_amounts.remaining_gain_loss, key=BOTCalculatorPage.REMAINING_GAIN_LOSS_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(BOTCalculatorPage.REMAINING_GAIN_LOSS_KEY))
            st.number_input("Importo Rimborsato (EUR):", value=sale_amounts.refunded_amount, key=BOTCalculatorPage.REFUNDED_AMOUNT_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(BOTCalculatorPage.REFUNDED_AMOUNT_KEY))

        # Guadagni
        with st.container(border=True):
            st.markdown("<h2 style='font-size: 20px;'>Guadagni</h2>", unsafe_allow_html=True)
            gross_total_gain = sale_amounts.refunded_amount - purchase_costs.clean_price
            net_total_gain = sale_amounts.refunded_amount - purchase_costs.total_cost
            st.number_input("Guadagno Lordo (EUR):", value=gross_total_gain, key=BOTCalculatorPage.GROSS_TOTAL_GAIN_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(BOTCalculatorPage.GROSS_TOTAL_GAIN_KEY))
            st.number_input("Guadagno Netto al Rimborso (EUR):", value=net_total_gain, key=BOTCalculatorPage.NET_TOTAL_GAIN_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(BOTCalculatorPage.NET_TOTAL_GAIN_KEY))

        # Rendimenti
        with st.container(border=True):
            st.markdown("<h2 style='font-size: 20px;'>Rendimenti</h2>", unsafe_allow_html=True)
            gross_yield = (gross_total_gain * 100 / purchase_costs.clean_price) * (365/remaining_duration) if purchase_costs.clean_price != 0 and remaining_duration != 0 else 0.00
            net_yield = (net_total_gain * 100 / purchase_costs.total_cost) * (365/remaining_duration) if purchase_costs.total_cost != 0 and remaining_duration != 0 else 0.00
            st.number_input("Rendimento Lordo %:", value=gross_yield, key=BOTCalculatorPage.GROSS_YIELD_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(BOTCalculatorPage.GROSS_YIELD_KEY))
            st.number_input("Rendimento Netto al Rimborso %:", value=net_yield, key=BOTCalculatorPage.NET_YIELD_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(BOTCalculatorPage.NET_YIELD_KEY))