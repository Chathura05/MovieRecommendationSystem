import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

app = Flask(__name__)

# Load Data and Precompute SVD
print("Loading dataset...")
df = pd.read_csv("data/processed/merged_cleaned_data.csv")

print("Building User-Item Matrix...")
user_item_matrix = df.pivot_table(index='user_id', columns='title', values='rating', aggfunc='mean').fillna(0)
item_user_matrix = user_item_matrix.T

print("Computing SVD...")
n_components = min(20, item_user_matrix.shape[0]-1, item_user_matrix.shape[1]-1)
svd = TruncatedSVD(n_components=n_components, random_state=42)
item_matrix_compressed = svd.fit_transform(item_user_matrix)

print("Computing Similarity...")
similarity_matrix = cosine_similarity(item_matrix_compressed)
movie_titles = pd.Series(item_user_matrix.index)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search_movies():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    # Simple substring match for autocomplete (regex=False prevents crash on special characters like parenthesis)
    matches = movie_titles[movie_titles.str.lower().str.contains(query, regex=False)].head(10).tolist()
    return jsonify(matches)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    movie_title = data.get('movie_title')
    
    # Log the search query to the SQLite database
    import sqlite3
    db_status = "success"
    try:
        # Added timeout=10 to help if the database is locked by VS Code
        conn = sqlite3.connect('data/movies.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO search_logs (search_query) VALUES (?)", (movie_title,))
        conn.commit()
        conn.close()
    except Exception as e:
        db_status = f"Error: {str(e)}"
        with open("db_error.log", "w") as f:
            f.write(db_status)
        print(f"Error logging to database: {e}")

    if not movie_title or movie_title not in movie_titles.values:
        return jsonify({"error": "Movie not found"}), 404
        
    idx = movie_titles[movie_titles == movie_title].index[0]
    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Top 5 recommendations
    top_5 = sim_scores[1:6]
    recommendations = []
    
    for movie_idx, score_val in top_5:
        title = movie_titles.iloc[movie_idx]
        score = round(score_val * 100, 1)  # cosine similarity as a percentage
        recommendations.append({
            "title": title,
            "match_score": score
        })
        
    return jsonify(recommendations)

@app.route('/api/trending', methods=['GET'])
def trending_searches():
    import sqlite3
    try:
        conn = sqlite3.connect('data/movies.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT search_query, timestamp FROM search_logs ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        conn.close()
        trending = [{"query": row[0], "timestamp": row[1]} for row in rows]
        return jsonify(trending)
    except Exception as e:
        print(f"Error fetching trending: {e}")
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
