import streamlit as st
from datetime import datetime
from src.services.bot_catalog_service import BOTCatalogService
from src.services.bot_calculator_service import BOTCalculatorService
from src.model.portfolio import Portfolio
from src.model.bot import BOT
from src.ui.page import Page
from src.ui.helper import Helper
from src.ui.session_state_keys import SessionStateKeys

class BOTCalculatorPage(Page):
    BOT_NOT_IN_CATALOG = "BOT non in Catalogo"

    def __init__(self):
        self.catalog = BOTCatalogService()
        self.bot_names = [bot.name for bot in self.catalog.get_active_bot_list()] + [BOTCalculatorPage.BOT_NOT_IN_CATALOG]

    def __validate_purchase_date(self):
        issuance_date=st.session_state[SessionStateKeys.ISSUANCE_DATE_KEY]
        maturity_date=st.session_state[SessionStateKeys.METURITY_DATE_KEY]
        purchase_date=st.session_state[SessionStateKeys.PURCHASE_DATE_KEY]
        if not (issuance_date <= purchase_date <= maturity_date):
            st.error("La Data di Acquisto (Regolamento) deve essere compresa tra la Data di Emissione e la Data di Scadenza.")
            return False
        return True

    def __validate_issuance_date(self):
        issuance_date=st.session_state[SessionStateKeys.ISSUANCE_DATE_KEY]
        maturity_date=st.session_state[SessionStateKeys.METURITY_DATE_KEY]
        if (issuance_date > maturity_date):
            st.error("La Data di Emissione deve essere precedente o uguale alla Data di Scadenza.")
            return False
        return True

    def __validate_maturity_date(self):
        issuance_date=st.session_state[SessionStateKeys.ISSUANCE_DATE_KEY]
        maturity_date=st.session_state[SessionStateKeys.METURITY_DATE_KEY]
        if (maturity_date < issuance_date):
            st.error("La Data di Scadenza deve essere successiva o uguale alla Data di Emissione.")
            return False
        return True

    def __validate_lot(self):
        lot=st.session_state[SessionStateKeys.LOT_KEY]
        if lot < 0 or (lot % 1000 != 0):
            st.error("Il Lotto deve essere 0 o un multiplo di 1000.")
            return False

        return True

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
            st.text_input("ISIN", value=bot.isin, key=SessionStateKeys.ISIN_KEY, max_chars=12, disabled=True, help=Helper.get_help(SessionStateKeys.ISIN_KEY))
            bot.issuance_date = st.date_input("Data di Emissione:", value=bot.issuance_date, key=SessionStateKeys.ISSUANCE_DATE_KEY, disabled=(selected_bot_name != BOTCalculatorPage.BOT_NOT_IN_CATALOG), format="DD/MM/YYYY", on_change=self.__validate_issuance_date, help=Helper.get_help(SessionStateKeys.ISSUANCE_DATE_KEY))
            bot.issuance_price = st.number_input("Prezzo di Emissione:", value=bot.issuance_price, key=SessionStateKeys.ISSUANCE_PRICE_KEY, disabled=(selected_bot_name != BOTCalculatorPage.BOT_NOT_IN_CATALOG), format="%.3f", step=0.001, help=Helper.get_help(SessionStateKeys.ISSUANCE_PRICE_KEY))
            bot.maturity_date = st.date_input("Data di Scadenza:", value=bot.maturity_date, key=SessionStateKeys.METURITY_DATE_KEY, disabled=(selected_bot_name != BOTCalculatorPage.BOT_NOT_IN_CATALOG), format="DD/MM/YYYY", on_change=self.__validate_maturity_date, help=Helper.get_help(SessionStateKeys.METURITY_DATE_KEY))
            last_price = st.number_input("Quotazione:", value=last_price, key=SessionStateKeys.LAST_PRICE_KEY, disabled=True, format="%.3f", step=0.001, help=Helper.get_help(SessionStateKeys.LAST_PRICE_KEY))

        # Dati di Acquisto
        with st.container(border=True):
            st.markdown("<h2 style='font-size: 20px;'>Dati di Acquito</h2>", unsafe_allow_html=True)
            market_type = st.radio("Mercato", ["MOT", "Asta"], index=0)
            if market_type == "MOT":
                purchase_data.buy_auction = False
                purchase_data.purchase_date = st.date_input("Data di Acquisto (Regolamento):", value=purchase_data.purchase_date, key=SessionStateKeys.PURCHASE_DATE_KEY, disabled=False, format="DD/MM/YYYY", on_change=self.__validate_purchase_date, help=Helper.get_help(SessionStateKeys.PURCHASE_DATE_KEY))
                purchase_data.purchase_price = st.number_input("Prezzo di Acquisto:", value=purchase_data.purchase_price, key=SessionStateKeys.PURCHASE_PRICE_KEY, disabled=False, format="%.3f", step=0.001, help=Helper.get_help(SessionStateKeys.PURCHASE_PRICE_KEY))
                commissions_policy.percentage = st.number_input("Commissioni (% sul Prezzo di Acquisto):", value=commissions_policy.percentage, key=SessionStateKeys.COMMISSIONS_KEY, disabled=False, format="%.2f", step=0.001, help=Helper.get_help(SessionStateKeys.COMMISSIONS_KEY))
            else:
                purchase_data.buy_auction = True
                purchase_data.purchase_date = bot.issuance_date
                purchase_data.purchase_price = bot.issuance_price
                purchase_data.purchase_date = st.date_input("Data di Acquisto (Regolamento):", value=purchase_data.purchase_date, key=SessionStateKeys.PURCHASE_DATE_KEY, disabled=True, format="DD/MM/YYYY", help=Helper.get_help(SessionStateKeys.PURCHASE_DATE_KEY))
                purchase_data.purchase_price = st.number_input("Prezzo di Acquisto (EUR):", value=purchase_data.purchase_price, key=SessionStateKeys.PURCHASE_PRICE_KEY, disabled=True, format="%.3f", step=0.001, help=Helper.get_help(SessionStateKeys.PURCHASE_PRICE_KEY))
                commissions_policy.percentage = st.number_input("Commissioni (% sul Prezzo Nominale):", value=commissions_policy.percentage, key=SessionStateKeys.COMMISSIONS_KEY, disabled=False, format="%.2f", step=0.001, help=Helper.get_help(SessionStateKeys.COMMISSIONS_KEY))

            commissions_policy.min_value = st.number_input("Min. Commissioni (EUR):", value=commissions_policy.min_value, key=SessionStateKeys.MIN_COMMISSIONS_KEY, disabled=False, format="%.2f", step=0.01, help=Helper.get_help(SessionStateKeys.MIN_COMMISSIONS_KEY))
            if commissions_policy.max_value == float('inf'):
                temp_max_commissions = st.number_input("Max. Commissioni (EUR)", value=None, key=SessionStateKeys.MAX_COMMISSIONS_KEY, disabled=False, format="%.2f", step=0.001, help=Helper.get_help(SessionStateKeys.MAX_COMMISSIONS_KEY))
            else:
                temp_max_commissions = st.number_input("Max. Commissioni (EUR)", value=commissions_policy.max_value, key=SessionStateKeys.MAX_COMMISSIONS_KEY, disabled=False, format="%.2f", step=0.001, help=Helper.get_help(SessionStateKeys.MAX_COMMISSIONS_KEY))
            if temp_max_commissions != None:
                commissions_policy.max_value = temp_max_commissions
            else:
                commissions_policy.max_value = float('inf')

            commissions_policy.fixed = st.number_input("Costi Fissi (EUR)", value=commissions_policy.fixed, key=SessionStateKeys.FIXED_COSTS_KEY, disabled=False, format="%.2f", step=0.01, help=Helper.get_help(SessionStateKeys.FIXED_COSTS_KEY))
            purchase_data.lot = st.number_input("Lotto (Importo Nominale in EUR)", value=purchase_data.lot, key=SessionStateKeys.LOT_KEY, min_value=0, disabled=False, format="%d", step=1000, on_change=self.__validate_lot, help=Helper.get_help(SessionStateKeys.LOT_KEY))
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
            st.number_input("Quantità:", value=quantity, key=SessionStateKeys.QUANTITY_KEY, disabled=True, format="%d", step=1, help=Helper.get_help(SessionStateKeys.QUANTITY_KEY))
            st.number_input("Durata totale (giorni):", value=duration, key=SessionStateKeys.DURATION_KEY, disabled=True, format="%d", step=1, help=Helper.get_help(SessionStateKeys.DURATION_KEY))
            st.number_input("Durata residua (giorni):", value=remaining_duration, key=SessionStateKeys.REMAINING_DURATION_KEY, disabled=True, format="%d", step=1, help=Helper.get_help(SessionStateKeys.REMAINING_DURATION_KEY))
            st.number_input("Durata trascorsa (giorni):", value=passed_duration, key=SessionStateKeys.ELAPSED_DURATION_KEY, disabled=True, format="%d", step=1, help=Helper.get_help(SessionStateKeys.ELAPSED_DURATION_KEY))
            theoric_price = st.number_input("Prezzo Teorico (EUR):", value=theoric_price, key=SessionStateKeys.THEORIC_PRICE_KEY, disabled=True, format="%.5f", step=0.001, help=Helper.get_help(SessionStateKeys.THEORIC_PRICE_KEY))

        # Importi Acquisto (Costi)
        with st.container(border=True):
            st.markdown("<h2 style='font-size: 20px;'>Importi Acquisto (Costi)</h2>", unsafe_allow_html=True)
            st.number_input("Importo Secco (EUR):", value=purchase_costs.clean_price, key=SessionStateKeys.CLEAN_PRICE_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(SessionStateKeys.CLEAN_PRICE_KEY))
            st.number_input("Commissioni + Costi Fissi (EUR):", value=purchase_costs.commission, key=SessionStateKeys.TOTAL_COMMISSIONS_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(SessionStateKeys.TOTAL_COMMISSIONS_KEY))
            st.number_input("Imposte (EUR):", value=purchase_costs.tax, key=SessionStateKeys.TAX_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(SessionStateKeys.TAX_KEY))
            st.number_input("Importo Totale da Pagare (EUR):", value=purchase_costs.total_cost, key=SessionStateKeys.TOTAL_COSTS_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(SessionStateKeys.TOTAL_COSTS_KEY))

        # Importi Vendita/Scadenza
        with st.container(border=True):
            st.markdown("<h2 style='font-size: 20px;'>Importi Vendita/Scadenza</h2>", unsafe_allow_html=True)
            st.number_input("Prezzo di Carico per il Capital Gain (EUR):", value=sale_amounts.purchase_price_capital_gain, key=SessionStateKeys.PURCHASE_PRICE_CAPITAL_GAIN_KEY, disabled=True, format="%.5f", step=0.00001, help=Helper.get_help(SessionStateKeys.PURCHASE_PRICE_CAPITAL_GAIN_KEY))
            st.number_input("Plus  (+)  Minus  (-) Valenza Realizzata (EUR):", value=sale_amounts.realized_gain_loss, key=SessionStateKeys.REALIZED_GAIN_LOSS_KEY, disabled=True, format="%.2f", step=0.00001, help=Helper.get_help(SessionStateKeys.REALIZED_GAIN_LOSS_KEY))
            st.number_input("Imponibile (EUR):", value=sale_amounts.taxable_amount, key=SessionStateKeys.TAXABLE_AMOUNT_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(SessionStateKeys.TAXABLE_AMOUNT_KEY))
            st.number_input("Imposta sulla Plus Valenza (EUR):", value=sale_amounts.capital_gain_tax, key=SessionStateKeys.CAPITAL_GAIN_TAX, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(SessionStateKeys.CAPITAL_GAIN_TAX))
            st.number_input("Importo Rimborsato (EUR):", value=sale_amounts.refunded_amount, key=SessionStateKeys.REFUNDED_AMOUNT_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(SessionStateKeys.REFUNDED_AMOUNT_KEY))

        # Guadagni
        with st.container(border=True):
            st.markdown("<h2 style='font-size: 20px;'>Guadagni</h2>", unsafe_allow_html=True)
            gross_total_gain = sale_amounts.refunded_amount - purchase_costs.clean_price
            net_total_gain = sale_amounts.refunded_amount - purchase_costs.total_cost
            st.number_input("Guadagno Lordo (EUR):", value=gross_total_gain, key=SessionStateKeys.GROSS_TOTAL_GAIN_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(SessionStateKeys.GROSS_TOTAL_GAIN_KEY))
            st.number_input("Guadagno Netto al Rimborso (EUR):", value=net_total_gain, key=SessionStateKeys.NET_TOTAL_GAIN_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(SessionStateKeys.NET_TOTAL_GAIN_KEY))

        # Rendimenti
        with st.container(border=True):
            st.markdown("<h2 style='font-size: 20px;'>Rendimenti</h2>", unsafe_allow_html=True)
            gross_yield = (gross_total_gain * 100 / purchase_costs.clean_price) * (365/remaining_duration) if purchase_costs.clean_price != 0 and remaining_duration != 0 else 0.00
            net_yield = (net_total_gain * 100 / purchase_costs.total_cost) * (365/remaining_duration) if purchase_costs.total_cost != 0 and remaining_duration != 0 else 0.00
            st.number_input("Rendimento Lordo %:", value=gross_yield, key=SessionStateKeys.GROSS_YIELD_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(SessionStateKeys.GROSS_YIELD_KEY))
            st.number_input("Rendimento Netto al Rimborso %:", value=net_yield, key=SessionStateKeys.NET_YIELD_KEY, disabled=True, format="%.2f", step=0.01, help=Helper.get_help(SessionStateKeys.NET_YIELD_KEY))