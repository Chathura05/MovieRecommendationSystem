import pandas as pd
import sqlite3
import os

def setup_database():
    print("--- STEP 0: DATABASE INITIALIZATION ---")
    
    # Ensure raw data exists
    if not os.path.exists("../data/raw/movies.csv") or not os.path.exists("../data/raw/ratings.csv"):
        print("Error: Raw CSV files not found. Please ensure movies.csv and ratings.csv exist in data/raw/.")
        return

    # Load datasets
    print("Loading raw CSV files into memory...")
    movies_df = pd.read_csv("../data/raw/movies.csv")
    ratings_df = pd.read_csv("../data/raw/ratings.csv")

    # Connect to SQLite Database
    db_path = "../data/movies.db"
    print(f"Connecting to SQLite database at {db_path}...")
    conn = sqlite3.connect(db_path)
    
    # Insert DataFrames into SQL tables
    print("Writing 'movies' table...")
    movies_df.to_sql('movies', conn, if_exists='replace', index=False)
    
    print("Writing 'ratings' table...")
    ratings_df.to_sql('ratings', conn, if_exists='replace', index=False)
    
    # Create the search_logs table
    print("Creating 'search_logs' table for web app tracking...")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_query TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    
    # Verify tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"\nDatabase setup complete! Tables created: {[table[0] for table in tables]}")
    
    conn.close()

if __name__ == "__main__":
    setup_database()
