# models/employee.py

class Employee:
    """Classe Employee représentant un employé"""
    
    def __init__(self, emp_id, name, position, salary):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.salary = float(salary)
    
    def to_string(self):
        """Convertit l'employé en chaîne pour stockage fichier"""
        return f"{self.emp_id},{self.name},{self.position},{self.salary}"
    
    @staticmethod
    def from_string(data):
        """Crée un employé à partir d'une chaîne"""
        parts = data.strip().split(",")
        return Employee(parts[0], parts[1], parts[2], float(parts[3]))
    
    def __str__(self):
        """Représentation lisible de l'employé"""
        return f"ID: {self.emp_id} | Nom: {self.name} | Poste: {self.position} | Salaire: {self.salary:.2f} CFA"
    
    def to_dict(self):
        """Convertit l'employé en dictionnaire"""
        return {
            'emp_id': self.emp_id,
            'name': self.name,
            'position': self.position,
            'salary': self.salary
        }