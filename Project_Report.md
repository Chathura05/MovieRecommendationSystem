# Movie Recommendation System - Final Project Report

## 1. Introduction & Objectives
The objective of this project was to design and implement a machine learning-powered Movie Recommendation System. The system was developed by applying a rigorous data science backend pipeline that mirrors industry standards—progressing from raw data ingestion to data cleaning, exploratory analysis, preprocessing, and finally mathematical modeling. To make the model accessible and interactive, the pipeline was deployed as a full-stack Flask web application featuring a modern, premium user interface.

## 2. Phase 1: Data Ingestion & Audit
The dataset chosen for this project was the industry-standard **MovieLens (Small)** dataset, which contains over 100,000 ratings applied to 9,000 movies by 600 users.
- Two primary files were ingested using Pandas: `movies.csv` (containing structural meta-tags like titles and genres) and `ratings.csv` (containing user interaction scores).
- Initial dimensionality checks and memory audits were performed via `df.info()` and `df.describe()` to establish a baseline understanding of dataset completeness and identify necessary preprocessing bounds.

## 3. Phase 2: Data Cleaning Pipeline
To ensure the machine learning model received pure inputs, the datasets underwent a stringent cleaning pipeline:
- **Merging**: The ratings and movies datasets were merged on the common key `movieId`.
- **Structural Pruning**: Irrelevant structural variables that do not contribute to long-term content similarity (such as the UNIX `timestamp` of the rating) were permanently dropped from the data frame.
- **Deduplication**: The dataset was scanned for identical duplicate rows, ensuring the model would not overfit to repeated identical samples.
- **Formatting**: Layout column names were standardized to snake_case (e.g., `userId` to `user_id`) to ensure safe programmatic access across the pipeline.

## 4. Phase 3: Exploratory Data Analysis (EDA)
Visual analysis was conducted using `matplotlib` and `seaborn` to uncover hidden trends and statistical distributions within the movie ratings:
- **Rating Distributions**: A histogram revealed that the majority of users rate movies between 3.0 and 4.0 stars. There is a psychological bias towards positive ratings, with very few 0.5 or 1.0 star ratings assigned.
- **Count vs. Average**: Scatter plots and correlation heatmaps demonstrated the relationship between a movie's average rating and its total number of ratings. The data proved that highly rated movies generally have a higher count of ratings (indicating popular consensus), whereas obscure movies with high ratings often suffer from small sample size biases.
- **Extreme Values**: Boxplots successfully identified outlier rating trends, assisting in understanding user behavior extremes.

## 5. Phase 4: Data Preprocessing & Compression
To prepare the categorical and numerical strings for the recommendation algorithm, the data structure was fundamentally transformed:
- **User-Item Matrix**: The linear dataframe was pivoted into a sparse User-Item Matrix where rows represented unique users, columns represented unique movie titles, and cell values held the rating. Unrated movies were populated with `0.0`.
- **Dimensionality Reduction (TruncatedSVD)**: Because the User-Item matrix is highly sparse (most users have only seen a fraction of the 9,000 movies), **Truncated Singular Value Decomposition (SVD)** was applied. This mathematically compressed the high-dimensional sparse array down to 20 dense principal components, extracting the latent "features" or "concepts" of the movies without relying on explicit genre tags.

## 6. Phase 5: Recommendation Engine
With the movie data successfully compressed into a dense mathematical space, the predictive engine was built:
- **Cosine Similarity**: The algorithm measures the cosine of the angle between two movie vectors projected in a multi-dimensional space. Movies that are highly similar in latent features (e.g., *Toy Story* and *A Bug's Life*) point in the exact same direction, yielding a similarity score close to 1.0 (or 100%).
- The engine dynamically accepts a target movie, calculates the cosine distance against all other 9,000 compressed movie vectors, and returns the top 5 highest-matching results.

## 7. Phase 6: Web Application Deployment
To demonstrate the pipeline's effectiveness, a front-end application was engineered:
- **Backend**: A **Flask** server acts as the API. It caches the computed similarity matrix in memory, allowing it to process recommendation requests in milliseconds.
- **Frontend UI/UX**: An interactive web page was built using HTML, CSS, and Vanilla JavaScript. The design strictly adheres to premium, modern aesthetic standards—featuring dark mode, frosted glass elements (glassmorphism), vibrant gradient micro-animations, and dynamic autocomplete search bars.
- **Integration**: The front end communicates with the Flask backend asynchronously via JSON fetches, preventing page reloads and providing a seamless, state-of-the-art user experience.

## 8. Conclusion
The Movie Recommendation System successfully bridges raw data analytics with accessible software engineering. By adapting a structured, 5-step data science methodology, the project successfully cleans, analyzes, and compresses massive datasets to generate highly accurate, mathematically sound movie recommendations in real-time.
