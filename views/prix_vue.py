import tkinter as tk

from observateurs.observateur import Observateur


class PrixVue(Observateur):

    def __init__(self, parent):
        self.frame_prix = tk.LabelFrame(parent, text="Prix en temps réel", padx=10, pady=10)
        self.frame_prix.pack(fill=tk.X, padx=10, pady=5)
        self.labels_prix = {}
        self.frames_prix = {}

    def actualiser(self, sujet) -> None:
        donnees = sujet.get_donnees()
        prix_actuels = donnees["prix_actuels"]
        titres = donnees["titres"]

        for ticker in titres:
            if ticker not in self.labels_prix:
                self._creer_ligne_prix(ticker)

        for ticker, (prix, ouverture) in prix_actuels.items():
            texte, couleur = self.formater_prix(prix, ouverture)

            self.labels_prix[ticker].config(text=texte, fg=couleur)

        for ticker in list(self.labels_prix):
            if ticker not in titres:
                self.labels_prix.pop(ticker)
                self.frames_prix.pop(ticker).destroy()

    def _creer_ligne_prix(self, ticker):
        frame = tk.Frame(self.frame_prix)
        frame.pack(fill=tk.X, pady=2)
        tk.Label(frame, text=f"{ticker}:", width=8, font=("Segoe UI", 10, "bold"), anchor="w").pack(side=tk.LEFT)
        label = tk.Label(frame, text="Chargement...")
        label.pack(side=tk.LEFT)
        self.labels_prix[ticker] = label
        self.frames_prix[ticker] = frame

    def formater_prix(self, prix, ouverture):
        variation = (prix - ouverture) / ouverture * 100
        symbole = "▲" if variation >= 0 else "▼"
        couleur = "green" if variation >= 0 else "red"

        return f"{prix:.2f} $  {symbole} {abs(variation):.2f}%", couleur