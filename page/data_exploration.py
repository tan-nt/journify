import streamlit as st
from database.article import article
import pandas as pd
import plotly.express as px

# Display data exploration in tab3
def display_data_exploration():
    data = article.read_articles()  # Load data into a DataFrame
    df = pd.DataFrame(data)

    st.header("Data Exploration and Analytics")
    st.info(f"We use {len(data)} article records")

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