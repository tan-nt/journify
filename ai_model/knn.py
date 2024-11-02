from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from database.article import article
import pandas as pd

def preprocess_and_fit_knn(df, k=5):
    # Check if 'title' and 'abstract' columns exist, otherwise use empty strings
    title = df.get('title', pd.Series([''] * len(df)))  # Default to empty if 'title' is missing
    abstract = df.get('abstract', pd.Series([''] * len(df)))  # Default to empty if 'abstract' is missing
    
    # Combine 'title' and 'abstract' into 'content'
    df['content'] = title.fillna('') + ' ' + abstract.fillna('')
    
    # Drop rows where 'content' is empty (only whitespace)
    df['content'] = df['content'].str.strip()  # Remove any leading/trailing whitespace
    df = df[df['content'] != '']  # Keep only rows with non-empty content
    
    # Check if there are any rows left after dropping empty content
    if df.empty:
        print("No valid content to process.")
        return None, None, df
    
    # Initialize TF-IDF Vectorizer with English stop words
    tfidf = TfidfVectorizer(stop_words='english')
    
    try:
        tfidf_matrix = tfidf.fit_transform(df['content'])
    except ValueError as e:
        print(f"Error: {e}")
        return None, None, df
    
    # Fit a Nearest Neighbors model
    knn = NearestNeighbors(n_neighbors=k, metric='cosine')
    knn.fit(tfidf_matrix)
    
    return knn, tfidf, df

def filter_articles(query, knn, tfidf, df):
    query_vec = tfidf.transform([query])  # Vectorize the query
    distances, indices = knn.kneighbors(query_vec)  # Get k nearest articles
    return df.iloc[indices[0]]  # Return filtered articles as a DataFrame

knn, tfidf, df = preprocess_and_fit_knn(pd.DataFrame(article.read_articles()))