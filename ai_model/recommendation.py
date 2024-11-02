from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from database.article import article_model
from database.user_access_log import user_access_logger_model
from database.user import user_model

def content_based_recommendation(user_history, articles, num_recommendations=5):
    try:
        # Concatenate title and abstract for TF-IDF analysis
        articles['content'] = articles['title'] + " " + articles['abstract']
        
        # Generate TF-IDF matrix for all articles
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(articles['content'])
        
        # Calculate cosine similarity matrix for all articles
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        # Collect similarity scores for each viewed article against non-viewed articles
        recommendations = []
        for article_id in user_history:
            # Get index of each viewed article
            idx = articles.index[articles['article_id'] == article_id][0]
            
            # Get similarity scores of the viewed article to all other articles
            sim_scores = list(enumerate(similarity_matrix[idx]))
            
            # Sort by similarity scores and filter out viewed articles
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            # Collect recommendations excluding already viewed articles
            for i, score in sim_scores:
                if articles.iloc[i]['article_id'] not in user_history:
                    recommendations.append(articles.iloc[i]['article_id'])
                    
                # Stop if we have enough recommendations
                if len(recommendations) >= num_recommendations:
                    break
                    
        # Return top unique recommendations
        return list(dict.fromkeys(recommendations))[:num_recommendations]
    
    except Exception as e:
        print(f"Error in content_based_recommendation: {e}")
        return []


def collaborative_filtering(user_id, user_access_logs, num_recommendations=5):
    try:
        # Pivot table to create a user-item interaction matrix
        interaction_matrix = user_access_logs.pivot_table(index='user_id', columns='article_id', aggfunc='size', fill_value=0)
        
        # Calculate cosine similarity between users
        user_similarity = cosine_similarity(interaction_matrix)
        user_similarity_df = pd.DataFrame(user_similarity, index=interaction_matrix.index, columns=interaction_matrix.index)
        
        # Find similar users
        similar_users = user_similarity_df[user_id].sort_values(ascending=False).index[1:num_recommendations + 1]
        
        # Get articles viewed by similar users but not by the current user
        viewed_by_similar_users = user_access_logs[user_access_logs['user_id'].isin(similar_users)]
        viewed_by_similar_users = viewed_by_similar_users[~viewed_by_similar_users['article_id'].isin(interaction_matrix.loc[user_id].index)]
        
        # Recommend articles that are popular among similar users
        recommendations = viewed_by_similar_users['article_id'].value_counts().head(num_recommendations).index.tolist()
        
        return recommendations
    
    except Exception as e:
        print(f"Error in collaborative_filtering: {e}")
        return []


def hybrid_recommendation_of_content_collaborative_filtering(user_id, num_recommendations=5):
    try:
        user_access_logs = user_access_logger_model.list_user_access_log()
        user_access_logs = pd.DataFrame(user_access_logs)
        articles = article_model.read_articles()
        articles = pd.DataFrame(articles)
        
        user_access_logs = user_access_logs.rename(columns={'ip_address': 'user_id'})
        
        # Get user history
        user_history = user_access_logs[user_access_logs['user_id'] == user_id]['article_id'].tolist()
        
        # Content-based recommendations
        content_recs = content_based_recommendation(user_history, articles, num_recommendations=3*num_recommendations)
        
        # Collaborative filtering recommendations
        collaborative_recs = collaborative_filtering(user_id, user_access_logs, num_recommendations=3*num_recommendations)
        
        # Combine recommendations with a preference for content-based results
        combined_recommendations = content_recs + collaborative_recs
        # Ensure unique recommendations
        unique_recommendations = list(dict.fromkeys(combined_recommendations))[:num_recommendations]
        
        # Get article details for each recommendation
        recommended_articles = articles[articles['article_id'].isin(unique_recommendations)][['article_id', 'title', 'abstract']]
        return recommended_articles.to_dict(orient='records')
    
    except Exception as e:
        print(f"Error in hybrid_recommendation_of_content_collaborative_filtering: {e}")
        return []


def other_friends_recommend(user_id, num_recommendations=5):
    try:
        user_access_logs = user_access_logger_model.list_user_access_log()
        user_access_logs = pd.DataFrame(user_access_logs)
        articles = article_model.read_articles()
        articles = pd.DataFrame(articles)
        
        # Ensure user_access_logs and articles have the required columns
        user_access_logs = user_access_logs.rename(columns={'ip_address': 'user_id'})
        friend_ids = user_model.read_random_ip_addresses()
        
        # Filter out articles accessed by the current user
        user_history = user_access_logs[user_access_logs['user_id'] == user_id]['article_id'].tolist()
        
        # Step 1: Get articles accessed by friends but not by the current user
        friend_logs = user_access_logs[user_access_logs['user_id'].isin(friend_ids)]
        friend_recommendations = friend_logs[~friend_logs['article_id'].isin(user_history)]['article_id'].value_counts().index.tolist()
        
        # If we have enough friend-based recommendations, return them
        if len(friend_recommendations) >= num_recommendations:
            friend_recommended_articles = articles[articles['article_id'].isin(friend_recommendations[:num_recommendations])]
            return friend_recommended_articles[['article_id', 'title', 'abstract']].to_dict(orient='records')

        # Step 2: If not enough recommendations, use collaborative filtering based on similar users
        interaction_matrix = user_access_logs.pivot_table(index='user_id', columns='article_id', aggfunc='size', fill_value=0)
        
        # Calculate user similarity
        user_similarity = cosine_similarity(interaction_matrix)
        user_similarity_df = pd.DataFrame(user_similarity, index=interaction_matrix.index, columns=interaction_matrix.index)
        
        # Find similar users
        similar_users = user_similarity_df[user_id].sort_values(ascending=False).index[1:num_recommendations + 1]
        
        # Get articles accessed by similar users but not by the current user
        similar_user_logs = user_access_logs[user_access_logs['user_id'].isin(similar_users)]
        collaborative_recommendations = similar_user_logs[~similar_user_logs['article_id'].isin(user_history)]['article_id'].value_counts().index.tolist()
        
        # Combine friend and collaborative recommendations
        combined_recommendations = friend_recommendations + collaborative_recommendations
        unique_recommendations = list(dict.fromkeys(combined_recommendations))[:num_recommendations]
        
        if len(unique_recommendations) >= num_recommendations:
            recommended_articles = articles[articles['article_id'].isin(unique_recommendations)]
            return recommended_articles[['article_id', 'title', 'abstract']].to_dict(orient='records')
        
        # Step 3: If still not enough recommendations, fallback to random popular articles
        remaining_count = num_recommendations - len(unique_recommendations)
        random_articles = articles.sample(remaining_count) if remaining_count > 0 else pd.DataFrame()

        # Combine all results using pd.concat instead of .append
        all_recommended_articles = pd.concat([articles[articles['article_id'].isin(unique_recommendations)], random_articles])

        return all_recommended_articles[['article_id', 'title', 'abstract']].to_dict(orient='records')
    
    except Exception as e:
        print(f"Error in other_friends_recommend: {e}")
        return []
