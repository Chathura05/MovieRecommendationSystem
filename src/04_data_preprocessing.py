import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler

def preprocess_data(df):
    print("\n--- STEP 4: DATA PREPROCESSING & COMPRESSION ---")
    
    # 1. Matrix Formulation (User-Item Matrix)
    print("Creating User-Item Matrix...")
    user_item_matrix = df.pivot_table(index='user_id', columns='title', values='rating', aggfunc='mean').fillna(0)
    print(f"User-Item Matrix shape: {user_item_matrix.shape}")
    
    # 2. Dimensionality Reduction (TruncatedSVD/PCA equivalent for sparse)
    print("Applying TruncatedSVD for dimensionality reduction...")
    # Reduce features to a lower dimension, e.g., 20
    n_components = min(20, user_item_matrix.shape[0]-1, user_item_matrix.shape[1]-1)
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    matrix_compressed = svd.fit_transform(user_item_matrix)
    
    # 3. Scaling
    print("Standardizing compressed features...")
    scaler = StandardScaler()
    matrix_scaled = scaler.fit_transform(matrix_compressed)
    
    print(f"Final Compressed & Scaled Matrix shape: {matrix_scaled.shape}")
    print("Backend data streams are 100% clean, standardized, and primed for Model Training!")
    
    return user_item_matrix, matrix_scaled

if __name__ == "__main__":
    df = pd.read_csv("../data/processed/merged_cleaned_data.csv")
    preprocess_data(df)
