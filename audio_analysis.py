import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials from environment variables
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# Scope required to access audio features
scope = "user-library-read"

# Set up Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

st.title("Spotify Audio Analysis")

# Input for song title and artist
song_title = st.text_input("Enter Song Title")
artist_name = st.text_input("Enter Artist Name")

if song_title and artist_name:
    try:
        # Search for the track
        query = f"track:{song_title} artist:{artist_name}"
        results = sp.search(q=query, type='track', limit=1)

        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_name = track['name']
            artist = track['artists'][0]['name']
            track_uri = track['uri']
            album_art = track['album']['images'][0]['url']
            
            # Get track audio features
            audio_features = sp.audio_features(track_uri)
            features = audio_features[0]

            # Display track information and audio features
            st.subheader(f"Track: {track_name}")
            st.write(f"**Artist:** {artist}")
            st.image(album_art, use_column_width=True)
            st.subheader("Audio Features Overview")
            st.write(f"**Danceability:** {features['danceability']:.2f}")
            st.write(f"**Energy:** {features['energy']:.2f}")
            st.write(f"**Key:** {features['key']}")
            st.write(f"**Loudness:** {features['loudness']:.2f} dB")
            st.write(f"**Mode:** {features['mode']}")
            st.write(f"**Speechiness:** {features['speechiness']:.2f}")
            st.write(f"**Acousticness:** {features['acousticness']:.2f}")
            st.write(f"**Instrumentalness:** {features['instrumentalness']:.2f}")
            st.write(f"**Liveness:** {features['liveness']:.2f}")
            st.write(f"**Valence:** {features['valence']:.2f}")
            st.write(f"**Tempo:** {features['tempo']:.2f} BPM")
            st.write(f"**Duration:** {features['duration_ms'] / 1000:.2f} seconds")
        else:
            st.write("No tracks found for the given title and artist.")
    except Exception as e:
        st.write(f"An error occurred: {e}")

st.write("Enter the song title and artist to analyze its audio features.")
