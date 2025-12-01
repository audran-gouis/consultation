"""
Module de synthèse des contributions avec IA locale (Ollama).
Design épuré fond blanc avec contours noirs
Streaming pour affichage en temps réel
"""

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText
import threading
import requests

from database import get_contributions, get_consultation_details

# Configuration Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen2:0.5b"  # Modèle léger et rapide

# Configuration des styles
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_SUBTITLE = ("Segoe UI", 11)
FONT_NORMAL = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 10)


def check_ollama_running():
    """Vérifie si Ollama est en cours d'exécution."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False


def get_available_models():
    """Récupère la liste des modèles disponibles dans Ollama."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
    except:
        pass
    return []


def generate_synthesis_stream(contributions_text, question, model, text_widget, status_var, btn, win):
    """
    Génère une synthèse avec streaming (affichage en temps réel).
    """
    prompt = f"""Tu es un expert en analyse et synthèse de contributions citoyennes.

CONTEXTE:
Une consultation publique a été organisée sur le thème suivant : "{question}"

CONTRIBUTIONS DES PARTICIPANTS:
{contributions_text}

MISSION:
Analyse ces contributions et produis une synthèse structurée qui:
1. Identifie les THÈMES PRINCIPAUX qui ressortent des contributions
2. Présente les POINTS DE CONSENSUS (idées partagées par plusieurs)
3. Relève les DIVERGENCES ou points de vue opposés
4. Propose des RECOMMANDATIONS basées sur l'ensemble des avis

FORMAT DE RÉPONSE:
Utilise des titres clairs et des puces pour structurer ta réponse.
Sois objectif et représente fidèlement toutes les opinions exprimées.
Écris en français. Sois concis.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 1500
                }
            },
            stream=True,
            timeout=300
        )
        
        if response.status_code == 200:
            # Effacer le texte d'attente
            def clear_text():
                text_widget.config(state="normal")
                text_widget.delete("1.0", "end")
            win.after(0, clear_text)
            
            # Lire le stream
            for line in response.iter_lines():
                if line:
                    try:
                        import json
                        data = json.loads(line)
                        chunk = data.get("response", "")
                        if chunk:
                            def append_text(t=chunk):
                                text_widget.config(state="normal")
                                text_widget.insert("end", t)
                                text_widget.see("end")
                                text_widget.config(state="disabled")
                            win.after(0, append_text)
                        
                        # Vérifier si c'est fini
                        if data.get("done", False):
                            break
                    except:
                        pass
            
            def on_complete():
                status_var.set("Synthèse terminée")
                btn.config(state="normal")
            win.after(0, on_complete)
            
        else:
            def on_error():
                text_widget.config(state="normal")
                text_widget.delete("1.0", "end")
                text_widget.insert("1.0", f"Erreur Ollama: {response.status_code}")
                text_widget.config(state="disabled")
                status_var.set("Erreur")
                btn.config(state="normal")
            win.after(0, on_error)
            
    except requests.exceptions.ConnectionError:
        def on_error():
            text_widget.config(state="normal")
            text_widget.delete("1.0", "end")
            text_widget.insert("1.0", "Impossible de se connecter à Ollama. Vérifiez qu'il est lancé.")
            text_widget.config(state="disabled")
            status_var.set("Erreur de connexion")
            btn.config(state="normal")
        win.after(0, on_error)
    except Exception as e:
        def on_error():
            text_widget.config(state="normal")
            text_widget.delete("1.0", "end")
            text_widget.insert("1.0", f"Erreur: {str(e)}")
            text_widget.config(state="disabled")
            status_var.set("Erreur")
            btn.config(state="normal")
        win.after(0, on_error)


def afficher_synthese(root, consultation_id, consultation_nom):
    """Affiche la fenêtre de synthèse pour une consultation."""
    
    # Récupérer les contributions
    contributions = get_contributions(consultation_id)
    details = get_consultation_details(consultation_id)
    
    if not contributions:
        messagebox.showinfo(
            "Aucune contribution",
            "Il n'y a pas encore de contributions pour cette consultation."
        )
        return
    
    # Créer la fenêtre
    win = ttk.Toplevel(root)
    win.title(f"Synthèse - {consultation_nom}")
    win.geometry("850x650")
    win.resizable(True, True)
    win.configure(bg="white")
    
    # Centrer la fenêtre
    win.place_window_center()
    
    # Rendre modale
    win.transient(root)
    win.grab_set()
    
    # Container principal
    main_frame = ttk.Frame(win, bootstyle="light", padding=25)
    main_frame.pack(fill="both", expand=True)
    
    # Header
    header_frame = ttk.Frame(main_frame, bootstyle="light")
    header_frame.pack(fill="x", pady=(0, 15))
    
    ttk.Label(
        header_frame,
        text="Synthèse IA",
        font=FONT_TITLE,
        foreground="black"
    ).pack(side="left")
    
    ttk.Button(
        header_frame,
        text="Fermer",
        bootstyle="secondary-link",
        command=win.destroy
    ).pack(side="right")
    
    # Info consultation
    ttk.Label(
        main_frame,
        text=consultation_nom,
        font=FONT_SUBTITLE,
        foreground="gray",
        wraplength=750
    ).pack(anchor="w")
    
    nb_contributions = len(contributions)
    ttk.Label(
        main_frame,
        text=f"{nb_contributions} contribution{'s' if nb_contributions > 1 else ''} à analyser",
        font=FONT_SMALL,
        foreground="gray"
    ).pack(anchor="w", pady=(5, 15))
    
    # Ligne de séparation
    sep = ttk.Frame(main_frame, height=1, bootstyle="dark")
    sep.pack(fill="x", pady=(0, 15))
    
    # Sélection du modèle
    model_frame = ttk.Frame(main_frame, bootstyle="light")
    model_frame.pack(fill="x", pady=(0, 15))
    
    ttk.Label(
        model_frame,
        text="Modèle :",
        font=FONT_NORMAL,
        foreground="black"
    ).pack(side="left", padx=(0, 10))
    
    models = get_available_models()
    if not models:
        models = [DEFAULT_MODEL]
    
    model_var = ttk.StringVar(value=models[0] if models else DEFAULT_MODEL)
    
    # Combobox avec bordure
    combo_border = ttk.Frame(model_frame, bootstyle="dark", padding=1)
    combo_border.pack(side="left")
    
    model_combo = ttk.Combobox(
        combo_border,
        textvariable=model_var,
        values=models,
        state="readonly",
        width=25,
        font=FONT_NORMAL
    )
    model_combo.pack()
    
    # Bouton générer
    btn_generer = ttk.Button(
        model_frame,
        text="Générer la synthèse",
        bootstyle="dark",
        padding=(20, 8)
    )
    btn_generer.pack(side="right")
    
    # Indicateur de statut
    status_var = ttk.StringVar(value="")
    status_label = ttk.Label(
        main_frame,
        textvariable=status_var,
        font=FONT_SMALL,
        foreground="gray"
    )
    status_label.pack(anchor="w", pady=(0, 10))
    
    # Zone de résultat avec bordure
    result_border = ttk.Frame(main_frame, bootstyle="dark", padding=1)
    result_border.pack(fill="both", expand=True)
    
    result_text = ScrolledText(result_border, autohide=True)
    result_text.pack(fill="both", expand=True)
    result_text.text.config(
        font=("Consolas", 10),
        wrap="word",
        state="disabled",
        padx=15,
        pady=15,
        bg="white"
    )
    
    # Fonction de génération
    def lancer_synthese():
        if not check_ollama_running():
            messagebox.showerror(
                "Ollama non disponible",
                "Ollama n'est pas en cours d'exécution.\n\n"
                "Pour l'installer :\n"
                "1. Téléchargez sur https://ollama.ai\n"
                "2. Installez et lancez Ollama\n"
                "3. Exécutez : ollama pull mistral\n"
                "4. Réessayez"
            )
            return
        
        # Préparer le texte
        contributions_text = "\n\n---\n\n".join([
            f"Contribution {i+1}:\n{texte}" 
            for i, (_, texte) in enumerate(contributions)
        ])
        
        question = details[1] if details else consultation_nom
        model = model_var.get()
        
        # UI loading
        btn_generer.config(state="disabled")
        status_var.set("Génération en cours... (la réponse s'affiche en temps réel)")
        
        result_text.text.config(state="normal")
        result_text.text.delete("1.0", "end")
        result_text.text.insert("1.0", "Connexion au modèle IA...\n")
        result_text.text.config(state="disabled")
        
        # Lancer en streaming
        thread = threading.Thread(
            target=generate_synthesis_stream,
            args=(contributions_text, question, model, result_text.text, status_var, btn_generer, win)
        )
        thread.daemon = True
        thread.start()
    
    btn_generer.config(command=lancer_synthese)
    
    # Note sur la performance
    perf_label = ttk.Label(
        main_frame,
        text="💡 Astuce : Pour une synthèse plus rapide, utilisez un modèle léger comme 'phi3' ou 'llama3.2:1b'",
        font=FONT_SMALL,
        foreground="gray"
    )
    perf_label.pack(anchor="w", pady=(10, 0))
