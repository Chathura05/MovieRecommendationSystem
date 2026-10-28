import pandas as pd

def clean_data(movies, ratings):
    print("\n--- STEP 2: DATA CLEANING PIPELINE ---")
    
    # Check missing values
    print("Missing values in movies:")
    print(movies.isnull().sum())
    print("\nMissing values in ratings:")
    print(ratings.isnull().sum())
    
    # Merge datasets
    df = pd.merge(ratings, movies, on='movieId')
    
    # Drop irrelevant variables (timestamp)
    df.drop(columns=['timestamp'], inplace=True, errors='ignore')
    
    # Deduplication
    duplicate_count = df.duplicated().sum()
    print(f"\nFound {duplicate_count} duplicate rows. Dropping them...")
    df.drop_duplicates(inplace=True)
    
    # Rename columns for consistency
    df.rename(columns={'userId': 'user_id', 'movieId': 'movie_id'}, inplace=True)
    
    print("\nData cleaning complete. Final structure:")
    df.info()
    
    # Save processed data
    df.to_csv("../data/processed/merged_cleaned_data.csv", index=False)
    print("Cleaned data saved to '../data/processed/merged_cleaned_data.csv'.")
    
    return df

if __name__ == "__main__":
    movies = pd.read_csv("../data/raw/movies.csv")
    ratings = pd.read_csv("../data/raw/ratings.csv")
    clean_data(movies, ratings)
