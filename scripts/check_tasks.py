from app.core.database import SessionLocal
from app.models.user import User  # Import User to resolve relationship
from app.models.task import Task
from sqlalchemy import func

db = SessionLocal()
try:
    # Check distinct departments in Task table
    departments = db.query(Task.department, func.count(Task.id)).group_by(Task.department).all()
    print("Distinct departments in Task table:")
    for dept, count in departments:
        print(f"Department: '{dept}', Count: {count}")

    # Check first few tasks
    tasks = db.query(Task).limit(5).all()
    print("\nFirst 5 tasks:")
    for t in tasks:
        print(f"ID: {t.id}, Dept: '{t.department}', Status: {t.status}")

finally:
    db.close()
