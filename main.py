import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def calculer_hash(fichier, algo='sha256'):
    h = hashlib.new(algo)
    try:
        with open(fichier, 'rb') as f:
            for bloc in iter(lambda: f.read(4096), b''):
                h.update(bloc)
        return h.hexdigest()
    except Exception as e:
        return str(e)

def selectionner_fichier():
    chemin = filedialog.askopenfilename()
    if chemin:
        entree_fichier.delete(0, tk.END)
        entree_fichier.insert(0, chemin)

def lancer_hash():
    fichier = entree_fichier.get()
    algo = algo_var.get()
    if not fichier:
        messagebox.showerror("Erreur", "Veuillez sélectionner un fichier.")
        return
    if algo not in algos_valides:
        messagebox.showerror("Erreur", "Algorithme non valide.")
        return
    resultat = calculer_hash(fichier, algo)
    texte_resultat.delete(1.0, tk.END)
    texte_resultat.insert(tk.END, f"{algo.upper()}:\n{resultat}")

# Algorithmes que l'on souhaite proposer
algos_valides = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']

# Interface
fenetre = tk.Tk()
fenetre.title("Hashage de fichier")

tk.Label(fenetre, text="Fichier à hasher:").grid(row=0, column=0, padx=10, pady=10)
entree_fichier = tk.Entry(fenetre, width=50)
entree_fichier.grid(row=0, column=1, padx=10)
btn_parcourir = tk.Button(fenetre, text="Parcourir...", command=selectionner_fichier)
btn_parcourir.grid(row=0, column=2, padx=10)

tk.Label(fenetre, text="Algorithme:").grid(row=1, column=0, padx=10, pady=10)
algo_var = tk.StringVar(value='sha256')
combo_algo = ttk.Combobox(fenetre, textvariable=algo_var, values=algos_valides, state='readonly')
combo_algo.grid(row=1, column=1, padx=10, pady=5, sticky='w')

btn_hasher = tk.Button(fenetre, text="Calculer le hash", command=lancer_hash)
btn_hasher.grid(row=2, column=1, pady=10)

texte_resultat = tk.Text(fenetre, height=5, width=80)
texte_resultat.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

fenetre.mainloop()
