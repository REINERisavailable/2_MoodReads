import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

def clean_rating(rating):
    match = re.search(r'(\d+\.\d+)', rating)
    return float(match.group(1)) if match else None

def dashboard_page():
    st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
    }
    .css-1d391kg {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .st-emotion-cache-1wivap2 {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1 {
        color: #1e3a8a;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

    books_df = pd.read_csv('books.csv')
    books_df.columns = books_df.columns.str.strip()
    books_df['average_rating'] = pd.to_numeric(books_df['average_rating'], errors='coerce')
    books_df['publication_date'] = pd.to_datetime(books_df['publication_date'], errors='coerce')
    books_df['publication_year'] = books_df['publication_date'].dt.year
    books_df = books_df[(books_df['publication_year'] >= 1996) & (books_df['publication_year'] <= 2006)]

    st.title("📚 Book Analysis Dashboard")
    
    st.markdown("<div class='metrics-container'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        total_authors = books_df['authors'].nunique()
        st.metric("Total Authors", f"{total_authors:,}")
    with col2:
        total_unique_books = books_df['title'].nunique()
        st.metric("Total Unique Books", f"{total_unique_books:,}")
    with col3:
        average_rating = books_df['average_rating'].mean()
        st.metric("Average Rating", f"{average_rating:.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Charts
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📊 Author & Publisher Analysis", "📈 Book Trends"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            authors_by_total_books = books_df['authors'].value_counts().nlargest(20).reset_index()
            authors_by_total_books.columns = ['authors', 'total_books']
            authors_chart = px.bar(authors_by_total_books.sort_values('total_books', ascending=True), 
                                   y='authors', x='total_books', 
                                   title='Top 20 Most Prolific Authors',
                                   labels={'authors': 'Author', 'total_books': 'Number of Books'},
                                   orientation='h')
            authors_chart.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
            authors_chart.update_layout(transition_duration=500)
            st.plotly_chart(authors_chart, use_container_width=True)

        with col2:
            publishers_by_total_books = books_df['publisher'].value_counts().nlargest(20).reset_index()
            publishers_by_total_books.columns = ['publisher', 'total_books']
            publishers_chart = px.bar(publishers_by_total_books.sort_values('total_books', ascending=True), 
                                      y='publisher', x='total_books', 
                                      title='Top 20 Publishing Houses',
                                      labels={'publisher': 'Publisher', 'total_books': 'Number of Books'},
                                      orientation='h')
            publishers_chart.update_traces(marker_color='rgb(255,158,158)', marker_line_color='rgb(107,8,8)', marker_line_width=1.5, opacity=0.6)
            publishers_chart.update_layout(transition_duration=500)
            st.plotly_chart(publishers_chart, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            books_per_year = books_df['publication_year'].value_counts().sort_index().reset_index()
            books_per_year.columns = ['publication_year', 'count']
            books_by_publication_date = px.line(books_per_year, x='publication_year', y='count', 
                                                title='Book Publication Trends',
                                                labels={'publication_year': 'Year', 'count': 'Number of Books Published'})
            books_by_publication_date.update_traces(line_color='rgb(0,128,128)', line_width=3)
            books_by_publication_date.update_layout(transition_duration=500)
            st.plotly_chart(books_by_publication_date, use_container_width=True)

        with col2:
            books_by_language = books_df['language_code'].value_counts().reset_index()
            books_by_language.columns = ['language_code', 'count']
            language_pie_chart = px.pie(books_by_language, names='language_code', values='count', title='Books by Language Code')
            language_pie_chart.update_traces(textposition='inside', textinfo='percent+label')
            language_pie_chart.update_layout(transition_duration=500)
            st.plotly_chart(language_pie_chart, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        pages_vs_rating = px.scatter(books_df, x='num_pages', y='average_rating', 
                                     title='Book Length vs. Rating Correlation',
                                     labels={'num_pages': 'Number of Pages', 'average_rating': 'Average Rating'},
                                     color='average_rating',
                                     color_continuous_scale=px.colors.sequential.Viridis)
        pages_vs_rating.update_traces(marker=dict(size=8, opacity=0.6), selector=dict(mode='markers'))
        pages_vs_rating.update_layout(transition_duration=500)
        st.plotly_chart(pages_vs_rating, use_container_width=True)

    with col2:
        ratings_histogram = px.histogram(books_df, x='average_rating', 
                                         title='Distribution of Book Ratings',
                                         labels={'average_rating': 'Average Rating', 'count': 'Number of Books'},
                                         color_discrete_sequence=['rgb(102,197,204)'])
        ratings_histogram.update_traces(opacity=0.75)
        ratings_histogram.update_layout(transition_duration=500)
        st.plotly_chart(ratings_histogram, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## 📊 Interactive Data Explorer")
    selected_columns = st.multiselect("Select columns to display", books_df.columns.tolist(), default=["title", "authors", "average_rating"])
    st.dataframe(books_df[selected_columns].head(50), use_container_width=True)