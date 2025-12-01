"""
Application de consultations citoyennes
Interface principale - Design épuré fond blanc
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from consultation import creer_formulaire
from contribution import creer_contribution
from synthese import afficher_synthese
from database import init_db, get_consultations, count_contributions, get_consultation_details

# Configuration des styles
FONT_TITLE = ("Segoe UI", 26, "bold")
FONT_SUBTITLE = ("Segoe UI", 16, "bold")
FONT_NORMAL = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 10)


class Application:
    def __init__(self):
        init_db()
        
        # Fenêtre principale avec thème clair
        self.root = ttk.Window(themename="litera")
        self.root.title("Plateforme de Consultation")
        self.root.state("zoomed")
        self.root.configure(bg="white")
        
        self.setup_ui()
        self.afficher_consultations()
    
    def setup_ui(self):
        """Configure l'interface principale."""
        # Container principal fond blanc
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True)
        
        # Header avec bordure
        header = ttk.Frame(main_container, padding=25)
        header.pack(fill="x")
        
        ttk.Label(
            header,
            text="Plateforme de Consultation",
            font=FONT_TITLE,
            foreground="black"
        ).pack(side="left")
        
        ttk.Button(
            header,
            text="+ Nouvelle consultation",
            bootstyle="dark-outline",
            command=self.ouvrir_formulaire,
            padding=(20, 10)
        ).pack(side="right")
        
        # Ligne de séparation noire
        separator = ttk.Frame(main_container, height=2, bootstyle="dark")
        separator.pack(fill="x")
        
        # Sous-titre
        subtitle_frame = ttk.Frame(main_container, padding=(40, 25))
        subtitle_frame.pack(fill="x")
        
        ttk.Label(
            subtitle_frame,
            text="Consultations actives",
            font=FONT_SUBTITLE,
            foreground="black"
        ).pack(anchor="w")
        
        # Zone scrollable pour les consultations
        scroll_container = ttk.Frame(main_container)
        scroll_container.pack(fill="both", expand=True, padx=40, pady=10)
        
        self.scroll_frame = ScrolledFrame(scroll_container, autohide=True)
        self.scroll_frame.pack(fill="both", expand=True)
        
        self.liste_container = self.scroll_frame
    
    def ouvrir_formulaire(self):
        """Ouvre le formulaire de création avec callback de rafraîchissement."""
        creer_formulaire(self.root, callback=self.afficher_consultations)
    
    def afficher_consultations(self):
        """Affiche la liste des consultations."""
        # Nettoyer le container
        for widget in self.liste_container.winfo_children():
            widget.destroy()
        
        consultations = get_consultations()
        
        if not consultations:
            # Message si aucune consultation
            empty_frame = ttk.Frame(self.liste_container, padding=60)
            empty_frame.pack(fill="x")
            
            ttk.Label(
                empty_frame,
                text="Aucune consultation pour le moment",
                font=FONT_NORMAL,
                foreground="gray"
            ).pack()
            
            ttk.Label(
                empty_frame,
                text="Cliquez sur \"+ Nouvelle consultation\" pour commencer",
                font=FONT_SMALL,
                foreground="gray"
            ).pack(pady=10)
            return
        
        # Afficher chaque consultation
        for cid, nom in consultations:
            self.creer_carte_consultation(cid, nom)
    
    def creer_carte_consultation(self, cid, nom):
        """Crée une carte pour une consultation."""
        details = get_consultation_details(cid)
        description = details[1] if details else ""
        nb_contrib = count_contributions(cid)
        
        # Carte principale avec bordure noire
        card_outer = ttk.Frame(self.liste_container, bootstyle="dark", padding=1)
        card_outer.pack(fill="x", pady=8)
        
        card = ttk.Frame(card_outer, padding=20)
        card.pack(fill="x")
        
        # Contenu de la carte
        content = ttk.Frame(card)
        content.pack(fill="x")
        
        # Colonne gauche : infos
        info_frame = ttk.Frame(content)
        info_frame.pack(side="left", fill="both", expand=True)
        
        ttk.Label(
            info_frame,
            text=nom,
            font=FONT_SUBTITLE,
            foreground="black",
            wraplength=600,
            justify="left"
        ).pack(anchor="w")
        
        # Description tronquée
        desc_short = (description[:120] + "...") if len(description) > 120 else description
        ttk.Label(
            info_frame,
            text=desc_short,
            font=FONT_SMALL,
            foreground="gray",
            wraplength=600,
            justify="left"
        ).pack(anchor="w", pady=(5, 10))
        
        # Badge contributions
        badge_text = f"{nb_contrib} contribution{'s' if nb_contrib != 1 else ''}"
        ttk.Label(
            info_frame,
            text=badge_text,
            font=FONT_SMALL,
            foreground="black"
        ).pack(anchor="w")
        
        # Colonne droite : boutons
        btn_frame = ttk.Frame(content)
        btn_frame.pack(side="right", padx=(20, 0))
        
        ttk.Button(
            btn_frame,
            text="Contribuer",
            bootstyle="dark-outline",
            width=16,
            command=lambda c=cid, n=nom: self.ouvrir_contribution(c, n)
        ).pack(pady=3)
        
        ttk.Button(
            btn_frame,
            text="Synthèse IA",
            bootstyle="dark",
            width=16,
            command=lambda c=cid, n=nom: afficher_synthese(self.root, c, n)
        ).pack(pady=3)
    
    def ouvrir_contribution(self, cid, nom):
        """Ouvre le formulaire de contribution avec callback."""
        creer_contribution(self.root, cid, nom, callback=self.afficher_consultations)
    
    def run(self):
        """Lance l'application."""
        self.root.mainloop()


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
