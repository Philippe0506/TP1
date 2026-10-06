import tkinter as tk

from observateur import Observateur


class AlertesVue(Observateur):

    def __init__(self, parent):
        self.frame_alertes = tk.LabelFrame(parent, text="Alertes", padx=10, pady=10)
        self.frame_alertes.pack(fill=tk.X, padx=10, pady=5)
        self.label_alertes = tk.Label(self.frame_alertes, text="Aucune alerte", fg="gray", justify=tk.LEFT, wraplength=380)
        self.label_alertes.pack(anchor="w")

    def actualiser(self, sujet) -> None:
        donnees = sujet.get_donnees()
        alertes = donnees["alertes"]

        self.label_alertes.config(text="\n".join(alertes) if alertes else "Aucune alerte",fg="red" if alertes else "gray")