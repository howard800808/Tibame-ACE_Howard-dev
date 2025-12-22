import pymysql
from urllib.parse import urlparse
import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.core.config import settings

def create_database():
    db_url = settings.DATABASE_URL
    # Parse the URL manually or use a library. 
    # Format: mysql+pymysql://user:password@host:port/dbname
    
    if not db_url.startswith("mysql"):
        print("Not a MySQL URL. Skipping.")
        return

    try:
        # Extract parts
        # Remove mysql+pymysql://
        url_part = db_url.split("://")[1]
        user_pass, host_db = url_part.split("@")
        user, password = user_pass.split(":")
        host_port, db_name = host_db.split("/")
        
        if ":" in host_port:
            host, port = host_port.split(":")
            port = int(port)
        else:
            host = host_port
            port = 3306
            
        print(f"Connecting to MySQL at {host}:{port} as {user}...")
        
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        
        cursor = conn.cursor()
        print(f"Creating database '{db_name}' if not exists...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print("Database created successfully.")
        
        conn.close()
        
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_database()
