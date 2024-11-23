import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tinytag import TinyTag
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Set up Spotify authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-public playlist-modify-private user-library-read",
    )
)


# Function to extract song metadata using TinyTag
def get_song_metadata(file_path):
    try:
        tag = TinyTag.get(file_path)
        song_title = tag.title
        artist = tag.artist
        return song_title, artist
    except Exception as e:
        print(f"Error reading metadata for {file_path}: {e}")
        return None, None


# Function to search for a song on Spotify
def search_song_on_spotify(title, artist):
    query = f"track:{title} artist:{artist}"
    result = sp.search(q=query, type="track", limit=1)
    if result["tracks"]["items"]:
        return result["tracks"]["items"][0]["uri"]
    else:
        return None


# Function to create a new playlist
def create_playlist(user_id, playlist_name):
    playlist = sp.user_playlist_create(user_id, playlist_name)
    return playlist["id"]


# Function to add songs to a playlist
def add_songs_to_playlist(playlist_id, song_uris):
    sp.playlist_add_items(playlist_id, song_uris)


# Main function to scan the folder and add songs to the Spotify playlist
def main():
    # Ask user for folder path and playlist name
    folder_path = input("Enter the folder path (e.g., D:\\music\\): ")
    playlist_name = input("Enter the name of the new playlist: ")

    # Validate folder path
    if not os.path.isdir(folder_path):
        print(f"The folder path '{folder_path}' is invalid.")
        return

    # Get current user's Spotify ID
    user_id = sp.current_user()["id"]

    # Create new playlist on Spotify
    playlist_id = create_playlist(user_id, playlist_name)
    print(f"Playlist '{playlist_name}' created successfully!")

    unmatched_songs = []  # List to store unmatched song names

    # Traverse through the folder and its subfolders
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(
                (
                    ".mp3",
                    ".wav",
                    ".flac",
                    ".m4a",
                    ".aac",
                    ".ogg",
                    ".m4a",
                    ".m3u",
                    ".m4a",
                )
            ):  # Supported audio formats
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}...")

                # Extract metadata (title, artist)
                title, artist = get_song_metadata(file_path)
                if title and artist:
                    # Search for the song on Spotify
                    song_uri = search_song_on_spotify(title, artist)
                    if song_uri:
                        print(f"Found '{title}' by {artist}, adding to playlist...")
                        add_songs_to_playlist(playlist_id, [song_uri])
                    else:
                        print(f"Song '{title}' by {artist} not found on Spotify.")
                        unmatched_songs.append(f"{title} - {artist}")

    # Write unmatched songs to a file
    if unmatched_songs:
        unmatched_file = os.path.join(folder_path, "unmatched_songs.txt")
        with open(unmatched_file, "w") as f:
            f.write("\n".join(unmatched_songs))
        print(f"\nUnmatched songs saved to {unmatched_file}.")
    else:
        print("\nAll songs were successfully added to the playlist.")


if __name__ == "__main__":
    main()
