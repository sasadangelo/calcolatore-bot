from src.services.bot_catalog_service import BOTCatalogService

# Aggiorna il file delle emissioni data/emissioni.csv
if __name__ == "__main__":
    catalog = BOTCatalogService()
    catalog.update()
    catalog.save()