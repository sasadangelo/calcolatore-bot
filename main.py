from bot_catalog import BOTCatalog
from tabulate import tabulate

# Esempio di utilizzo della classe BOTCatalog
if __name__ == "__main__":
    catalog = BOTCatalog()

    # Ottenere la lista di tutti i BOT
    bot_list = catalog.get_bot_list()

    # Creare una lista di tuple con i dati dei BOT
    table_data = []

    # Aggiungere la colonna del Rendimento Emissione
    for bot in bot_list:
        duration = (bot.maturity_date - bot.issuance_date).days
        gain = 100 - bot.issuance_price
        yield_percent = (gain * 100) / bot.issuance_price * (365 / duration) if duration != 0 else 0
        table_data.append((bot.name, bot.isin, bot.issuance_date, bot.issuance_price, bot.maturity_date, "{:.2f}%".format(yield_percent)))

    # Stampa la tabella formattata
    headers = ["Nome BOT", "ISIN", "Data E.", "Prezzo E.", "Scadenza", "Rendimento E. Lordo"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
