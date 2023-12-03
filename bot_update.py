from bot_catalog import BOTCatalog

# Aggiorna il file delle emissioni data/emissioni.csv
if __name__ == "__main__":
    catalog = BOTCatalog()
    catalog.update()
    catalog.save()