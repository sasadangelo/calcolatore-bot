from bot_catalog import BOTCatalog

if __name__ == "__main__":
    catalog = BOTCatalog('data/emissioni.csv')
    bot_list = catalog.get_bot_list()

    for bot in bot_list:
        print(f"Nome BOT: {bot.nome}")
        print(f"ISIN: {bot.isin}")
        print(f"Data Emissione: {bot.data_emissione}")
        print(f"Prezzo Emissione: {bot.prezzo_emissione:.3f}")
        print(f"Scadenza: {bot.scadenza}")
        print()
