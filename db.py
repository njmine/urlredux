import pymysql
from flask import g
from dotenv import load_dotenv, find_dotenv
import os

if find_dotenv():
	load_dotenv()

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DB"),
    "cursorclass": pymysql.cursors.Cursor
}

def get_db():
    if "db" not in g:
        g.db = pymysql.connect(**DB_CONFIG)
    return g.db

def init_db():
    # First connect without selecting a DB to create the DB itself
    temp_db = pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )
    cursor = temp_db.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    temp_db.commit()
    cursor.close()
    temp_db.close()

    # Now create tables inside the correct DB
    db = pymysql.connect(**DB_CONFIG)
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INT AUTO_INCREMENT PRIMARY KEY,
            short_code VARCHAR(10) UNIQUE NOT NULL,
            original_url TEXT NOT NULL
        );
    """)
    db.commit()
    cursor.close()
    db.close()

