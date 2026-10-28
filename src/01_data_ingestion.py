import pandas as pd
import numpy as np

def run_ingestion():
    print("--- STEP 1: DATA INGESTION & AUDIT ---")
    try:
        import sqlite3
        print("Connecting to SQLite database...")
        conn = sqlite3.connect("../data/movies.db")
        
        # Load datasets via SQL
        movies = pd.read_sql("SELECT * FROM movies", conn)
        ratings = pd.read_sql("SELECT * FROM ratings", conn)
        conn.close()
        print("Data loaded successfully.")

        print("\n--- Matrix Dimensionality ---")
        print(f"Movies shape: {movies.shape}")
        print(f"Ratings shape: {ratings.shape}")

        print("\n--- Movies Info ---")
        movies.info()

        print("\n--- Ratings Info ---")
        ratings.info()

        print("\n--- Ratings Description ---")
        print(ratings.describe())
        
        return movies, ratings
    except FileNotFoundError:
        print("Error: Could not find raw data files. Please ensure dataset is downloaded.")
        return None, None

if __name__ == "__main__":
    run_ingestion()
