# services/db_service.py

import psycopg2
from psycopg2 import sql
from models.employee import Employee

# Configuration de la base de données
DB_CONFIG = {
    'dbname': 'employees_db',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': '5432'
}

def connect():
    """Établit la connexion à la base de données"""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

def init_database():
    """Initialise la base de données et crée la table"""
    conn = connect()
    if conn is None:
        return False
    
    try:
        cur = conn.cursor()
        
        # Création de la table employees
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                emp_id VARCHAR(10) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                position VARCHAR(50) NOT NULL,
                salary FLOAT NOT NULL
            )
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("Base de données initialisée avec succès")
        return True
    except Exception as e:
        print(f"Erreur d'initialisation de la base: {e}")
        return False

def add_employee_db(emp):
    """Ajoute un employé dans la base de données"""
    try:
        conn = connect()
        if conn is None:
            return False
        
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO employees (emp_id, name, position, salary) VALUES (%s, %s, %s, %s)",
            (emp.emp_id, emp.name, emp.position, emp.salary)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.IntegrityError:
        print(f"Erreur: Un employé avec l'ID {emp.emp_id} existe déjà")
        return False
    except Exception as e:
        print(f"Erreur base de données: {e}")
        return False

def get_all_employees_db():
    """Récupère tous les employés de la base"""
    employees = []
    try:
        conn = connect()
        if conn is None:
            return employees
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees")
        rows = cur.fetchall()
        
        for r in rows:
            employees.append(Employee(r[0], r[1], r[2], float(r[3])))
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erreur base de données: {e}")
    
    return employees

def delete_employee_db(emp_id):
    """Supprime un employé de la base par son ID"""
    try:
        conn = connect()
        if conn is None:
            return False
        
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
        deleted = cur.rowcount > 0
        conn.commit()
        cur.close()
        conn.close()
        return deleted
    except Exception as e:
        print(f"Erreur lors de la suppression: {e}")
        return False

def search_employee_by_name_db(name):
    """Recherche des employés par nom dans la base"""
    employees = []
    try:
        conn = connect()
        if conn is None:
            return employees
        
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM employees WHERE name ILIKE %s",
            (f'%{name}%',)
        )
        rows = cur.fetchall()
        
        for r in rows:
            employees.append(Employee(r[0], r[1], r[2], float(r[3])))
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de la recherche: {e}")
    
    return employees

def search_employee_by_id_db(emp_id):
    """Recherche un employé par ID dans la base"""
    try:
        conn = connect()
        if conn is None:
            return None
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees WHERE emp_id = %s", (emp_id,))
        row = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if row:
            return Employee(row[0], row[1], row[2], float(row[3]))
    except Exception as e:
        print(f"Erreur lors de la recherche: {e}")
    
    return None