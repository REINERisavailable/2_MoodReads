import streamlit as st
import pandas as pd
import plotly.express as px
import re

def clean_rating(rating):
    match = re.search(r'(\d+\.\d+)', rating)
    return float(match.group(1)) if match else None

def dashboard_page():
    books_df = pd.read_csv('books.csv')
    books_df.columns = books_df.columns.str.strip()
    books_df['average_rating'] = pd.to_numeric(books_df['average_rating'], errors='coerce')
    books_df['publication_date'] = pd.to_datetime(books_df['publication_date'], errors='coerce')
    books_df['publication_year'] = books_df['publication_date'].dt.year
    books_df = books_df[(books_df['publication_year'] >= 1996) & (books_df['publication_year'] <= 2006)]

    st.title("Book Analysis Dashboard")
    
    # Metrics
    a1, a2, a3 = st.columns(3)
    with a1:
        total_authors = books_df['authors'].nunique()
        st.metric("Total Authors", total_authors)
    with a2:
        total_unique_books = books_df['title'].nunique()
        st.metric("Total Unique Books", total_unique_books)
    with a3:
        average_rating = books_df['average_rating'].mean()
        st.metric("Average Rating", f"{average_rating:.2f}")
    
    # Charts
    b1, b2 = st.columns(2)
    with b1:
        authors_by_total_books = books_df['authors'].value_counts().nlargest(20).reset_index()
        authors_by_total_books.columns = ['authors', 'total_books']
        authors_chart = px.bar(authors_by_total_books.sort_values('total_books', ascending=False), 
                               x='authors', y='total_books', title='Top 20 Authors by Total Books')
        st.plotly_chart(authors_chart, use_container_width=True)
    with b2:
        publishers_by_total_books = books_df['publisher'].value_counts().nlargest(20).reset_index()
        publishers_by_total_books.columns = ['publisher', 'total_books']
        publishers_chart = px.bar(publishers_by_total_books.sort_values('total_books', ascending=False), 
                                  x='publisher', y='total_books', title='Top 20 Publishers by Total Books')
        st.plotly_chart(publishers_chart, use_container_width=True)
    
    c1, c2 = st.columns(2)
    with c1:
        books_per_year = books_df['publication_year'].value_counts().sort_index().reset_index()
        books_per_year.columns = ['publication_year', 'count']
        books_by_publication_date = px.line(books_per_year, x='publication_year', y='count', title='Books by Publication Year')
        st.plotly_chart(books_by_publication_date, use_container_width=True)
    with c2:
        books_by_language = books_df['language_code'].value_counts().reset_index()
        books_by_language.columns = ['language_code', 'count']
        language_pie_chart = px.pie(books_by_language, names='language_code', values='count', title='Books by Language Code')
        language_pie_chart.update_traces(textinfo='none')
        st.plotly_chart(language_pie_chart, use_container_width=True)
    
    d1, d2 = st.columns(2)
    with d1:
        pages_vs_rating = px.scatter(books_df, x='num_pages', y='average_rating', title='Number of Pages vs. Rating')
        st.plotly_chart(pages_vs_rating, use_container_width=True)
    with d2:
        ratings_histogram = px.histogram(books_df, x='average_rating', title='Distribution of Book Ratings')
        st.plotly_chart(ratings_histogram, use_container_width=True)
    
    