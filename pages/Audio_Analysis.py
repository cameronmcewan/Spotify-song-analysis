import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import plotly.graph_objects as go
from functions.functions import convert_duration_ms, convert_key, convert_mode
from functions.spotify_setup import get_authenticated_spotify_client
from sidebar import render_sidebar


# Spotify authentication loaded from spotify_setup.py
sp = get_authenticated_spotify_client()

results = render_sidebar()

# Title for page
st.title("Spotify Audio Analysis")

# Input for song title and artist
song_title = st.text_input("Song Title")
artist_name = st.text_input("Artist Name")

# Track if a search has been made
search_made = False

if results:
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
