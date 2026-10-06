import tkinter as tk

from modeles.portfolio import PortfolioSubject
from views.prix_vue import PrixVue
from views.alertes_vue import AlertesVue
from views.portfolio_vue import PortfolioVue
from observateurs.csv_logger import CsvLoggerObserver


class App:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Portfolio Tracker")
        self.fenetre.resizable(False, False)

        self.sujet = PortfolioSubject(self.fenetre)

        self.prix_vue = PrixVue(self.fenetre)
        self.portfolio_vue = PortfolioVue(self.fenetre)
        self.alertes_vue = AlertesVue(self.fenetre)

        self.csv_logger = CsvLoggerObserver()

        self.sujet.abonner(self.prix_vue)
        self.sujet.abonner(self.portfolio_vue)
        self.sujet.abonner(self.alertes_vue)
        self.sujet.abonner(self.csv_logger)

        self.sujet.rafraichir()

        self.fenetre.mainloop()


if __name__ == "__main__":
    App()