import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import plotly.graph_objects as go

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

def convert_duration_ms(duration_ms):
    minutes = duration_ms // 60000
    seconds = (duration_ms % 60000) // 1000
    return f"{minutes}m {seconds:02d}s"

def convert_key(key):
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return keys[key] if 0 <= key < len(keys) else "Unknown"

def convert_mode(mode):
    return "Major" if mode == 1 else "Minor"

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
                st.write(f"**Duration:** {convert_duration_ms(features['duration_ms'])}")
                st.write(f"**Key:** {convert_key(features['key'])}")
                st.write(f"**Mode:** {convert_mode(features['mode'])}")
                st.image(album_art, use_column_width=True)

            # Column 2: Audio Features Overview and Radar Chart
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
                        'speechiness': "Detects the presence of spoken words. Higher values indicate more spoken words.",
                        'acousticness': "Measures the amount of acoustic sound in the track.",
                        'instrumentalness': "Predicts the likelihood of the track being instrumental.",
                        'liveness': "Detects the presence of an audience in the recording. Higher values indicate a more live performance.",
                        'valence': "Describes the musical positiveness conveyed by the track. Higher values indicate a more positive mood.",
                    }

                    # Display each feature with its description
                    for feature, description in descriptions.items():
                        st.subheader(feature.capitalize())
                        st.write(f"**{feature.capitalize()}:** {features[feature]:.2f}")
                        st.write(description)

                # Include only the specified features for the radar chart
                radar_features = {feature: features[feature] for feature in ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']}
                
                # Radar chart configuration
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=list(radar_features.values()),
                    theta=list(radar_features.keys()),
                    fill='toself',
                    name='Audio Features'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 1]
                        )
                    ),
                    showlegend=True
                )
                
                st.plotly_chart(fig)
                
        else:
            st.write("No tracks found for the given title and artist.")
            search_made = False
    except Exception as e:
        st.write(f"An error occurred: {e}")
        search_made = False

# Display the prompt only if no search has been made
if not search_made:
    st.write("Enter the song title and artist to analyze its audio features.")
