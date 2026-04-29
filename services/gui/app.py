# gui/app.py

import tkinter as tk
from tkinter import ttk, messagebox
from models.employee import Employee
from services import file_service, db_service
from services.db_service import init_database
import config

class EmployeeApp:
    """Application de gestion des employés"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Mode de stockage
        self.storage_mode = config.STORAGE_MODE
        
        # Initialisation de la base si nécessaire
        if self.storage_mode == 'db':
            init_database()
        
        # Configuration de l'interface
        self.setup_ui()
        
        # Chargement des employés
        self.refresh_employee_list()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        
        # Frame pour le titre
        title_frame = tk.Frame(self.root, bg='navy', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="SYSTEME DE GESTION DES EMPLOYES", 
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='navy'
        )
        title_label.pack(expand=True)
        
        # Frame principal avec deux colonnes
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Colonne gauche - Formulaire d'ajout
        left_frame = tk.LabelFrame(main_frame, text="Ajouter un employé", font=('Arial', 12, 'bold'))
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Champs du formulaire
        fields_frame = tk.Frame(left_frame)
        fields_frame.pack(padx=20, pady=20)
        
        # ID
        tk.Label(fields_frame, text="ID Employé:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.entry_id = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.entry_id.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Nom
        tk.Label(fields_frame, text="Nom complet:", font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.entry_name = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.entry_name.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Poste
        tk.Label(fields_frame, text="Poste:", font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.entry_position = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.entry_position.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Salaire
        tk.Label(fields_frame, text="Salaire (CFA):", font=('Arial', 10)).grid(row=3, column=0, sticky='w', pady=5)
        self.entry_salary = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.entry_salary.grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # Boutons d'action
        button_frame = tk.Frame(left_frame)
        button_frame.pack(pady=20)
        
        self.btn_add = tk.Button(
            button_frame, 
            text="➕ Ajouter employé", 
            command=self.add_employee,
            bg='green',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5
        )
        self.btn_add.pack(side='left', padx=5)
        
        self.btn_clear = tk.Button(
            button_frame,
            text="🗑️ Effacer",
            command=self.clear_form,
            bg='orange',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5
        )
        self.btn_clear.pack(side='left', padx=5)
        
        # Colonne droite - Liste des employés
        right_frame = tk.LabelFrame(main_frame, text="Liste des employés", font=('Arial', 12, 'bold'))
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Frame de recherche
        search_frame = tk.Frame(right_frame)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="Rechercher:", font=('Arial', 10)).pack(side='left')
        self.search_entry = tk.Entry(search_frame, font=('Arial', 10), width=20)
        self.search_entry.pack(side='left', padx=10)
        self.search_entry.bind('<KeyRelease>', self.search_employees)
        
        self.btn_search = tk.Button(
            search_frame,
            text="🔍 Rechercher",
            command=self.search_employees,
            font=('Arial', 9)
        )
        self.btn_search.pack(side='left')
        
        # Treeview pour afficher les employés
        columns = ('ID', 'Nom', 'Poste', 'Salaire')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        
        # Configuration des colonnes
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nom', text='Nom')
        self.tree.heading('Poste', text='Poste')
        self.tree.heading('Salaire', text='Salaire (CFA)')
        
        self.tree.column('ID', width=80)
        self.tree.column('Nom', width=150)
        self.tree.column('Poste', width=120)
        self.tree.column('Salaire', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=(0, 10))
        scrollbar.pack(side='right', fill='y', pady=(0, 10))
        
        # Frame des boutons de gestion
        manage_frame = tk.Frame(right_frame)
        manage_frame.pack(pady=10)
        
        self.btn_delete = tk.Button(
            manage_frame,
            text="❌ Supprimer sélection",
            command=self.delete_employee,
            bg='red',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5
        )
        self.btn_delete.pack(side='left', padx=5)
        
        self.btn_refresh = tk.Button(
            manage_frame,
            text="🔄 Actualiser",
            command=self.refresh_employee_list,
            bg='blue',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5
        )
        self.btn_refresh.pack(side='left', padx=5)
        
        self.btn_switch_mode = tk.Button(
            manage_frame,
            text=f"Mode: {'Fichier' if self.storage_mode == 'file' else 'Base de données'}",
            command=self.switch_mode,
            bg='purple',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5
        )
        self.btn_switch_mode.pack(side='left', padx=5)
        
        # Label d'information
        self.info_label = tk.Label(
            right_frame, 
            text=f"Mode actuel: {'STOCKAGE FICHIER' if self.storage_mode == 'file' else 'STOCKAGE BASE DE DONNEES'}",
            font=('Arial', 9, 'italic'),
            fg='blue'
        )
        self.info_label.pack(pady=5)
    
    def get_storage_service(self):
        """Retourne le service de stockage approprié"""
        if self.storage_mode == 'file':
            return file_service
        else:
            return db_service
    
    def add_employee(self):
        """Ajoute un employé"""
        # Validation des champs
        emp_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        position = self.entry_position.get().strip()
        salary_str = self.entry_salary.get().strip()
        
        if not emp_id or not name or not position or not salary_str:
            messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs!")
            return
        
        try:
            salary = float(salary_str)
            if salary < 0:
                raise ValueError("Salaire négatif")
        except ValueError:
            messagebox.showerror("Erreur", "Le salaire doit être un nombre valide positif!")
            return
        
        # Création et ajout de l'employé
        emp = Employee(emp_id, name, position, salary)
        service = self.get_storage_service()
        
        if service.add_employee(emp):
            messagebox.showinfo("Succès", f"Employé {name} ajouté avec succès!")
            self.clear_form()
            self.refresh_employee_list()
        else:
            messagebox.showerror("Erreur", "Impossible d'ajouter l'employé!")
    
    def delete_employee(self):
        """Supprime l'employé sélectionné"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un employé à supprimer!")
            return
        
        emp_id = self.tree.item(selected[0])['values'][0]
        service = self.get_storage_service()
        
        # Confirmation
        if messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer l'employé avec l'ID {emp_id}?"):
            if service.delete_employee(emp_id):
                messagebox.showinfo("Succès", "Employé supprimé avec succès!")
                self.refresh_employee_list()
            else:
                messagebox.showerror("Erreur", "Impossible de supprimer l'employé!")
    
    def refresh_employee_list(self):
        """Actualise la liste des employés"""
        # Effacer la liste existante
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Récupérer les employés
        service = self.get_storage_service()
        employees = service.get_all_employees()
        
        # Afficher les employés
        for emp in employees:
            self.tree.insert('', 'end', values=(emp.emp_id, emp.name, emp.position, f"{emp.salary:,.2f}"))
        
        self.search_entry.delete(0, tk.END)
        self.info_label.config(
            text=f"Total: {len(employees)} employé(s) | Mode: {'FICHIER' if self.storage_mode == 'file' else 'BASE DE DONNEES'}"
        )
    
    def search_employees(self, event=None):
        """Recherche des employés par nom"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            self.refresh_employee_list()
            return
        
        service = self.get_storage_service()
        
        if self.storage_mode == 'file':
            employees = service.search_employee_by_name(search_term)
        else:
            employees = service.search_employee_by_name_db(search_term)
        
        # Effacer la liste
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Afficher les résultats
        for emp in employees:
            self.tree.insert('', 'end', values=(emp.emp_id, emp.name, emp.position, f"{emp.salary:,.2f}"))
        
        self.info_label.config(text=f"Résultats de recherche: {len(employees)} employé(s) trouvé(s)")
    
    def clear_form(self):
        """Efface le formulaire"""
        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_position.delete(0, tk.END)
        self.entry_salary.delete(0, tk.END)
        self.entry_id.focus()
    
    def switch_mode(self):
        """Change le mode de stockage"""
        if self.storage_mode == 'file':
            self.storage_mode = 'db'
            config.STORAGE_MODE = 'db'
            # Vérifier que la base est initialisée
            init_database()
        else:
            self.storage_mode = 'file'
            config.STORAGE_MODE = 'file'
        
        self.btn_switch_mode.config(text=f"Mode: {'Fichier' if self.storage_mode == 'file' else 'Base de données'}")
        self.refresh_employee_list()
        messagebox.showinfo("Mode changé", f"Mode de stockage changé vers: {'Fichier' if self.storage_mode == 'file' else 'Base de données'}")


def run():
    """Lance l'application"""
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()