import streamlit as st
from functions.spotify_setup import get_authenticated_spotify_client

# Spotify authentication loaded from spotify_setup.py
sp = get_authenticated_spotify_client()

def render_sidebar():
    st.sidebar.header("Sidebar")
    artist_name = st.sidebar.text_input("Enter an artist")
    song_title = st.sidebar.text_input("Enter a song")

    results = None # Initialize results to None
    if song_title and not artist_name:
        query = f"track:{song_title}"
        results = sp.search(q=query, type='track', limit=1)

    if artist_name and not song_title:
        query = f"artist:{artist_name}"
        results = sp.search(q=query, type='artist', limit=1)

    if song_title and artist_name:
        query = f"track:{song_title} artist:{artist_name}"
        results = sp.search(q=query, type='track', limit=1)

    return results  
