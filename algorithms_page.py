import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load the dataset
books_df = pd.read_csv('books.csv')

# Create TF-IDF matrix
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(books_df['authors'].fillna(''))

def get_content_based_recommendations(selected_book):
    # Get the index of the selected book
    tfidf_index = books_df[books_df['title'] == selected_book].index[0]
    
    # Compute cosine similarities
    cosine_similarities = linear_kernel(tfidf_matrix[tfidf_index], tfidf_matrix).flatten()
    
    # Get indices of books sorted by similarity score
    content_indices = cosine_similarities.argsort()[::-1][1:]
    
    # Get top 5 recommendations
    recommendations = [
        {
            "title": books_df.iloc[idx]['title'],
            "authors": books_df.iloc[idx]['authors'],
            "average_rating": books_df.iloc[idx]['average_rating'],
            "ratings_count": books_df.iloc[idx]['ratings_count'],
            "similarity_score": cosine_similarities[idx]
        }
        for idx in content_indices[:5]
    ]
    
    return recommendations

def Algorithms_page():
    st.title("Recommendations Algorithms")
    
    st.write("Here are the links to the algorithms on Google Colab:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("[Collaborative Filtering (CB)](https://colab.research.google.com/drive/your_cb_link)", unsafe_allow_html=True)
        st.markdown("[Content-Based Filtering (CF)](https://colab.research.google.com/drive/your_cf_link)", unsafe_allow_html=True)
    with col2:
        st.markdown("[Neural Collaborative Filtering (NCF)](https://colab.research.google.com/drive/your_ncf_link)", unsafe_allow_html=True)
        st.markdown("[Generative Adversarial Network (GAN)](https://colab.research.google.com/drive/your_gan_link)", unsafe_allow_html=True)
    st.write("### Content-Based Algorithm Showcase")
    # Select box for book title with default blank option
    book_titles = [""] + books_df['title'].tolist()
    selected_book = st.selectbox("Select a book:", book_titles)
    
    if selected_book:
        # Display recommendations and similarity scores
        st.write(f"Recommendations for '{selected_book}':")
        
        # Content-based recommendations
        
        content_recommendations = get_content_based_recommendations(selected_book)
        
        for rec in content_recommendations:
            st.write(f"Title: {rec['title']}")
            st.write(f"Authors: {rec['authors']}")
            st.write(f"Average Rating: {rec['average_rating']}")
            st.write(f"Ratings Count: {rec['ratings_count']}")
            st.write(f"Similarity Score: {rec['similarity_score']:.2f}")
            st.write("---")
