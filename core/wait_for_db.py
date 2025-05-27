import time
import os
import sys
import psycopg2
from django.db import connections
from django.db.utils import OperationalError

def wait_for_db():
    """Wait for database to be available"""
    start_time = time.time()
    timeout = 30  # 30 seconds timeout
    
    print("Waiting for database...")
    
    while True:
        try:
            # Try to connect to the database
            conn = psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB', 'social'),
                user=os.getenv('POSTGRES_USER', 'postgres'),
                password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
                host=os.getenv('POSTGRES_HOST', 'db'),
                port=os.getenv('POSTGRES_PORT', '5432')
            )
            conn.close()
            print("Database is available!")
            return
        except psycopg2.OperationalError as e:
            if time.time() - start_time >= timeout:
                print(f"Database connection failed after {timeout} seconds")
                print(f"Error: {e}")
                sys.exit(1)
            time.sleep(1)

if __name__ == "__main__":
    wait_for_db()
