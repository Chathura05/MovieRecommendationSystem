import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_eda(df):
    print("\n--- STEP 3: EXPLORATORY DATA ANALYSIS (EDA) ---")
    
    # Check if the column 'title' exists
    if 'title' not in df.columns or 'rating' not in df.columns:
        print("Required columns ('title', 'rating') are missing for EDA.")
        return
    
    # 1. Rating counts and averages per movie
    movie_stats = df.groupby('title')['rating'].agg(['count', 'mean']).reset_index()
    movie_stats.columns = ['title', 'rating_count', 'rating_mean']
    
    # We will save the plots to a directory instead of plt.show() which might block
    os.makedirs('../data/processed/plots', exist_ok=True)
    
    # Correlation Heatmap
    print("Generating Correlation Heatmap...")
    plt.figure(figsize=(6, 4))
    sns.heatmap(movie_stats[['rating_count', 'rating_mean']].corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation: Rating Count vs Average Rating')
    plt.savefig('../data/processed/plots/correlation_heatmap.png')
    plt.close()
    
    # Boxplot of Rating Distribution
    print("Generating Boxplot for Ratings...")
    plt.figure(figsize=(6, 4))
    sns.boxplot(x=df['rating'])
    plt.title('Boxplot of Movie Ratings')
    plt.savefig('../data/processed/plots/boxplot_ratings.png')
    plt.close()
    
    # Scatter plot: Highly-rated vs Frequently-rated
    print("Generating Scatter Plot...")
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='rating_mean', y='rating_count', data=movie_stats, alpha=0.5)
    plt.title('Scatter Plot: Average Rating vs Rating Count')
    plt.savefig('../data/processed/plots/scatter_ratings.png')
    plt.close()
    
    # Histogram of Ratings
    print("Generating Histogram of Ratings...")
    plt.figure(figsize=(6, 4))
    sns.histplot(df['rating'], bins=10, kde=True)
    plt.title('Distribution of Ratings')
    plt.savefig('../data/processed/plots/histogram_ratings.png')
    plt.close()
    
    print("EDA plots saved in 'data/processed/plots/'.")

if __name__ == "__main__":
    df = pd.read_csv("../data/processed/merged_cleaned_data.csv")
    run_eda(df)
