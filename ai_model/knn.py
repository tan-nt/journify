from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from database.article import article
import pandas as pd

def preprocess_and_fit_knn(df, k=5):
    df['content'] = df['title'].fillna('') + ' ' + df['abstract'].fillna('')
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['content'])

    # Fit a Nearest Neighbors model
    knn = NearestNeighbors(n_neighbors=k, metric='cosine')
    knn.fit(tfidf_matrix)
    return knn, tfidf, df

def filter_articles(query, knn, tfidf, df):
    query_vec = tfidf.transform([query])  # Vectorize the query
    distances, indices = knn.kneighbors(query_vec)  # Get k nearest articles
    return df.iloc[indices[0]]  # Return filtered articles as a DataFrame

knn, tfidf, df = preprocess_and_fit_knn(pd.DataFrame(article.read_articles()))