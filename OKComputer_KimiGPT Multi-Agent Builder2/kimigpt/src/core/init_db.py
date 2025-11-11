#!/usr/bin/env python3
"""
Database initialization script for KimiGPT
Creates SQLite database and required tables
"""

import sqlite3
import os
from datetime import datetime

def create_database():
    """Create SQLite database and tables"""
    
    # Ensure database directory exists
    db_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'database')
    os.makedirs(db_dir, exist_ok=True)
    
    db_path = os.path.join(db_dir, 'kimigpt.db')
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            settings TEXT,
            result TEXT
        )
    ''')
    
    # Create api_usage table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_name TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            status_code INTEGER,
            response_time REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            error_message TEXT
        )
    ''')
    
    # Create user_preferences table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create cache table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL,
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create default preferences
    default_preferences = {
        'default_style': 'modern',
        'default_complexity': 'moderate',
        'auto_save': 'true',
        'auto_deploy': 'false',
        'cache_duration': '60',
        'max_concurrent': '3',
        'retry_attempts': '3'
    }
    
    for key, value in default_preferences.items():
        cursor.execute('''
            INSERT OR IGNORE INTO user_preferences (key, value) VALUES (?, ?)
        ''', (key, value))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database initialized successfully at: {db_path}")
    return db_path

if __name__ == '__main__':
    db_path = create_database()
    print("Database initialization complete!")