import sys
import os
import random
import string

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.department import Department
from app.models.user import User
from app.core.security import get_password_hash

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_user_data(dept_code, role, index):
    # Generate a somewhat readable username
    username = f"{dept_code}_{role}_{generate_random_string(4)}"
    email = f"{username}@example.com"
    full_name = f"{role.capitalize()} {generate_random_string(5).capitalize()}"
    
    return {
        "username": username,
        "email": email,
        "full_name": full_name,
        "hashed_password": get_password_hash("ace123"),
        "role": role,
        "department": dept_code,
        "is_active": True
    }

def seed_users():
    db: Session = SessionLocal()
    try:
        # Fetch all departments
        departments = db.query(Department).all()
        if not departments:
            print("No departments found. Please seed departments first.")
            return

        print(f"Found {len(departments)} departments.")

        users_to_add = []
        
        for dept in departments:
            print(f"Processing department: {dept.name_zh} ({dept.code})")
            
            # 1 Manager
            manager_data = generate_user_data(dept.code, "manager", 1)
            # Check if user exists
            if not db.query(User).filter(User.username == manager_data["username"]).first():
                user = User(**manager_data)
                users_to_add.append(user)
            
            # 4 Employees
            for i in range(4):
                employee_data = generate_user_data(dept.code, "user", i+1)
                if not db.query(User).filter(User.username == employee_data["username"]).first():
                    user = User(**employee_data)
                    users_to_add.append(user)
        
        if users_to_add:
            db.add_all(users_to_add)
            db.commit()
            print(f"Successfully added {len(users_to_add)} users.")
        else:
            print("No new users to add.")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()
