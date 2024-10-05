import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from groq import Groq

client = Groq(api_key="")

def get_book_recommendations(mood):
    prompt = f"""Recommend three books for someone feeling {mood}. For each book, provide the following information in a Python dictionary format:
    - title: The book's title
    - author: The book's author
    - rating: A float between 1 and 5
    - genres: A list of 2-3 genres
    - description: A brief description (20-30 words)
    - image_url: A valid URL for the book's cover image (use real book cover URL)

    Return the result as a Python list containing three dictionaries, one for each book recommendation."""
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="mixtral-8x7b-32768",
            max_tokens=800,
        )
        
        
        books = eval(chat_completion.choices[0].message.content.strip())
        return books
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return [
            {
                "title": "The Happiness Project",
                "author": "Gretchen Rubin",
                "rating": 4.5,
                "genres": ["Self-help", "Personal Development"],
                "description": "Gretchen Rubin's year-long experiment to discover how to create true happiness.",
                "image_url": "https://www.libertybooks.com/image/cache/catalog/87419-313x487.jpg?q6"
            },
            {
                "title": "The Alchemist",
                "author": "Paulo Coelho",
                "rating": 4.8,
                "genres": ["Fiction", "Philosophy"],
                "description": "A mystical story about following your dreams and finding your destiny.",
                "image_url": "https://images-na.ssl-images-amazon.com/images/I/51kcX5PpaZL._SX329_BO1,204,203,200_.jpg"
            },
            {
                "title": "Thinking, Fast and Slow",
                "author": "Daniel Kahneman",
                "rating": 4.6,
                "genres": ["Psychology", "Non-fiction"],
                "description": "An exploration of the two systems that drive the way we think and make choices.",
                "image_url": "https://images-na.ssl-images-amazon.com/images/I/41shZGS-G%2BL._SX331_BO1,204,203,200_.jpg"
            }
        ]

def display_book(book):
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            response = requests.get(book['image_url'])
            img = Image.open(BytesIO(response.content))
            st.image(img, use_column_width=True)
        except:
            st.write("Image not available")
    
    with col2:
        st.markdown(f"## {book['title']}")
        st.write(f"By {book['author']}")
        st.write(f"Rating: {'⭐' * int(book['rating'])}")
        st.markdown(" ".join([f"<span class='badge'>{genre}</span>" for genre in book['genres']]), unsafe_allow_html=True)
        st.write(book['description'])

def mood_recommender():
    st.markdown("""
    <style>
    .big-button {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        font-size: 24px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
    }
    .badge {
        background-color: #f1f1f1;
        color: black;
        padding: 4px 8px;
        text-align: center;
        border-radius: 5px;
        display: inline-block;
        margin: 2px;
    }
    </style>
    """, unsafe_allow_html=True)


    cont1 = st.container()
    cont2 = st.container()

    with cont1:
        st.markdown("**Find Books Based on Your Mood**")
        st.write("How are you feeling?")
        
        moods = ["Happy 😊", "Sad 😢", "Excited 🎉", "Anxious 😰", "Relaxed 😌", "Angry 😠",
                 "Bored 😑", "Curious 🤔", "Inspired 💡", "Nostalgic 🕰️", "Romantic ❤️", "Adventurous 🌄",
                 "Confused 😕", "Determined 💪", "Grateful 🙏", "Hopeful 🌟", "Lonely 😔", "Peaceful ☮️"]
        
        cols = st.columns(3)
        selected_mood = None
        for i, mood in enumerate(moods):
            if cols[i % 3].button(mood):
                selected_mood = mood.split()[0].lower()
                cont1.empty()
                break

    if selected_mood:
        with cont2:
            st.write(f"Books to Read When You Feel {selected_mood.capitalize()}...")
            with st.spinner("Fetching book recommendations..."):
                books = get_book_recommendations(selected_mood)
            for book in books:
                display_book(book)
                st.markdown("---")
if __name__ == "__main__":
    mood_recommender()