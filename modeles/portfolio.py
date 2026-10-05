import yfinance as yf
from datetime import datetime
from modeles.sujet import Sujet


class PortfolioSubject(Sujet):
    def __init__(self, fenetre, intervalle_ms=30000):
        super().__init__()
        self.fenetre = fenetre
        self.intervalle_ms = intervalle_ms

        self.titres = {
            "AAPL":  {"quantite": 10, "seuil_haut": 200.0, "seuil_bas": 150.0},
            "GOOGL": {"quantite": 5,  "seuil_haut": 160.0, "seuil_bas": 120.0},
            "MSFT":  {"quantite": 8,  "seuil_haut": 430.0, "seuil_bas": 380.0},
        }

        self._prix_actuels = {}
        self._valeur_totale = 0.0
        self._variation_globale = 0.0
        self._alertes = []
        self._horodatage = ""
        self._erreur = None

    def get_donnees(self) -> dict:
        return {
            "titres": self.titres,
            "prix_actuels": self._prix_actuels,
            "valeur_totale": self._valeur_totale,
            "variation_globale": self._variation_globale,
            "alertes": self._alertes,
            "horodatage": self._horodatage,
            "erreur": self._erreur,
        }

    def _recuperer_prix(self, ticker):
        info = yf.Ticker(ticker).fast_info
        prix = info["last_price"]
        if prix is None:
            raise ValueError(f"Le titre '{ticker}' n'existe pas.")
        return prix, info["open"]

    def rafraichir(self) -> None:
        try:
            prix_actuels = {ticker: self._recuperer_prix(ticker) for ticker in self.titres}
            self._prix_actuels = prix_actuels

            valeur_totale = sum(prix * self.titres[t]["quantite"] for t, (prix, _) in prix_actuels.items())
            valeur_ouverture = sum(ouv * self.titres[t]["quantite"] for t, (_, ouv) in prix_actuels.items())
            self._valeur_totale = valeur_totale
            self._variation_globale = valeur_totale - valeur_ouverture

            alertes = []
            for ticker, (prix, _) in prix_actuels.items():
                if prix >= self.titres[ticker]["seuil_haut"]:
                    alertes.append(f"⚠️ {ticker} dépasse le seuil haut ({prix:.2f} $ ≥ {self.titres[ticker]['seuil_haut']:.2f} $)")
                elif prix <= self.titres[ticker]["seuil_bas"]:
                    alertes.append(f"⚠️ {ticker} sous le seuil bas ({prix:.2f} $ ≤ {self.titres[ticker]['seuil_bas']:.2f} $)")
            self._alertes = alertes
            self._horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._erreur = None

        except Exception as e:
            self._erreur = str(e)

        self.notifier()

        self.fenetre.after(self.intervalle_ms, self.rafraichir)

    def ajouter_titre(self, ticker: str, quantite: int, seuil_bas=None, seuil_haut=None):
            ticker = ticker.strip().upper()
            if not ticker or ticker in self.titres:
                raise ValueError(f"Le titre '{ticker}' est invalide ou déjà présent.")

            donnees = self._recuperer_prix(ticker)
            prix = donnees[0]

            seuil_bas_final = round(seuil_bas if seuil_bas is not None else prix * 0.8, 2)
            seuil_haut_final = round(seuil_haut if seuil_haut is not None else prix * 1.2, 2)

            self.titres[ticker] = {
                "quantite": quantite,
                "seuil_haut": seuil_haut_final,
                "seuil_bas": seuil_bas_final}

            self.rafraichir()

    def retirer_titre(self, ticker: str):
        """Retire un titre du portefeuille et notifie les observateurs."""
        ticker = ticker.strip().upper()
        if ticker in self.titres:
            del self.titres[ticker]
            self.rafraichir()


def modifier_titre(self, ticker: str, nouvelle_quantite=None, nouveau_seuil_bas=None, nouveau_seuil_haut=None):
        ticker = ticker.strip().upper()
        if ticker not in self.titres:
            return

        if nouvelle_quantite is not None:
            self.titres[ticker]["quantite"] = nouvelle_quantite
        if nouveau_seuil_bas is not None and nouveau_seuil_haut is not None:
            self.titres[ticker]["seuil_bas"] = round(nouveau_seuil_bas, 2)
            self.titres[ticker]["seuil_haut"] = round(nouveau_seuil_haut, 2)

        self.rafraichir()