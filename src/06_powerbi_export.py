import pandas as pd
import sqlite3
import os

def export_for_powerbi():
    print("\n--- STEP 6: PREPARING DATA FOR POWER BI ---")
    
    # Fix paths to be relative to this script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Create a dedicated folder for Power BI data
    powerbi_dir = os.path.join(base_dir, "data", "processed", "powerbi")
    os.makedirs(powerbi_dir, exist_ok=True)
    
    # 2. Connect to the database
    db_path = os.path.join(base_dir, "data", "movies.db")
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}. Please run app.py or setup scripts first.")
        return
        
    conn = sqlite3.connect(db_path)
    
    # 3. Export Movie Stats (Average Ratings & Popularity)
    print("Generating Movie Stats CSV for Power BI...")
    movie_stats_query = """
    SELECT 
        m.title,
        COUNT(r.rating) as total_ratings,
        ROUND(AVG(r.rating), 2) as average_rating
    FROM movies m
    JOIN ratings r ON m.movieId = r.movieId
    GROUP BY m.title
    HAVING total_ratings > 10
    ORDER BY total_ratings DESC;
    """
    movie_stats_df = pd.read_sql_query(movie_stats_query, conn)
    movie_stats_df.to_csv(f"{powerbi_dir}/movie_stats_for_powerbi.csv", index=False)
    print(f"Saved: {powerbi_dir}/movie_stats_for_powerbi.csv")
    
    # 4. Export Search Logs (User Engagement)
    print("Generating Search Logs CSV for Power BI...")
    search_logs_query = "SELECT search_query, timestamp FROM search_logs;"
    
    try:
        search_logs_df = pd.read_sql_query(search_logs_query, conn)
        # Convert timestamp to date for easier Power BI timeline filtering
        if not search_logs_df.empty:
            search_logs_df['timestamp'] = pd.to_datetime(search_logs_df['timestamp'])
            search_logs_df['date'] = search_logs_df['timestamp'].dt.date
            
        search_logs_df.to_csv(f"{powerbi_dir}/search_logs_for_powerbi.csv", index=False)
        print(f"Saved: {powerbi_dir}/search_logs_for_powerbi.csv")
    except Exception as e:
        print(f"Could not export search logs (table might be empty or missing): {e}")
        
    conn.close()
    print("\n✅ Data export complete! You can now import these CSVs directly into Power BI.")

if __name__ == "__main__":
    export_for_powerbi()
