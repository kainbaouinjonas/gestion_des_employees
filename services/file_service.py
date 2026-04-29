# services/file_service.py

from models.employee import Employee
import os

FILE_NAME = "employees.txt"

def add_employee(emp):
    """Ajoute un employé au fichier"""
    try:
        with open(FILE_NAME, "a") as f:
            f.write(emp.to_string() + "\n")
        return True
    except Exception as e:
        print(f"Erreur d'écriture dans le fichier: {e}")
        return False

def get_all_employees():
    """Récupère tous les employés du fichier"""
    employees = []
    try:
        with open(FILE_NAME, "r") as f:
            for line in f:
                if line.strip():
                    employees.append(Employee.from_string(line))
    except FileNotFoundError:
        print("Fichier non trouvé, démarrage avec une liste vide.")
    return employees

def delete_employee(emp_id):
    """Supprime un employé par son ID"""
    employees = get_all_employees()
    new_employees = [emp for emp in employees if emp.emp_id != emp_id]
    
    if len(new_employees) == len(employees):
        return False
    
    try:
        with open(FILE_NAME, "w") as f:
            for emp in new_employees:
                f.write(emp.to_string() + "\n")
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression: {e}")
        return False

def search_employee_by_name(name):
    """Recherche des employés par nom"""
    employees = get_all_employees()
    return [emp for emp in employees if name.lower() in emp.name.lower()]

def search_employee_by_id(emp_id):
    """Recherche un employé par ID"""
    employees = get_all_employees()
    for emp in employees:
        if emp.emp_id == emp_id:
            return emp
    return None