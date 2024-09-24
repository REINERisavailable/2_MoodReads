import streamlit as st
from streamlit_option_menu import option_menu
from mood_recommender import mood_recommender
from dashboard_page import dashboard_page  # Import the dashboard_page function
from algorithms_page import Algorithms_page  # Import the Algorithms_page function
import pandas as pd

# Load the dataset
books_df = pd.read_csv('books.csv')

# ... existing code ...

def main_page():
    mood_recommender()

def feedback_page():
    st.title("Feedback and Quotes")
    
    user_quote = st.text_area("Enter your quote here")
    if st.button("Submit"):
        st.write("Thank you for your submission!")
    
    st.write("### Recently Submitted Quotes")
    st.write("No quotes submitted yet.")

# Navigation menu
selected = option_menu(
    menu_title=None,
    options=["Main Page", "Dashboard", "Algorithms", "Feedback"],
    icons=["house", "bar-chart", "book", "chat"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Display the selected page
if selected == "Main Page":
    main_page()
elif selected == "Dashboard":
    dashboard_page()
elif selected == "Algorithms":
    Algorithms_page()
elif selected == "Feedback":
    feedback_page()

# Footer
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

# Hide Streamlit style
hide_st_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
