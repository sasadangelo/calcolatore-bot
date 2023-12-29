import streamlit as st
import pandas as pd
from bot_catalog import BOTCatalog
from tabulate import tabulate
from datetime import datetime

def calculate_yield(bot, price_type):
    if price_type == "Emissione":
        price = bot.issuance_price
        date = bot.issuance_date
    else:
        # Se l'utente ha scelto "Ultimo" come Tipo Prezzo.
        price = bot.last_quote.ultimo_prezzo if bot.last_quote else 0
        date = bot.last_quote.ora.date() if bot.last_quote else datetime.now().date()

    duration = (bot.maturity_date - date).days
    gain = 100 - price
    yield_percent = (gain * 100) / price * (365 / duration) if duration != 0 else 0
    #return "{:.2f}%".format(yield_percent), date, "{:.3f}".format(price)
    return yield_percent, date, price

def main():
    st.title("Elenco dei BOT")

    # Carica il catalogo dei BOT
    catalog = BOTCatalog()

    # Ottieni la lista dei BOT escludendo quelli già scaduti
    current_date = datetime.now().date()
    bot_list = [bot for bot in catalog.get_bot_list() if bot.maturity_date >= current_date]

    # Creare una lista di tuple con i dati dei BOT
    table_data = []

    # Aggiungi i radio button per selezionare il "Tipo Prezzo"
    price_type = st.radio("Data - Prezzo - Rendimento", ["Ultimo", "Emissione"], index=0)  # Default a "Ultimo"

    # Aggiungere la colonna del Rendimento Emissione
    for bot in bot_list:
        yield_percent, date, price = calculate_yield(bot, price_type)
        table_data.append((bot.name, bot.isin, date.strftime('%d/%m/%Y'),
                           "{:.3f}".format(price), bot.maturity_date.strftime('%d/%m/%Y'),
                           "{:.2f}%".format(yield_percent)))

    # Definisci le intestazioni corrette
    headers = ["Nome BOT", "ISIN", "Data", "Prezzo", "Scadenza", "Rendimento Lordo"]
    df = pd.DataFrame(table_data, columns=headers)

    # Mostra la tabella utilizzando Streamlit
    st.table(df)

if __name__ == "__main__":
    main()
