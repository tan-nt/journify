import streamlit as st
from database.article import article_model
from database.user import user_model
import pandas as pd
import plotly.express as px
import numpy as np # linear algebra
import pandas as pd # data processing
import os
import tweepy as tw #for accessing Twitter API
from wordcloud import WordCloud, STOPWORDS
from sklearn.preprocessing import LabelEncoder
import plotly.express as px

#For Preprocessing
import re    # RegEx for removing non-letter characters
import nltk  #natural language processing
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.stem.porter import *
from sklearn.feature_extraction.text import CountVectorizer

# For Building the model
from sklearn.model_selection import train_test_split
import tensorflow as tf
import seaborn as sns

#For data visualization
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def display_article_analysis():
    data = article_model.read_articles()  # Load data into a DataFrame
    df = pd.DataFrame(data)
    st.header("Artile Data Exploration and Analytics")
    # Section 1: Raw Analysis
    st.subheader("Session 1: 📊 Raw Data Analysis")
    st.info(f"Dataset contains {len(df)} rows and {len(df.columns)} columns.")

    # Display the first few rows of the dataset
    st.write("### Sample Data")
    st.write(df.head())

    # Create three columns for each section to display side by side
    col1, col2 = st.columns(2)

    # Display "Missing Values Summary" table in the first column
    with col1:
        st.write("### Missing Values Summary")
        missing_values = df.isna().sum() + (df == "").sum()
        missing_values = missing_values[missing_values > 0]
        missing_df = missing_values.reset_index()
        missing_df.columns = ["Column", "Missing or Empty Values"]
        st.table(missing_df)

    # Display "Data Types" table in the second column
    with col2:
        st.write("### Data Types")
        data_types_df = pd.DataFrame(df.dtypes, columns=["Data Type"]).reset_index()
        data_types_df.columns = ["Column", "Data Type"]
        st.table(data_types_df)

    # CSS styling to expand the width of all displayed tables in Streamlit
    st.markdown("""
        <style>
        /* Apply full width to tables in Streamlit */
        .streamlit-table {
            width: 100% !important;
        }
        .stDataFrame, .stTable, .stMarkdown table {
            width: 100% !important;
            display: block;
            overflow-x: auto;
        }
        </style>
    """, unsafe_allow_html=True)

    # Section 2: Descriptive Statistics
    st.subheader("Session 2: 📈 Descriptive Statistics")
    st.write("Below are the descriptive statistics for the numerical columns in the dataset.")
    st.table(df.describe().T)  # Using st.table for a consistent table layout

    # Section 3: Detailed Analysis and Visualization
    st.subheader("Session 3: 📉 Detailed Analysis and Visualizations")
    st.info("This section includes detailed visualizations and analysis of specific fields.")

    # Example 1: Distribution of Articles by Category
    st.subheader("Distribution of Articles by Category")
    if 'categories' in df.columns:
        category_counts = df['categories'].value_counts()
        fig1 = px.bar(category_counts, x=category_counts.index, y=category_counts.values,
                      labels={'x': 'Categories', 'y': 'Number of Articles'},
                      title="Articles by Category")
        st.plotly_chart(fig1, use_container_width=True)

    # Example 2: Top Authors by Article Count
    st.subheader("Top Authors by Article Count")
    if 'authors' in df.columns:
        # Split authors if multiple authors are joined by a separator (e.g., ",")
        df['authors'] = df['authors'].str.split(',')
        author_counts = pd.Series([author.strip() for authors in df['authors'].dropna() for author in authors]).value_counts()
        fig2 = px.bar(author_counts.head(10), x=author_counts.index[:10], y=author_counts.values[:10],
                      labels={'x': 'Authors', 'y': 'Number of Articles'},
                      title="Top 10 Authors")
        st.plotly_chart(fig2, use_container_width=True)

    # Example 3: Publication Trends Over Time
    # Convert 'update_date' to datetime format if it exists in the dataframe
    if 'update_date' in df.columns:
        try:
            df['update_date'] = pd.to_datetime(df['update_date'], errors='coerce')
            df = df.dropna(subset=['update_date'])  # Drop rows where conversion failed (optional)
            df['year'] = df['update_date'].dt.year
            year_counts = df.groupby('year').size()

            # Plot the data
            fig3 = px.line(year_counts, x=year_counts.index, y=year_counts.values,
                           labels={'x': 'Year', 'y': 'Number of Articles'},
                           title="Publication Trends by Year")
            st.plotly_chart(fig3, use_container_width=True)
        except Exception as e:
            st.error(f"Error processing date column: {e}")
    else:
        st.warning("The 'update_date' column is not available in the dataset.")

    # Example 4: Article Abstract Length Distribution
    st.subheader("Article Abstract Length Distribution")
    if 'abstract' in df.columns:
        df['abstract_length'] = df['abstract'].str.len()  # Calculate abstract length
        fig4 = px.histogram(df, x='abstract_length', nbins=30,
                            title="Distribution of Article Abstract Lengths",
                            labels={'abstract_length': 'Abstract Length (characters)'})
        st.plotly_chart(fig4, use_container_width=True)
        
    # 5. Trend of Articles Published by Category Over Time
    st.subheader("Trend of Articles Published by Category Over Time")
    if 'categories' in df.columns and 'update_date' in df.columns:
        df['update_date'] = pd.to_datetime(df['update_date'], errors='coerce')
        df['year'] = df['update_date'].dt.year
        category_trends = df.groupby(['year', 'categories']).size().reset_index(name='count')
        fig5 = px.line(category_trends, x='year', y='count', color='categories',
                       labels={'year': 'Year', 'count': 'Number of Articles'},
                       title="Publication Trend by Category")
        st.plotly_chart(fig5, use_container_width=True)

    # 6. Top Journals by Number of Articles
    st.subheader("Top Journals by Number of Articles")
    if 'journal_ref' in df.columns:
        journal_counts = df['journal_ref'].value_counts().head(10)
        fig6 = px.bar(journal_counts, x=journal_counts.index, y=journal_counts.values,
                      labels={'x': 'Journal', 'y': 'Number of Articles'},
                      title="Top 10 Journals by Article Count")
        st.plotly_chart(fig6, use_container_width=True)

    # 7. Average Abstract Length by Category
    st.subheader("Average Abstract Length by Category")
    if 'abstract' in df.columns and 'categories' in df.columns:
        df['abstract_length'] = df['abstract'].str.len()
        avg_abstract_length = df.groupby('categories')['abstract_length'].mean().sort_values(ascending=False).head(10)
        fig7 = px.bar(avg_abstract_length, x=avg_abstract_length.index, y=avg_abstract_length.values,
                      labels={'x': 'Categories', 'y': 'Average Abstract Length'},
                      title="Average Abstract Length by Category")
        st.plotly_chart(fig7, use_container_width=True)

    # 8. License Distribution
    st.subheader("License Distribution")
    if 'license' in df.columns:
        license_counts = df['license'].value_counts()
        fig8 = px.pie(license_counts, names=license_counts.index, values=license_counts.values,
                      title="Distribution of Article Licenses")
        st.plotly_chart(fig8, use_container_width=True)

    # 9. Number of Versions per Article
    st.subheader("Number of Versions per Article")
    if 'versions' in df.columns:
        df['version_count'] = df['versions'].str.count(';') + 1  # Assuming ';' separates versions
        fig9 = px.histogram(df, x='version_count', nbins=10,
                            title="Distribution of Number of Versions per Article",
                            labels={'version_count': 'Number of Versions'})
        st.plotly_chart(fig9, use_container_width=True)

    # 10. Submission Frequency by Month
    st.subheader("Submission Frequency by Month")
    if 'update_date' in df.columns:
        df['month'] = df['update_date'].dt.month
        month_counts = df['month'].value_counts().sort_index()
        fig10 = px.bar(month_counts, x=month_counts.index, y=month_counts.values,
                       labels={'x': 'Month', 'y': 'Number of Submissions'},
                       title="Submission Frequency by Month")
        st.plotly_chart(fig10, use_container_width=True)
        
def display_user_logger_analysis():
    data = user_model.read_user_access()  # Load data into a DataFrame
    df = pd.DataFrame(data)
    # Convert all object-type columns to string to ensure compatibility
    df = df.astype({col: "string" for col in df.select_dtypes(include="object").columns})
    # Replace NaN with an empty string (or you could use fillna if preferred)
    df = df.fillna("")
    st.header("User Logger Data Exploration and Analytics")
    # Section 1: Raw Analysis
    st.subheader("Session 1: 📊 Raw Data Analysis")
    st.info(f"Dataset contains {len(df)} rows and {len(df.columns)} columns.")

    # Display the first few rows of the dataset
    st.write("### Sample Data")
    st.write(df.head())

    # Create three columns for each section to display side by side
    col1, col2 = st.columns(2)

    # Display "Missing Values Summary" table in the first column
    with col1:
        st.write("### Missing Values Summary")
        missing_values = df.isna().sum() + (df == "").sum()
        missing_values = missing_values[missing_values > 0]
        missing_df = missing_values.reset_index()
        missing_df.columns = ["Column", "Missing or Empty Values"]
        st.table(missing_df)

    # Display "Data Types" table in the second column
    with col2:
        st.write("### Data Types")
        data_types_df = pd.DataFrame(df.dtypes, columns=["Data Type"]).reset_index()
        data_types_df.columns = ["Column", "Data Type"]
        st.table(data_types_df)

    # CSS styling to expand the width of all displayed tables in Streamlit
    st.markdown("""
        <style>
        /* Apply full width to tables in Streamlit */
        .streamlit-table {
            width: 100% !important;
        }
        .stDataFrame, .stTable, .stMarkdown table {
            width: 100% !important;
            display: block;
            overflow-x: auto;
        }
        </style>
    """, unsafe_allow_html=True)

    # Section 2: Descriptive Statistics
    st.subheader("Session 2: 📈 Descriptive Statistics")
    st.write("Below are the descriptive statistics for the numerical columns in the dataset.")
    st.table(df.describe().T)  # Using st.table for a consistent table layout

    # Section 3: Detailed Analysis and Visualization
    st.subheader("Session 3: 📉 Detailed Analysis and Visualizations")
    st.info("This section includes detailed visualizations and analysis of specific fields.")

    # Example 1: Distribution of Articles by Category
    st.subheader("Distribution of Articles by Category")
    if 'categories' in df.columns:
        category_counts = df['categories'].value_counts()
        fig1 = px.bar(category_counts, x=category_counts.index, y=category_counts.values,
                      labels={'x': 'Categories', 'y': 'Number of Articles'},
                      title="Articles by Category")
        st.plotly_chart(fig1, use_container_width=True)

    # Example 2: Top Authors by Article Count
    st.subheader("Top Authors by Article Count")
    if 'authors' in df.columns:
        # Split authors if multiple authors are joined by a separator (e.g., ",")
        df['authors'] = df['authors'].str.split(',')
        author_counts = pd.Series([author.strip() for authors in df['authors'].dropna() for author in authors]).value_counts()
        fig2 = px.bar(author_counts.head(10), x=author_counts.index[:10], y=author_counts.values[:10],
                      labels={'x': 'Authors', 'y': 'Number of Articles'},
                      title="Top 10 Authors")
        st.plotly_chart(fig2, use_container_width=True)

    # Example 3: Publication Trends Over Time
    # Convert 'update_date' to datetime format if it exists in the dataframe
    if 'update_date' in df.columns:
        try:
            df['update_date'] = pd.to_datetime(df['update_date'], errors='coerce')
            df = df.dropna(subset=['update_date'])  # Drop rows where conversion failed (optional)
            df['year'] = df['update_date'].dt.year
            year_counts = df.groupby('year').size()

            # Plot the data
            fig3 = px.line(year_counts, x=year_counts.index, y=year_counts.values,
                           labels={'x': 'Year', 'y': 'Number of Articles'},
                           title="Publication Trends by Year")
            st.plotly_chart(fig3, use_container_width=True)
        except Exception as e:
            st.error(f"Error processing date column: {e}")
    else:
        st.warning("The 'update_date' column is not available in the dataset.")

    # Example 4: Article Abstract Length Distribution
    st.subheader("Article Abstract Length Distribution")
    if 'abstract' in df.columns:
        df['abstract_length'] = df['abstract'].str.len()  # Calculate abstract length
        fig4 = px.histogram(df, x='abstract_length', nbins=30,
                            title="Distribution of Article Abstract Lengths",
                            labels={'abstract_length': 'Abstract Length (characters)'})
        st.plotly_chart(fig4, use_container_width=True)
        
    # 5. Trend of Articles Published by Category Over Time
    st.subheader("Trend of Articles Published by Category Over Time")
    if 'categories' in df.columns and 'update_date' in df.columns:
        df['update_date'] = pd.to_datetime(df['update_date'], errors='coerce')
        df['year'] = df['update_date'].dt.year
        category_trends = df.groupby(['year', 'categories']).size().reset_index(name='count')
        fig5 = px.line(category_trends, x='year', y='count', color='categories',
                       labels={'year': 'Year', 'count': 'Number of Articles'},
                       title="Publication Trend by Category")
        st.plotly_chart(fig5, use_container_width=True)

    # 6. Top Journals by Number of Articles
    st.subheader("Top Journals by Number of Articles")
    if 'journal_ref' in df.columns:
        journal_counts = df['journal_ref'].value_counts().head(10)
        fig6 = px.bar(journal_counts, x=journal_counts.index, y=journal_counts.values,
                      labels={'x': 'Journal', 'y': 'Number of Articles'},
                      title="Top 10 Journals by Article Count")
        st.plotly_chart(fig6, use_container_width=True)

    # 7. Average Abstract Length by Category
    st.subheader("Average Abstract Length by Category")
    if 'abstract' in df.columns and 'categories' in df.columns:
        df['abstract_length'] = df['abstract'].str.len()
        avg_abstract_length = df.groupby('categories')['abstract_length'].mean().sort_values(ascending=False).head(10)
        fig7 = px.bar(avg_abstract_length, x=avg_abstract_length.index, y=avg_abstract_length.values,
                      labels={'x': 'Categories', 'y': 'Average Abstract Length'},
                      title="Average Abstract Length by Category")
        st.plotly_chart(fig7, use_container_width=True)

    # 8. License Distribution
    st.subheader("License Distribution")
    if 'license' in df.columns:
        license_counts = df['license'].value_counts()
        fig8 = px.pie(license_counts, names=license_counts.index, values=license_counts.values,
                      title="Distribution of Article Licenses")
        st.plotly_chart(fig8, use_container_width=True)

    # 9. Number of Versions per Article
    st.subheader("Number of Versions per Article")
    if 'versions' in df.columns:
        df['version_count'] = df['versions'].str.count(';') + 1  # Assuming ';' separates versions
        fig9 = px.histogram(df, x='version_count', nbins=10,
                            title="Distribution of Number of Versions per Article",
                            labels={'version_count': 'Number of Versions'})
        st.plotly_chart(fig9, use_container_width=True)

    # 10. Submission Frequency by Month
    st.subheader("Submission Frequency by Month")
    if 'update_date' in df.columns:
        df['month'] = df['update_date'].dt.month
        month_counts = df['month'].value_counts().sort_index()
        fig10 = px.bar(month_counts, x=month_counts.index, y=month_counts.values,
                       labels={'x': 'Month', 'y': 'Number of Submissions'},
                       title="Submission Frequency by Month")
        st.plotly_chart(fig10, use_container_width=True)
        
        
def display_sentiment_analysis():
     # Display title and link to the Kaggle dataset
    st.title("Sentiment Analysis Dataset Exploration.")
    st.markdown(
        """
        [**Twitter and Reddit Sentimental Analysis Dataset on Kaggle**](https://www.kaggle.com/datasets/cosmos98/twitter-and-reddit-sentimental-analysis-dataset/code?datasetId=429085&sortBy=voteCount)
        """
    )
    st.markdown("The simple LSTM will be used for the best efficiency for solving the problem")
    
    st.subheader("Dataset 1: Twitter Sentiment Analysis Data Preview (First 5 rows)")
    df1 = pd.read_csv('database/sentimental_analysis/Twitter_Data.csv')  # Example for df1, adjust as needed
    st.write(df1.head())  # Display the first few rows in Streamlit

    # Load and display second dataset (Reddit data)
    st.subheader("Dataset 2: Reddit Sentiment Analysis Data Preview (First 5 rows)")
    df2 = pd.read_csv('database/sentimental_analysis/Reddit_Data.csv')
    df2 = df2.rename(columns={'clean_comment': 'clean_text'})  # Rename columns
    st.write(df2.head())  # Display the first few rows in Streamlit
    
    df = pd.concat([df1, df2], ignore_index=True)
    # Data Cleaning
    st.header("Data Cleaning")
    st.write("Checking for Missing Values")
    missing_values = df.isnull().sum()
    st.write(missing_values)  # Display missing values count
    st.write("Dropping Missing Values")
    df.dropna(axis=0, inplace=True)

    # Map tweet sentiment categories
    df['category'] = df['category'].map({-1.0: 'Negative', 0.0: 'Neutral', 1.0: 'Positive'})

    # Display cleaned data
    st.write("Cleaned Dataset (First 5 Rows):")
    st.write(df.head())

    # Sentiment Distribution
    st.header("Sentiment Category Distribution")
    sentiment_counts = df['category'].value_counts()
    st.write(sentiment_counts)  # Display sentiment distribution counts
    st.bar_chart(sentiment_counts)  # Display as bar chart

    # Analyze Text Lengths
    st.header("Analysis of Text Lengths")
    st.write("Distribution of Text Lengths (Words per Tweet)")
    data_len = pd.Series([len(tweet.split()) for tweet in df['clean_text']])
    fig, ax = plt.subplots()
    data_len.plot(kind='box', ax=ax)
    st.pyplot(fig)

    # Text Length Distribution for Positive Sentiment
    st.header("Text Length Distribution for Positive Sentiment")
    df['length'] = df['clean_text'].str.split().apply(len)  # Calculate text length

    # Display Histogram and Summary Statistics for Positive Sentiment
    fig = plt.figure(figsize=(14, 7))

    # Histogram for text length of positive sentiment
    ax1 = fig.add_subplot(122)
    sns.histplot(df[df['category'] == 'Positive']['length'], ax=ax1, color='green')
    ax1.set_title("Text Length Distribution (Positive Sentiment)")

    # Summary statistics for positive sentiment text length
    describe = df['length'][df['category'] == 'Positive'].describe().to_frame().round(2)
    ax2 = fig.add_subplot(121)
    ax2.axis('off')
    table = ax2.table(cellText=describe.values, rowLabels=describe.index, bbox=[0, 0, 1, 1], colLabels=describe.columns)
    table.set_fontsize(14)
    fig.suptitle("Distribution of Text Length for Positive Sentiment Tweets", fontsize=16)

    st.pyplot(fig)
        
    # Display text length distribution and summary for Negative sentiment
    st.header("Distribution of Text Length for Negative Sentiment Tweets")
    fig, ax = plt.subplots(1, 2, figsize=(14, 7))
    df['length'] = df['clean_text'].str.split().apply(len)

    # Histogram of text lengths for negative sentiment
    sns.histplot(df[df['category'] == 'Negative']['length'], ax=ax[1], color='red')
    ax[1].set_title("Text Length Distribution (Negative Sentiment)")

    # Summary statistics table for text length of negative sentiment
    describe = df['length'][df['category'] == 'Negative'].describe().to_frame().round(2)
    ax[0].axis('off')
    table = ax[0].table(cellText=describe.values, rowLabels=describe.index, colLabels=describe.columns, bbox=[0, 0, 1, 1])
    table.set_fontsize(14)

    fig.suptitle("Distribution of Text Length for Negative Sentiment Tweets", fontsize=16)
    st.pyplot(fig)

    # Display pie chart of sentiment distribution
    # st.header("Sentiment Distribution of Tweets")
    # fig = px.pie(df, names='category', title='Pie Chart of Different Sentiments of Tweets')
    # st.plotly_chart(fig)

    # Define a function to generate word clouds and display them in Streamlit
    from wordcloud import WordCloud

    def wordcount_gen(data, sentiment):
        st.subheader(f"Word Cloud for {sentiment} Sentiment Tweets")
        words = ' '.join(data[data['category'] == sentiment]['clean_text'])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(words)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

    # Generate word clouds for each sentiment category
    # wordcount_gen(df, 'Positive')
    # wordcount_gen(df, 'Negative')
    # wordcount_gen(df, 'Neutral')

    # # Apply data processing to each tweet
    # st.header("Data Preprocessing and Encoding")
    # X = list(map(tweet_to_words, df['clean_text']))

    # # Encode target labels
    # st.write("Encoding Target Labels")
    # le = LabelEncoder()
    # Y = le.fit_transform(df['category'])
    # st.write("Encoded labels:", le.classes_)

    # # Split dataset into training, testing, and validation sets
    # y = pd.get_dummies(df['category'])
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
    # X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=1)
    # st.write(f"Training set size: {len(X_train)}, Validation set size: {len(X_val)}, Test set size: {len(X_test)}")

    # # Vectorize text data
    # st.header("Text Vectorization using Count Vectorizer")
    # vocabulary_size = 5000
    # count_vector = CountVectorizer(max_features=vocabulary_size, preprocessor=lambda x: x, tokenizer=lambda x: x)

    # # Fit the training data
    # X_train = count_vector.fit_transform(X_train).toarray()
    # X_test = count_vector.transform(X_test).toarray()

    # st.write("Count Vectorization Complete. First 5 Feature Vectors from Training Data:")
    # st.write(X_train[:5])

        

# Function to process a tweet into words
def tweet_to_words(tweet):
    '''Convert tweet text into a sequence of words'''
    
    # Convert to lowercase
    text = tweet.lower()
    
    # Remove non-letter characters
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)
    
    # Tokenize by splitting the string
    words = text.split()
    
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [w for w in words if w not in stop_words]
    
    # Apply stemming
    stemmer = PorterStemmer()
    words = [stemmer.stem(w) for w in words]
    
    # Return the list of words
    return words

# Function to generate and display a word cloud for a given sentiment category
def wordcount_gen(df, category):
    '''
    Generate a word cloud for a specific sentiment category
    Inputs:
    - df: tweets dataset
    - category: Positive/Negative/Neutral
    '''
    
    # Combine all tweets of the given category
    combined_tweets = " ".join(tweet for tweet in df[df['category'] == category]['clean_text'])
    
    # Initialize WordCloud object
    wc = WordCloud(
        background_color='white',
        max_words=50,
        stopwords=STOPWORDS
    )
    
    # Generate the word cloud
    wordcloud = wc.generate(combined_tweets)
    
    # Display word cloud in Streamlit
    st.subheader(f"Word Cloud for {category} Sentiment Tweets")
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)