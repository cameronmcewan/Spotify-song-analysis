import streamlit as st
from header import render_header
from sidebar import render_sidebar
from functions.spotify_setup import get_authenticated_spotify_client

st.set_page_config(page_title="Streamlit App", layout="wide")

# Spotify authentication loaded from spotify_setup.py
sp = get_authenticated_spotify_client()

# render_header()
render_sidebar()


# =============================================================================
# Page Content
# =============================================================================

st.header("Songify", divider=True)
st.write("hi")

song_title = st.text_input("Enter a song")

# if st.text_input("Enter a song name:"):
#     query = f"track:{song_title} artist:{artist_name}"
#     results = sp.search(q=query, type='track', limit=1)