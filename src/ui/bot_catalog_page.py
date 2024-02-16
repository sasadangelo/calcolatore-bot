# BOTCatalogPage - Display the BOT Catalog
#
# This class is responsible for displaying an overview of the BOT Catalog.
#
# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo sasadangelo@gmail.com
#
# This file is part of the Running Data Analysis project.
#
# SPDX-License-Identifier: MIT
import streamlit as st
import pandas as pd
from datetime import datetime
from src.services.bot_catalog_service import BOTCatalogService
from src.model.bot import BOTType
from src.ui.page import Page

class BOTCatalogPage(Page):
    def __calculate_yield(self, bot, price_type):
        if price_type == "Emissione":
            price = bot.issuance_price
            date = bot.issuance_date
            remaining_duration = bot.get_duration()
        else:
            # Se l'utente ha scelto "Ultimo" come Tipo Prezzo.
            price = bot.last_quote.last_price if bot.last_quote else 0.000
            date = bot.last_quote.quote_datetime.date() if bot.last_quote else datetime.now().date()
            remaining_duration = bot.get_remaining_duration(date)

        gain = 100 - price
        yield_percent = (gain * 100) / price * (365 / remaining_duration) if remaining_duration != 0 else 0
        return yield_percent, date, price

    def __filter_bots_by_type(self, bot_list, selected_type):
        if selected_type == "Tutti":
            return bot_list
        else:
            selected_enum = BOTType.ANNUALE if selected_type == "Annuale" else BOTType.SEMESTRALE
            return [bot for bot in bot_list if bot.type == selected_enum]

    # Renders the overview of running activities, displaying the data in a table.
    def render(self):
        st.title("Catalogo BOT")

        # Carica il catalogo dei BOT
        catalog = BOTCatalogService()

        # Imposta il lavoro programmato solo se non ci sono già lavori programmati
        #if not schedule.get_jobs(tag='update_catalog'):
        #    update_catalog_job = schedule.every().day.at("14:32", "Europe/Rome").do(update_catalog)
        #    update_catalog_job.tag('update_catalog')
        #    print("Lavoro programmato per aggiornare il catalogo dei BOT ogni giorno a mezzanotte.")
        #else:
        #    print("Lavoro programmato per aggiornare il catalogo dei BOT già impostato.")

        # Ottieni la lista dei BOT escludendo quelli già scaduti
        #current_date = datetime.now().date()
        #bot_list = [bot for bot in catalog.get_bot_list() if bot.maturity_date >= current_date]
        bot_list = catalog.get_active_bot_list()

        # Aggiungi il ComboBox per selezionare il tipo di BOT
        selected_type = st.selectbox("Tipo BOT:", ["Tutti", "Annuale", "Semestrale"], index=0)

        # Filtra i BOT in base al tipo selezionato
        filtered_bot_list = self.__filter_bots_by_type(bot_list, selected_type)

        # Creare una lista di tuple con i dati dei BOT
        table_data = []

        # Aggiungi i radio button per selezionare il "Tipo Prezzo"
        price_type = st.radio("Data - Prezzo - Rendimento", ["Ultimo", "Emissione"], index=0)  # Default a "Ultimo"

        # Aggiungere la colonna del Rendimento Emissione
        for bot in filtered_bot_list:
            yield_percent, date, price = self.__calculate_yield(bot, price_type)
            table_data.append((bot.name, bot.isin, date.strftime('%d/%m/%Y'),
                            "{:.3f}".format(price), bot.maturity_date.strftime('%d/%m/%Y'),
                            "{:.2f}%".format(yield_percent)))

        # Definisci le intestazioni corrette
        headers = ["Nome BOT", "ISIN", "Data", "Prezzo", "Scadenza", "Rendimento Lordo"]
        df = pd.DataFrame(table_data, columns=headers)

        # Mostra la tabella utilizzando Streamlit
        st.table(df)
