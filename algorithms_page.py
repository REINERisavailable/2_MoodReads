import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

books_df = pd.read_csv('books.csv')

tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(books_df['authors'].fillna(''))

def get_content_based_recommendations(selected_book):
    tfidf_index = books_df[books_df['title'] == selected_book].index[0]
    
    cosine_similarities = linear_kernel(tfidf_matrix[tfidf_index], tfidf_matrix).flatten()
    
    content_indices = cosine_similarities.argsort()[::-1][1:]
    
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
    st.title("Recommendation Algorithms")
    
    st.markdown("""
    <style>
    .stButton>button {
        width: 330px;
        height: 50px;
        margin: 1px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.write("Explore our recommendation algorithms on Google Colab:")
    
    button_container = st.container()
    
    col1, col2 = button_container.columns(2)
    
    algorithms = {
        "Collaborative Filtering (CF)": "https://colab.research.google.com/drive/your_cf_link",
        "Content-Based Filtering (CB)": "https://colab.research.google.com/drive/your_cb_link",
        "Neural Collaborative Filtering (NCF)": "https://colab.research.google.com/drive/your_ncf_link",
        "Generative Adversarial Network (GAN)": "https://colab.research.google.com/drive/your_gan_link"
    }
    
    for i, (name, link) in enumerate(algorithms.items()):
        if i % 2 == 0:
            with col1:
                if st.button(name, key=f"btn_{i}"):
                    st.markdown(f'<a href="{link}" target="_blank">Open in Colab</a>', unsafe_allow_html=True)
        else:
            with col2:
                if st.button(name, key=f"btn_{i}"):
                    st.markdown(f'<a href="{link}" target="_blank">Open in Colab</a>', unsafe_allow_html=True)
    
    st.write("### Content-Based Algorithm Showcase")
    book_titles = [""] + books_df['title'].tolist()
    selected_book = st.selectbox("Select a book:", book_titles)
    
    if selected_book:
        st.write(f"Recommendations for '{selected_book}':")
        
        
        content_recommendations = get_content_based_recommendations(selected_book)
        
        for rec in content_recommendations:
            st.write(f"Title: {rec['title']}")
            st.write(f"Authors: {rec['authors']}")
            st.write(f"Average Rating: {rec['average_rating']}")
            st.write(f"Ratings Count: {rec['ratings_count']}")
            st.write(f"Similarity Score: {rec['similarity_score']:.2f}")
            st.write("---")
