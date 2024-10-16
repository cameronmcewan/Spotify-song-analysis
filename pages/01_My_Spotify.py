import streamlit as st
from functions.spotify_setup import get_authenticated_spotify_client
from sidebar import render_sidebar

st.set_page_config(page_title="My Spotify App", layout="wide")

# Spotify authentication loaded from spotify_setup.py
sp = get_authenticated_spotify_client()

results = render_sidebar()

# =============================================================================
# Page Content
# =============================================================================

st.header("My Spotify", divider=True)

if results:
    track = results['tracks']['items'][0]
    track_name = track['name']
    artist = track['artists'][0]['name']
    track_uri = track['uri']
    album_art = track['album']['images'][0]['url']

    st.header(track_name)
    st.audio(track["preview_url"], format="audio/mp3")
    st.write(artist)
    st.write(track_uri)
    
    # Get track audio features
    audio_features = sp.audio_features(track_uri)
    features = audio_features[0]
    st.write(results)
else:
    st.write("No tracks found for the given title.")