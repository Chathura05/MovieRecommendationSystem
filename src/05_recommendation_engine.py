import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

def get_recommendations(movie_title, user_item_matrix, k=5):
    print(f"\n--- STEP 5: RECOMMENDATION ENGINE ---")
    print(f"Generating top {k} recommendations for: '{movie_title}'")
    
    # Transpose to Item-User matrix so we can find similar items (movies)
    item_user_matrix = user_item_matrix.T
    
    # Apply SVD on items for compression
    n_components = min(20, item_user_matrix.shape[0]-1, item_user_matrix.shape[1]-1)
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    item_matrix_compressed = svd.fit_transform(item_user_matrix)
    
    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(item_matrix_compressed)
    
    movie_indices = pd.Series(item_user_matrix.index)
    
    if movie_title not in movie_indices.values:
        print(f"Movie '{movie_title}' not found in the dataset.")
        # Print a few available movies for convenience
        print(f"Available examples: {', '.join(movie_indices.head(3).values)}")
        return
        
    idx = movie_indices[movie_indices == movie_title].index[0]
    
    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get top k similar movies (excluding the target movie itself)
    top_k_indices = [i[0] for i in sim_scores[1:k+1]]
    top_k_movies = movie_indices.iloc[top_k_indices]
    
    print("\nTop Recommendations:")
    for i, title in enumerate(top_k_movies, 1):
        print(f"{i}. {title} (Similarity: {sim_scores[top_k_indices[i-1]][1]:.4f})")

if __name__ == "__main__":
    df = pd.read_csv("../data/processed/merged_cleaned_data.csv")
    user_item_matrix = df.pivot_table(index='user_id', columns='title', values='rating', aggfunc='mean').fillna(0)
    
    target_movie = "Toy Story (1995)"
    get_recommendations(target_movie, user_item_matrix)
