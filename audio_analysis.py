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

# Track if a search has been made
search_made = False

if song_title and artist_name:
    search_made = True
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

            # Create two columns
            col1, col2 = st.columns(2)

            # Column 1: Track Info
            with col1:
                st.subheader(f"Track: {track_name}")
                st.write(f"**Artist:** {artist}")
                st.image(album_art, use_column_width=True)

            # Column 2: Audio Features Overview
            with col2:
                st.subheader("Audio Features Overview")
                st.write("Select an audio feature from the sidebar to view more details.")

            # Sidebar for detailed information
            with st.sidebar:
                st.header("Audio Features Descriptions")

                # Define descriptions for each audio feature
                descriptions = {
                    'danceability': "Danceability describes how suitable a track is for dancing based on tempo, rhythm stability, and beat strength.",
                    'energy': "Energy is a measure of intensity and activity, determined by dynamics, timbre, and other aspects.",
                    'key': "The musical key of the track, with values from 0 (C) to 11 (B).",
                    'loudness': "Overall loudness of the track in decibels (dB).",
                    'mode': "Modality of the track. Major is 1, minor is 0.",
                    'speechiness': "Detects the presence of spoken words. Higher values indicate more spoken words.",
                    'acousticness': "Measures the amount of acoustic sound in the track.",
                    'instrumentalness': "Predicts the likelihood of the track being instrumental.",
                    'liveness': "Detects the presence of an audience in the recording. Higher values indicate a more live performance.",
                    'valence': "Describes the musical positiveness conveyed by the track. Higher values indicate a more positive mood.",
                    'tempo': "Speed of the track measured in beats per minute (BPM).",
                    'duration_ms': "Length of the track in milliseconds."
                }

                # Display each feature with its description
                for feature, description in descriptions.items():
                    st.subheader(feature.capitalize())
                    st.write(f"**{feature.capitalize()}:** {features[feature]:.2f}")
                    st.write(description)
                
        else:
            st.write("No tracks found for the given title and artist.")
            search_made = False
    except Exception as e:
        st.write(f"An error occurred: {e}")
        search_made = False

# Display the prompt only if no search has been made
if not search_made:
    st.write("Enter the song title and artist to analyze its audio features.")
