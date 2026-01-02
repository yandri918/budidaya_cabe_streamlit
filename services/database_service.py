"""
Database Service for Data Persistence
SQLite database for storing harvest, growth, journal, and user data
"""

import sqlite3
import json
import os
from datetime import datetime
import pandas as pd

class DatabaseService:
    
    DB_PATH = "data/budidaya_cabe.db"
    BACKUP_DIR = "data/backups"
    
    @staticmethod
    def init_database():
        """Initialize database and create tables if not exist"""
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        os.makedirs(DatabaseService.BACKUP_DIR, exist_ok=True)
        
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        cursor = conn.cursor()
        
        # Harvests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS harvests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_name TEXT NOT NULL,
                farm_location TEXT NOT NULL,
                harvest_number INTEGER,
                date TEXT,
                grading TEXT,
                weight_kg REAL,
                price_per_kg INTEGER,
                total_value INTEGER,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Growth records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS growth_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_name TEXT,
                planting_date TEXT,
                hst INTEGER,
                height_cm REAL,
                leaf_count INTEGER,
                health_score INTEGER,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Journal entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_name TEXT,
                date TEXT,
                activity_type TEXT,
                description TEXT,
                cost INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_name TEXT UNIQUE NOT NULL,
                farm_location TEXT,
                land_area REAL,
                planting_date TEXT,
                total_investment INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # QR Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qr_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT UNIQUE NOT NULL,
                harvest_id TEXT,
                batch_number TEXT,
                harvest_date TEXT NOT NULL,
                farm_location TEXT,
                farmer_name TEXT,
                grade TEXT,
                weight_kg REAL,
                certifications TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        return True
    
    # ===== HARVEST OPERATIONS =====
    
    @staticmethod
    def save_harvest(harvest_data):
        """Save harvest entry to database"""
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO harvests (
                farmer_name, farm_location, harvest_number, date, grading,
                weight_kg, price_per_kg, total_value, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            harvest_data['farmer_name'],
            harvest_data['farm_location'],
            harvest_data['harvest_number'],
            harvest_data['date'],
            harvest_data['grading'],
            harvest_data['weight_kg'],
            harvest_data['price_per_kg'],
            harvest_data['total_value'],
            harvest_data.get('notes', '')
        ))
        
        conn.commit()
        harvest_id = cursor.lastrowid
        conn.close()
        
        return harvest_id
    
    @staticmethod
    def get_all_harvests(farmer_name=None):
        """Get all harvest entries, optionally filtered by farmer"""
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        
        if farmer_name:
            query = "SELECT * FROM harvests WHERE farmer_name = ? ORDER BY date DESC"
            df = pd.read_sql_query(query, conn, params=(farmer_name,))
        else:
            query = "SELECT * FROM harvests ORDER BY date DESC"
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        return df.to_dict('records') if not df.empty else []
    
    @staticmethod
    def delete_harvest(harvest_id):
        """Delete a harvest entry"""
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM harvests WHERE id = ?", (harvest_id,))
        
        conn.commit()
        conn.close()
        
        return True
    
    # ===== GROWTH RECORDS OPERATIONS =====
    
    @staticmethod
    def save_growth_record(growth_data):
        """Save growth monitoring record"""
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO growth_records (
                farmer_name, planting_date, hst, height_cm, leaf_count,
                health_score, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            growth_data.get('farmer_name', ''),
            growth_data.get('planting_date', ''),
            growth_data.get('hst', 0),
            growth_data.get('height_cm', 0),
            growth_data.get('leaf_count', 0),
            growth_data.get('health_score', 0),
            growth_data.get('notes', '')
        ))
        
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        
        return record_id
    
    @staticmethod
    def get_growth_records(farmer_name=None):
        """Get growth records"""
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        
        if farmer_name:
            query = "SELECT * FROM growth_records WHERE farmer_name = ? ORDER BY hst"
            df = pd.read_sql_query(query, conn, params=(farmer_name,))
        else:
            query = "SELECT * FROM growth_records ORDER BY hst"
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        return df.to_dict('records') if not df.empty else []
    
    # ===== JOURNAL OPERATIONS =====
    
    @staticmethod
    def save_journal_entry(entry_data):
        """Save journal entry"""
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO journal_entries (
                farmer_name, date, activity_type, description, cost
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            entry_data.get('farmer_name', ''),
            entry_data.get('date', ''),
            entry_data.get('activity_type', ''),
            entry_data.get('description', ''),
            entry_data.get('cost', 0)
        ))
        
        conn.commit()
        entry_id = cursor.lastrowid
        conn.close()
        
        return entry_id
    
    @staticmethod
    def get_journal_entries(farmer_name=None):
        """Get journal entries"""
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        
        if farmer_name:
            query = "SELECT * FROM journal_entries WHERE farmer_name = ? ORDER BY date DESC"
            df = pd.read_sql_query(query, conn, params=(farmer_name,))
        else:
            query = "SELECT * FROM journal_entries ORDER BY date DESC"
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        return df.to_dict('records') if not df.empty else []
    
    # ===== USER PROFILE OPERATIONS =====
    
    @staticmethod
    def save_user_profile(profile_data):
        """Save or update user profile"""
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        cursor = conn.cursor()
        
        # Check if profile exists
        cursor.execute("SELECT id FROM user_profiles WHERE farmer_name = ?", 
                      (profile_data['farmer_name'],))
        existing = cursor.fetchone()
        
        if existing:
            # Update
            cursor.execute('''
                UPDATE user_profiles SET
                    farm_location = ?,
                    land_area = ?,
                    planting_date = ?,
                    total_investment = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE farmer_name = ?
            ''', (
                profile_data.get('farm_location', ''),
                profile_data.get('land_area', 1.0),
                profile_data.get('planting_date', ''),
                profile_data.get('total_investment', 0),
                profile_data['farmer_name']
            ))
        else:
            # Insert
            cursor.execute('''
                INSERT INTO user_profiles (
                    farmer_name, farm_location, land_area, planting_date, total_investment
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                profile_data['farmer_name'],
                profile_data.get('farm_location', ''),
                profile_data.get('land_area', 1.0),
                profile_data.get('planting_date', ''),
                profile_data.get('total_investment', 0)
            ))
        
        conn.commit()
        conn.close()
        
        return True
    
    @staticmethod
    def get_user_profile(farmer_name):
        """Get user profile"""
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user_profiles WHERE farmer_name = ?", (farmer_name,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        
        return None
    
    # ===== EXPORT/IMPORT =====
    
    @staticmethod
    def export_to_json():
        """Export all data to JSON"""
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        
        data = {
            'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version': '1.0',
            'data': {
                'harvests': pd.read_sql_query("SELECT * FROM harvests", conn).to_dict('records'),
                'growth_records': pd.read_sql_query("SELECT * FROM growth_records", conn).to_dict('records'),
                'journal_entries': pd.read_sql_query("SELECT * FROM journal_entries", conn).to_dict('records'),
                'user_profiles': pd.read_sql_query("SELECT * FROM user_profiles", conn).to_dict('records')
            }
        }
        
        conn.close()
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    @staticmethod
    def import_from_json(json_data, mode='merge'):
        """
        Import data from JSON
        
        Args:
            json_data: JSON string or dict
            mode: 'merge' or 'replace'
        """
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
        
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        cursor = conn.cursor()
        
        # If replace mode, clear existing data
        if mode == 'replace':
            cursor.execute("DELETE FROM harvests")
            cursor.execute("DELETE FROM growth_records")
            cursor.execute("DELETE FROM journal_entries")
            cursor.execute("DELETE FROM user_profiles")
        
        # Import harvests
        for harvest in data['data'].get('harvests', []):
            cursor.execute('''
                INSERT INTO harvests (
                    farmer_name, farm_location, harvest_number, date, grading,
                    weight_kg, price_per_kg, total_value, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                harvest.get('farmer_name', ''),
                harvest.get('farm_location', ''),
                harvest.get('harvest_number', 0),
                harvest.get('date', ''),
                harvest.get('grading', ''),
                harvest.get('weight_kg', 0),
                harvest.get('price_per_kg', 0),
                harvest.get('total_value', 0),
                harvest.get('notes', '')
            ))
        
        # Import other tables similarly...
        
        conn.commit()
        conn.close()
        
        return True
    
    # ===== BACKUP =====
    
    @staticmethod
    def create_backup():
        """Create database backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"{DatabaseService.BACKUP_DIR}/backup_{timestamp}.json"
        
        json_data = DatabaseService.export_to_json()
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(json_data)
        
        # Cleanup old backups (keep last 7)
        DatabaseService._cleanup_old_backups()
        
        return backup_file
    
    @staticmethod
    def _cleanup_old_backups(keep_last=7):
        """Remove old backup files"""
        if not os.path.exists(DatabaseService.BACKUP_DIR):
            return
        
        backups = sorted([
            f for f in os.listdir(DatabaseService.BACKUP_DIR)
            if f.startswith('backup_') and f.endswith('.json')
        ])
        
        if len(backups) > keep_last:
            for old_backup in backups[:-keep_last]:
                os.remove(os.path.join(DatabaseService.BACKUP_DIR, old_backup))
    
    # ===== QR PRODUCT OPERATIONS =====
    
    @staticmethod
    def save_qr_product(product_data):
        """Save QR product data"""
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        cursor = conn.cursor()
        
        # Convert certifications list to JSON string
        certs_json = json.dumps(product_data.get('certifications', []))
        
        cursor.execute('''
            INSERT OR REPLACE INTO qr_products (
                product_id, harvest_id, batch_number, harvest_date,
                farm_location, farmer_name, grade, weight_kg, certifications
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product_data['product_id'],
            product_data.get('harvest_id', ''),
            product_data.get('batch_number', ''),
            product_data['harvest_date'],
            product_data.get('farm_location', ''),
            product_data.get('farmer_name', ''),
            product_data.get('grade', ''),
            product_data.get('weight_kg', 0),
            certs_json
        ))
        
        conn.commit()
        product_id = cursor.lastrowid
        conn.close()
        
        return product_id
    
    @staticmethod
    def get_qr_product(product_id):
        """Get QR product by ID"""
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM qr_products WHERE product_id = ?", (product_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            product = dict(zip(columns, row))
            # Parse certifications JSON
            product['certifications'] = json.loads(product.get('certifications', '[]'))
            return product
        
        return None
    
    @staticmethod
    def get_all_qr_products():
        """Get all QR products"""
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        
        query = "SELECT * FROM qr_products ORDER BY created_at DESC"
        df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        if not df.empty:
            products = df.to_dict('records')
            # Parse certifications for each product
            for product in products:
                product['certifications'] = json.loads(product.get('certifications', '[]'))
            return products
        
        return []
    
    # ===== STATISTICS =====
    
    @staticmethod
    def get_database_stats():
        """Get database statistics"""
        conn = sqlite3.connect(DatabaseService.DB_PATH)
        cursor = conn.cursor()
        
        stats = {
            'total_harvests': cursor.execute("SELECT COUNT(*) FROM harvests").fetchone()[0],
            'total_growth_records': cursor.execute("SELECT COUNT(*) FROM growth_records").fetchone()[0],
            'total_journal_entries': cursor.execute("SELECT COUNT(*) FROM journal_entries").fetchone()[0],
            'total_users': cursor.execute("SELECT COUNT(*) FROM user_profiles").fetchone()[0],
            'total_qr_products': cursor.execute("SELECT COUNT(*) FROM qr_products").fetchone()[0],
            'database_size_kb': os.path.getsize(DatabaseService.DB_PATH) / 1024 if os.path.exists(DatabaseService.DB_PATH) else 0
        }
        
        conn.close()
        
        return stats
