import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import psycopg2
import os

class Command(BaseCommand):
    """Django command to wait for database to be available"""
    
    def handle(self, *args, **options):
        """Handle the command"""
        self.stdout.write('Waiting for database...')
        db_conn = None
        start_time = time.time()
        timeout = 30  # 30 seconds timeout
        
        while not db_conn:
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
                db_conn = True
            except psycopg2.OperationalError as e:
                if time.time() - start_time >= timeout:
                    self.stdout.write(self.style.ERROR('Database connection failed after 30 seconds'))
                    self.stdout.write(self.style.ERROR(f'Error: {e}'))
                    raise
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS('Database available!'))
