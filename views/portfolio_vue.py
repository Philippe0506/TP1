import tkinter as tk

from observateurs.observateur import Observateur


class PortfolioVue(Observateur):

    def __init__(self, parent):
        self.parent = parent

        self._construire_gestion()

        self.frame_portfolio = tk.LabelFrame(parent, text="Mon portfolio", padx=10, pady=10)
        self.frame_portfolio.pack(fill=tk.X, padx=10, pady=5)

        self.label_valeur = tk.Label(self.frame_portfolio, text="Valeur totale : calcul en cours...", font=("Segoe UI", 13, "bold"))
        self.label_valeur.pack()

        self.label_variation = tk.Label(self.frame_portfolio, text="")
        self.label_variation.pack()

    def _construire_gestion(self):
        self.frame_gestion = tk.LabelFrame(self.parent, text="Gérer les titres", padx=10, pady=10)
        self.frame_gestion.pack(fill=tk.X, padx=10, pady=5)

        frame_ajout = tk.Frame(self.frame_gestion)
        frame_ajout.pack(fill=tk.X, pady=5)

        self.entry_ticker = self._champ(frame_ajout, "Ticker :", 0)

        self.entry_quantite = self._champ(frame_ajout, "Quantité :", 1)

        self.entry_seuil_bas = self._champ(frame_ajout, "Seuil bas :", 2)

        self.entry_seuil_haut = self._champ(frame_ajout, "Seuil haut :", 3)

        tk.Button(
            frame_ajout,
            text="Ajouter",
            command=self.ajouter_titre
        ).grid(row=0, column=8, padx=5)

        self.listbox = tk.Listbox(
            self.frame_gestion,
            height=6
        )
        self.listbox.pack(fill=tk.X, pady=5)

        tk.Button(
            self.frame_gestion,
            text="Retirer",
            command=self.retirer_titre
        ).pack(pady=3)

        frame_modification = tk.Frame(self.frame_gestion)
        frame_modification.pack(fill=tk.X, pady=5)

        self.entry_modif_quantite = self._champ(
            frame_modification,
            "Nouvelle quantité :",
            0
        )

        self.entry_modif_seuil_bas = self._champ(
            frame_modification,
            "Nouveau seuil bas :",
            1
        )

        self.entry_modif_seuil_haut = self._champ(
            frame_modification,
            "Nouveau seuil haut :",
            2
        )

        tk.Button(
            frame_modification,
            text="Modifier",
            command=self.modifier_selection
        ).grid(row=0, column=6, padx=5)

        self.label_statut = tk.Label(
            self.frame_gestion,
            text=""
        )
        self.label_statut.pack()

    def _champ(self, parent, texte, colonne):
        tk.Label(
            parent,
            text=texte
        ).grid(row=0, column=colonne * 2, padx=3)

        entry = tk.Entry(parent, width=10)
        entry.grid(row=0, column=colonne * 2 + 1, padx=3)

        return entry

    def _texte_listbox(self, ticker, donnees):
        return (
            f"{ticker} — {donnees['quantite']} action(s) "
            f"(alerte : {donnees['seuil_bas']:.2f} $ / "
            f"{donnees['seuil_haut']:.2f} $)"
        )

    def _rafraichir_ligne_listbox(self, index, ticker, donnees):
        self.listbox.delete(index)
        self.listbox.insert(
            index,
            self._texte_listbox(ticker, donnees)
        )

    def _ticker_selectionne(self, titres):
        selection = self.listbox.curselection()

        if not selection:
            return None

        index = selection[0]
        ticker = list(titres.keys())[index]

        return index, ticker

    def _statut(self, texte, couleur):
        self.label_statut.config(
            text=texte,
            fg=couleur
        )

    def ajouter_titre(self):
        ticker = self.entry_ticker.get().strip().upper()
        quantite_texte = self.entry_quantite.get().strip()
        seuil_bas_texte = self.entry_seuil_bas.get().strip()
        seuil_haut_texte = self.entry_seuil_haut.get().strip()

        if not ticker:
            self._statut("Veuillez entrer un ticker.", "red")
            return

        try:
            quantite = int(quantite_texte)
        except ValueError:
            self._statut("La quantité doit être un nombre entier.", "red")
            return

        if quantite <= 0:
            self._statut("La quantité doit être positive.", "red")
            return

        try:
            seuil_bas = (
                float(seuil_bas_texte)
                if seuil_bas_texte
                else None
            )

            seuil_haut = (
                float(seuil_haut_texte)
                if seuil_haut_texte
                else None
            )
        except ValueError:
            self._statut("Les seuils doivent être des nombres.", "red")
            return

        if seuil_bas is not None and seuil_bas <= 0:
            self._statut("Le seuil bas doit être positif.", "red")
            return

        if seuil_haut is not None and seuil_haut <= 0:
            self._statut("Le seuil haut doit être positif.", "red")
            return

        try:
            self.sujet.ajouter_titre(
                ticker,
                quantite,
                seuil_bas,
                seuil_haut
            )

            self.entry_ticker.delete(0, tk.END)
            self.entry_quantite.delete(0, tk.END)
            self.entry_seuil_bas.delete(0, tk.END)
            self.entry_seuil_haut.delete(0, tk.END)

            self._statut(
                f"{ticker} ajouté avec succès.",
                "green"
            )

        except Exception as e:
            self._statut(str(e), "red")

    def retirer_titre(self):
        donnees = self.sujet.get_donnees()
        titres = donnees["titres"]

        resultat = self._ticker_selectionne(titres)

        if resultat is None:
            self._statut(
                "Veuillez sélectionner un titre.",
                "red"
            )
            return

        index, ticker = resultat

        self.sujet.retirer_titre(ticker)

        self._statut(
            f"{ticker} retiré avec succès.",
            "green"
        )

    def modifier_selection(self):
        donnees = self.sujet.get_donnees()
        titres = donnees["titres"]

        resultat = self._ticker_selectionne(titres)

        if resultat is None:
            self._statut(
                "Veuillez sélectionner un titre.",
                "red"
            )
            return

        index, ticker = resultat

        quantite_texte = self.entry_modif_quantite.get().strip()
        seuil_bas_texte = self.entry_modif_seuil_bas.get().strip()
        seuil_haut_texte = self.entry_modif_seuil_haut.get().strip()

        nouvelle_quantite = None
        nouveau_seuil_bas = None
        nouveau_seuil_haut = None

        if quantite_texte:
            try:
                nouvelle_quantite = int(quantite_texte)
            except ValueError:
                self._statut(
                    "La quantité doit être un nombre entier.",
                    "red"
                )
                return

            if nouvelle_quantite <= 0:
                self._statut(
                    "La quantité doit être positive.",
                    "red"
                )
                return

        if seuil_bas_texte:
            try:
                nouveau_seuil_bas = float(seuil_bas_texte)
            except ValueError:
                self._statut(
                    "Le seuil bas doit être un nombre.",
                    "red"
                )
                return

            if nouveau_seuil_bas <= 0:
                self._statut(
                    "Le seuil bas doit être positif.",
                    "red"
                )
                return

        if seuil_haut_texte:
            try:
                nouveau_seuil_haut = float(seuil_haut_texte)
            except ValueError:
                self._statut(
                    "Le seuil haut doit être un nombre.",
                    "red"
                )
                return

            if nouveau_seuil_haut <= 0:
                self._statut(
                    "Le seuil haut doit être positif.",
                    "red"
                )
                return

        if (nouveau_seuil_bas is None) != (nouveau_seuil_haut is None):
            self._statut(
                "Veuillez entrer les deux seuils.",
                "red"
            )
            return

        self.sujet.modifier_titre(
            ticker,
            nouvelle_quantite,
            nouveau_seuil_bas,
            nouveau_seuil_haut
        )

        self.entry_modif_quantite.delete(0, tk.END)
        self.entry_modif_seuil_bas.delete(0, tk.END)
        self.entry_modif_seuil_haut.delete(0, tk.END)

        self._statut(
            f"{ticker} modifié avec succès.",
            "green"
        )

    def actualiser(self, sujet) -> None:
        self.sujet = sujet

        donnees = sujet.get_donnees()

        valeur_totale = donnees["valeur_totale"]
        variation_portfolio = donnees["variation_globale"]
        titres = donnees["titres"]

        self.label_valeur.config(
            text=f"Valeur totale : {valeur_totale:.2f} $"
        )

        symbole = "▲" if variation_portfolio >= 0 else "▼"

        self.label_variation.config(
            text=f"{symbole} {abs(variation_portfolio):.2f} $ depuis l'ouverture",
            fg="green" if variation_portfolio >= 0 else "red"
        )

        self.listbox.delete(0, tk.END)

        for ticker, donnees_titre in titres.items():
            self.listbox.insert(
                tk.END,
                self._texte_listbox(ticker, donnees_titre)
            )