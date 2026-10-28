# Movie Recommendation System

A machine learning data science pipeline and full-stack web application that predicts and recommends movies using Truncated Singular Value Decomposition (SVD).

## Overview
This project processes the **MovieLens (Small)** dataset (100,000+ ratings) to build a personalized recommendation engine. It features a complete 5-step data science pipeline:
1. **Data Ingestion**: Loading and auditing raw datasets.
2. **Data Cleaning**: Handling missing values, deduplication, and structural pruning.
3. **Exploratory Data Analysis (EDA)**: Visualizing rating distributions and correlations.
4. **Data Preprocessing**: Dimensionality reduction (TruncatedSVD) on sparse User-Item matrices.
5. **Recommendation Engine**: Cosine similarity calculations for predictions.

## Project Structure
- `data/raw/`: Contains the raw `movies.csv` and `ratings.csv`.
- `data/processed/`: Contains the cleaned dataset and generated EDA plots.
- `src/`: Contains the 5 Python scripts executing the core backend pipeline.
- `app.py`: The Flask web server.
- `templates/` & `static/`: Frontend HTML, CSS, and JS files for the premium user interface.

## How to Run

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Data Pipeline (Optional)**
   Navigate to the `src` folder and execute the scripts sequentially to regenerate the processed data and EDA plots.
   ```bash
   cd src
   python 01_data_ingestion.py
   python 02_data_cleaning.py
   python 03_exploratory_data_analysis.py
   python 04_data_preprocessing.py
   python 05_recommendation_engine.py
   ```

3. **Start the Web Application**
   Run the Flask server from the root directory:
   ```bash
   python app.py
   ```
   Then navigate to `http://127.0.0.1:5000` in your web browser to interact with the CineMatch AI.
