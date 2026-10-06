import os
from observateurs.observateur import Observateur


class CsvLoggerObserver(Observateur):

    def __init__(self, fichier_csv="portfolio.csv"):
        self.fichier_csv = fichier_csv
        self._initialiser_fichier()

    def _initialiser_fichier(self) -> None:
        if not os.path.exists(self.fichier_csv):
            with open(self.fichier_csv, "w") as f:
                f.write("horodatage,valeur_totale,variation_globale,alertes\n")

    def actualiser(self, sujet) -> None:
        donnees = sujet.get_donnees()

        if donnees["erreur"]:
            return

        horodatage = donnees["horodatage"]
        valeur_totale = donnees["valeur_totale"]
        variation_globale = donnees["variation_globale"]

        if donnees["alertes"]:
            alertes = " | ".join(donnees["alertes"])
        else:
            alertes = "Aucune alerte"

        with open(self.fichier_csv, "a") as f:
            f.write(f"{horodatage},{valeur_totale:.2f},{variation_globale:.2f},{alertes}\n")