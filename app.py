import streamlit as st
import pandas as pd
from bot_catalog import BOTCatalog
from tabulate import tabulate

def main():
    # Carica il catalogo dei BOT
    catalog = BOTCatalog()
    catalog.update()
    catalog.save()

    # Ottieni la lista dei BOT
    bot_list = catalog.get_bot_list()

    # Creare una lista di tuple con i dati dei BOT
    table_data = []

    # Aggiungere la colonna del Rendimento Emissione
    for bot in bot_list:
        duration = (bot.maturity_date - bot.issuance_date).days
        gain = 100 - bot.issuance_price
        yield_percent = (gain * 100) / bot.issuance_price * (365 / duration) if duration != 0 else 0
        table_data.append((bot.name, bot.isin, bot.issuance_date.strftime('%d/%m/%Y'),
                           "{:.3f}".format(bot.issuance_price), bot.maturity_date.strftime('%d/%m/%Y'),
                           "{:.2f}%".format(yield_percent)))

    # Definisci le intestazioni corrette
    headers = ["Nome BOT", "ISIN", "Data Emissione", "Prezzo Emissione", "Scadenza", "Rendimento Emissione Lordo"]
    df = pd.DataFrame(table_data, columns=headers)

    # Mostra la tabella utilizzando Streamlit
    st.title("Elenco dei BOT")
    st.table(df)
    #st.table(table_data)

if __name__ == "__main__":
    main()
