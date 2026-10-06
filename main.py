import tkinter as tk

from modeles.portfolio import PortfolioSubject
from observateurs.prix_vue import PrixVue
from observateurs.alertes_vue import AlertesVue
from observateurs.portfolio_vue import PortfolioVue


class App:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Suivi de portefeuille")
        self.fenetre.resizable(False, False)

        self.sujet = PortfolioSubject(self.fenetre)

        self.prix_vue = PrixVue(self.fenetre)
        self.alertes_vue = AlertesVue(self.fenetre)
        self.portfolio_vue = PortfolioVue(self.fenetre)

        self.sujet.abonner(self.prix_vue)
        self.sujet.abonner(self.alertes_vue)
        self.sujet.abonner(self.portfolio_vue)

        self.sujet.rafraichir()

        self.fenetre.mainloop()


if __name__ == "__main__":
    App()