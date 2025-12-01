"""
Formulaire de contribution à une consultation
Design épuré fond blanc avec contours noirs
"""

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from database import enregistrer_contribution

# Configuration des styles
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_SUBTITLE = ("Segoe UI", 11)
FONT_LABEL = ("Segoe UI", 11)
FONT_INPUT = ("Segoe UI", 11)


def creer_contribution(root, consultation_id, consultation_nom, callback=None):
    """
    Ouvre le formulaire de contribution.
    """
    win = ttk.Toplevel(root)
    win.title("Contribuer")
    win.geometry("700x520")
    win.resizable(False, False)
    win.configure(bg="white")
    
    # Centrer la fenêtre
    win.place_window_center()
    
    # Rendre la fenêtre modale
    win.transient(root)
    win.grab_set()
    
    # Container principal
    main_frame = ttk.Frame(win, padding=30)
    main_frame.pack(fill="both", expand=True)
    
    # Header
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill="x", pady=(0, 10))
    
    ttk.Label(
        header_frame,
        text="Votre contribution",
        font=FONT_TITLE,
        foreground="black"
    ).pack(side="left")
    
    ttk.Button(
        header_frame,
        text="Annuler",
        bootstyle="secondary-link",
        command=win.destroy
    ).pack(side="right")
    
    # Nom de la consultation
    ttk.Label(
        main_frame,
        text=consultation_nom,
        font=FONT_SUBTITLE,
        foreground="gray",
        wraplength=620
    ).pack(anchor="w", pady=(0, 15))
    
    # Ligne de séparation
    sep = ttk.Frame(main_frame, height=1, bootstyle="dark")
    sep.pack(fill="x", pady=(0, 20))
    
    # Zone de texte
    ttk.Label(
        main_frame,
        text="Rédigez votre avis ou proposition",
        font=FONT_LABEL,
        foreground="black"
    ).pack(anchor="w", pady=(0, 5))
    
    # Cadre avec bordure noire
    text_border = ttk.Frame(main_frame, bootstyle="dark", padding=1)
    text_border.pack(fill="x", pady=(0, 20))
    
    text_zone = tk.Text(
        text_border,
        font=FONT_INPUT,
        wrap="word",
        bd=0,
        padx=12,
        pady=12,
        height=12,
        bg="white"
    )
    text_zone.pack(fill="x")
    text_zone.focus_set()
    
    # Fonction de validation
    def valider():
        texte = text_zone.get("1.0", "end").strip()
        
        if not texte:
            messagebox.showwarning(
                "Contribution vide",
                "Veuillez rédiger votre contribution."
            )
            text_zone.focus_set()
            return
        
        if len(texte) < 10:
            messagebox.showwarning(
                "Contribution trop courte",
                "Votre contribution doit contenir au moins 10 caractères."
            )
            text_zone.focus_set()
            return
        
        enregistrer_contribution(consultation_id, texte)
        win.destroy()
        
        messagebox.showinfo(
            "Merci",
            "Votre contribution a été enregistrée."
        )
        
        # Appeler le callback pour rafraîchir
        if callback:
            callback()
    
    # Bouton d'envoi
    ttk.Button(
        main_frame,
        text="Envoyer ma contribution",
        bootstyle="dark",
        command=valider,
        padding=(25, 12)
    ).pack(anchor="e", pady=(10, 0))
