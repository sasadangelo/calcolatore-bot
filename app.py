import streamlit as st
from streamlit_option_menu import option_menu
from src.ui.bot_catalog_page import BOTCatalogPage
from src.ui.bot_calculator_page import BOTCalculatorPage

#def update_catalog():
#    catalog = BOTCatalog()
#    catalog.update()
#    catalog.save()
#    print("Catalogo BOT aggiornato con successo!")

def Singleton(cls):
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@Singleton
class BOTApp:
    # The constructor load all the activities in the gpx folder of the logged in user.
    def __init__(self):
        self.current_page = None

    # Runs the TrainingApp and initializes the first page as ActivityOverviewPage.
    def run(self):
        self.__create_sidebar_menu()

    # Selects and renders the current page based on user navigation logic.
    def select_page(self, page):
        # Here you can add logic for navigating between different pages.
        # For example, if you want to show the ActivityOverviewPage as the initial page:
        self.current_page = page
        self.current_page.render()

    # Create the sidebar menu with two options:
    # - Activities, it shows all the athlete's activities
    # - Profile, it shows the athlete's profile
    def __create_sidebar_menu(self):
        with st.sidebar:
            menu_choice = option_menu("Menu", ["Calcolatore BOT", "Catalogo BOT"], 
                icons=['calculator', 'list'], menu_icon="cast", default_index=0)

        # Select the page to show depending on the menu option the user selected
        if menu_choice == "Calcolatore BOT":
            self.select_page(BOTCalculatorPage())
        if menu_choice == "Catalogo BOT":
            self.select_page(BOTCatalogPage())

if __name__ == "__main__":
    app = BOTApp()
    app.run()
