import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import json
from .lib_graphe import Graphe, trouve_arbitrages, trouve_chemin_optimal


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Convertisseur de devises")
        self.geometry("800x600")
        self.load_data()
        self.create_widgets()

    def load_data(self):
        with open("donnees.json", "r") as json_file:
            self.data = json.load(json_file)
        self.devises = self.data["devises"]
        self.taux = self.data["taux"]

    def create_widgets(self):
        style = ttk.Style(self)
        style.configure("TFrame", background="#ffffff")
        style.configure(
            "TButton", background="#336699", foreground="white", font=("Arial", 12)
        )
        style.configure("TLabel", background="#ffffff", font=("Arial", 12))
        style.configure("Header.TLabel", font=("Arial", 14, "bold"))

        style.configure("OptimalPath.TButton", foreground="black", font=("Arial", 12))

        frame = ttk.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        header = ttk.Label(
            frame, text="Convertisseur de devises", style="Header.TLabel"
        )
        header.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        devise_label = ttk.Label(frame, text="Choisissez une devise :", style="TLabel")
        devise_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.combo_devise = ttk.Combobox(frame, values=self.devises)
        self.combo_devise.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.btn_afficher = ttk.Button(
            frame,
            text="Afficher le chemin optimal",
            command=self.afficher_chemin_optimal,
            style="OptimalPath.TButton",
        )
        self.btn_afficher.grid(
            row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        self.label_resultat = ttk.Label(frame, text="", style="TLabel")
        self.label_resultat.grid(
            row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w"
        )

        self.btn_devises = ttk.Button(
            frame,
            text="Afficher les devises",
            command=self.afficher_devises,
            style="OptimalPath.TButton",
        )
        self.btn_devises.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

    def afficher_chemin_optimal(self):
        devise_initiale = self.combo_devise.get()

        graphe_devises = Graphe(self.devises, self.taux)
        dictionnaire_taux = graphe_devises.to_dictionnaire_taux()

        arbitrages = trouve_arbitrages(dictionnaire_taux, devise_initiale)
        chemin_optimal = trouve_chemin_optimal(arbitrages)

        message = f"Le chemin optimal pour {devise_initiale} est : {chemin_optimal[0]} avec un rendement de {chemin_optimal[1]}"
        self.label_resultat.config(text=message)

        if messagebox.askyesno(
            "Convertir un montant", "Voulez-vous choisir un montant à convertir ?"
        ):
            montant = simpledialog.askfloat(
                "Montant à convertir", "Entrez le montant à convertir :", minvalue=0.01
            )
            montant_converti = montant * chemin_optimal[1]
            gain = montant_converti - montant
            messagebox.showinfo(
                "Résultat",
                f"Le montant converti grâce à cet arbitrage est : {montant_converti}, le gain est de {gain} {devise_initiale}",
            )

    def afficher_devises(self):
        messagebox.showinfo("Devises disponibles", "\n".join(self.devises))


if __name__ == "__main__":
    app = Application()
    app.mainloop()
