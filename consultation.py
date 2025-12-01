"""
Formulaire de création de consultation
Design épuré fond blanc avec contours noirs
"""

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from database import enregistrer_consultation

# Configuration des styles
FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_INPUT = ("Segoe UI", 11)


def creer_formulaire(root, callback=None):
    """
    Ouvre le formulaire de création de consultation.
    """
    form_win = ttk.Toplevel(root)
    form_win.title("Nouvelle consultation")
    form_win.geometry("650x520")
    form_win.resizable(False, False)
    form_win.configure(bg="white")
    
    # Centrer la fenêtre
    form_win.place_window_center()
    
    # Rendre la fenêtre modale
    form_win.transient(root)
    form_win.grab_set()
    
    # Container principal
    main_frame = ttk.Frame(form_win, padding=30)
    main_frame.pack(fill="both", expand=True)
    
    # Header
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill="x", pady=(0, 20))
    
    ttk.Label(
        header_frame,
        text="Créer une consultation",
        font=FONT_TITLE,
        foreground="black"
    ).pack(side="left")
    
    ttk.Button(
        header_frame,
        text="Annuler",
        bootstyle="secondary-link",
        command=form_win.destroy
    ).pack(side="right")
    
    # Ligne de séparation
    sep = ttk.Frame(main_frame, height=1, bootstyle="dark")
    sep.pack(fill="x", pady=(0, 20))
    
    # Champ nom
    ttk.Label(
        main_frame,
        text="Titre de la consultation",
        font=FONT_LABEL,
        foreground="black"
    ).pack(anchor="w", pady=(0, 5))
    
    # Cadre avec bordure pour l'entrée
    entry_border = ttk.Frame(main_frame, bootstyle="dark", padding=1)
    entry_border.pack(fill="x", pady=(0, 20))
    
    entry_nom = ttk.Entry(entry_border, font=FONT_INPUT, bootstyle="light")
    entry_nom.pack(fill="x", ipady=8)
    entry_nom.focus_set()
    
    # Champ description
    ttk.Label(
        main_frame,
        text="Question ou thème soumis aux participants",
        font=FONT_LABEL,
        foreground="black"
    ).pack(anchor="w", pady=(0, 5))
    
    # Cadre avec bordure pour le texte
    text_border = ttk.Frame(main_frame, bootstyle="dark", padding=1)
    text_border.pack(fill="x", pady=(0, 20))
    
    text_zone = tk.Text(
        text_border,
        font=FONT_INPUT,
        height=8,
        wrap="word",
        bd=0,
        padx=10,
        pady=10,
        bg="white"
    )
    text_zone.pack(fill="x")
    
    # Fonction de validation
    def valider():
        nom = entry_nom.get().strip()
        desc = text_zone.get("1.0", "end").strip()
        
        if not nom:
            messagebox.showwarning(
                "Champ requis",
                "Veuillez saisir un titre pour la consultation."
            )
            entry_nom.focus_set()
            return
        
        if not desc:
            messagebox.showwarning(
                "Champ requis",
                "Veuillez saisir une question ou un thème."
            )
            text_zone.focus_set()
            return
        
        enregistrer_consultation(nom, desc)
        form_win.destroy()
        
        # Appeler le callback pour rafraîchir la liste
        if callback:
            callback()
    
    # Bouton de validation
    ttk.Button(
        main_frame,
        text="Créer la consultation",
        bootstyle="dark",
        command=valider,
        padding=(25, 12)
    ).pack(anchor="e", pady=(10, 0))
    
    # Bind Enter pour valider
    form_win.bind("<Return>", lambda e: valider())
