from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from database.article import article_model
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

def preprocess_and_fit_knn(df, title_weight=0.7, abstract_weight=0.3):
    # Check if 'title' and 'abstract' columns exist, otherwise use empty strings
    title = df.get('title', pd.Series([''] * len(df)))
    abstract = df.get('abstract', pd.Series([''] * len(df)))
    
    # Remove any rows where both title and abstract are empty
    df['content'] = title.fillna('') + ' ' + abstract.fillna('')
    df['content'] = df['content'].str.strip()
    df = df[df['content'] != '']
    
    if df.empty:
        print("No valid content to process.")
        return None, None, None, df
    
    # Initialize a single TF-IDF Vectorizer for both title and abstract
    tfidf = TfidfVectorizer(stop_words='english')
    
    # Fit the TF-IDF vectorizer on the combined content
    tfidf.fit(df['content'])
    
    # Transform the title and abstract separately using the same vectorizer
    title_matrix = tfidf.transform(df['title'].fillna(''))
    abstract_matrix = tfidf.transform(df['abstract'].fillna(''))
    
    # Combine title and abstract matrices with weighting
    combined_matrix = title_weight * title_matrix + abstract_weight * abstract_matrix
    
    # Fit the KNN model on the combined matrix
    knn = NearestNeighbors(metric='cosine')
    knn.fit(combined_matrix)
    
    # Return KNN model and both TF-IDF vectorizers
    return knn, tfidf, df

def filter_articles_knn(query, knn, tfidf, df, threshold=0.8, max_results=10, title_weight=0.7, abstract_weight=0.3):
    query_title_vec = tfidf.transform([query])
    query_abstract_vec = tfidf.transform([query])
    query_vec = title_weight * query_title_vec + abstract_weight * query_abstract_vec
    
    distances, indices = knn.kneighbors(query_vec, n_neighbors=len(df))
    result_tuples = [(idx, dist) for idx, dist in zip(indices[0], distances[0]) if dist <= threshold]
    
    # If no results within threshold, return top 3 closest results
    if not result_tuples:
        result_tuples = sorted([(idx, dist) for idx, dist in zip(indices[0], distances[0])])[:3]
    
    result_tuples = sorted(result_tuples, key=lambda x: x[1])[:max_results]
    filtered_df = df.iloc[[idx for idx, _ in result_tuples]].copy()
    filtered_df['score'] = [1 - dist for _, dist in result_tuples]
    filtered_df['model'] = 'KNN'
    
    return filtered_df

knn, tfidf, df = preprocess_and_fit_knn(pd.DataFrame(article_model.read_articles()))

def preprocess_and_fit_hnsw(df, title_weight=0.7, abstract_weight=0.3):
    title = df.get('title', pd.Series([''] * len(df)))
    abstract = df.get('abstract', pd.Series([''] * len(df)))
    
    df['content'] = title.fillna('') + ' ' + abstract.fillna('')
    df['content'] = df['content'].str.strip()
    df = df[df['content'] != '']
    
    if df.empty:
        print("No valid content to process.")
        return None, None, df
    
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    # Generate separate embeddings for title and abstract
    title_embeddings = model.encode(df['title'].fillna('').tolist(), convert_to_tensor=False)
    abstract_embeddings = model.encode(df['abstract'].fillna('').tolist(), convert_to_tensor=False)
    
    # Combine title and abstract embeddings with weighting
    embeddings = title_weight * np.array(title_embeddings) + abstract_weight * np.array(abstract_embeddings)
    embeddings = embeddings.astype('float32')
    
    # Initialize FAISS HNSW index
    dimension = embeddings.shape[1]
    index = faiss.IndexHNSWFlat(dimension, 32)
    index.hnsw.efConstruction = 200
    index.add(embeddings)
    
    return index, model, df

def filter_articles_hnsw(query, index, model, df, threshold=0.8, max_results=10):
    query_embedding = model.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, len(df))
    result_tuples = [(idx, dist) for idx, dist in zip(indices[0], distances[0]) if dist <= threshold]
    
    # If no results within threshold, return top 3 closest results
    if not result_tuples:
        result_tuples = sorted([(idx, dist) for idx, dist in zip(indices[0], distances[0])])[:3]
    
    result_tuples = sorted(result_tuples, key=lambda x: x[1])[:max_results]
    filtered_df = df.iloc[[idx for idx, _ in result_tuples]].copy()
    filtered_df['score'] = [1 - dist for _, dist in result_tuples]
    filtered_df['model'] = 'HNSW'
    
    return filtered_df

index, model, hnsw_df = preprocess_and_fit_hnsw(df)