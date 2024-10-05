import streamlit as st
from streamlit_option_menu import option_menu
from mood_recommender import mood_recommender
from dashboard_page import dashboard_page
from algorithms_page import Algorithms_page
import pandas as pd

books_df = pd.read_csv('books.csv')

def main_page():
    # Add the custom style for mood buttons and MoodReads button
    st.markdown("""
        <style>
        .stButton>button {
            width: 230px;
            height: 50px;
            margin: 1px;
            border-radius: 5px;
        }
        .big-button {
            width: 100%;
            height: 60px;
            margin: 0;
            padding: 10px;
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Add the MoodReads button
    st.markdown('<button class="big-button">📚 MoodReads</button>', unsafe_allow_html=True)
    
    mood_recommender()

def feedback_page():
    st.title("Feedback and Quotes")
    
    user_quote = st.text_area("Enter your quote here")
    if st.button("Submit"):
        st.write("Thank you for your submission!")
    
    st.write("### Recently Submitted Quotes")
    st.write("No quotes submitted yet.")

# Function to display rating stars
def display_rating(rating):
    full_stars = int(rating)
    half_star = rating - full_stars >= 0.5
    empty_stars = 5 - full_stars - (1 if half_star else 0)
    
    stars = "⭐" * full_stars
    if half_star:
        stars += "½"
    stars += "☆" * empty_stars
    
    return f"Rating: {stars} {rating}/5"

selected = option_menu(
    menu_title=None,
    options=["Main Page", "Dashboard", "Algorithms", "Feedback"],
    icons=["house", "bar-chart", "book", "chat"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected == "Main Page":
    main_page()
elif selected == "Dashboard":
    dashboard_page()
elif selected == "Algorithms":
    Algorithms_page()
elif selected == "Feedback":
    feedback_page()

footer_html = """
<div class="footer" style="position: fixed; left: 0; bottom: 0; width: 100%; background-color: #f1f1f1; text-align: center; padding: 10px;">
    <a href="https://example.com/docs" target="_blank" style="margin: 0 10px; color: #333; text-decoration: none;">Documentation</a>
    <a href="https://example.com/feedback" target="_blank" style="margin: 0 10px; color: #333; text-decoration: none;">Feedback</a>
    <a href="https://www.linkedin.com/in/yourprofile" target="_blank" style="margin: 0 10px; color: #333; text-decoration: none;">LinkedIn</a>
    <a href="mailto:mhmdjmri@gmail.com" style="margin: 0 10px; color: #333; text-decoration: none;">Email</a>
    <span style="margin: 0 10px; color: #333;">Hire me!</span>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)

hide_st_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
