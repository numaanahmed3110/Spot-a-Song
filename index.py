import os
import re
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# Spotify Authentication
sp = Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="playlist-modify-private",
    )
)


# Helper Functions
def clean_title(title):
    """Clean and simplify the file name."""
    title = re.sub(r"\(.*?\)|\[.*?\]", "", title)  # Remove text in brackets/parentheses
    title = re.sub(r"[-_]", " ", title)  # Replace hyphens/underscores with spaces
    title = re.sub(r"\s+", " ", title).strip()  # Remove extra spaces
    return title


def search_song_on_spotify(sp, title):
    """Search for a song on Spotify."""
    try:
        result = sp.search(q=title, type="track", limit=1)
        if result["tracks"]["items"]:
            track = result["tracks"]["items"][0]
            print(
                f"Found: {track['name']} by {', '.join([a['name'] for a in track['artists']])}"
            )
            return track["uri"]
        else:
            print(f"Song not found: {title}")
            return None
    except Exception as e:
        print(f"Error searching Spotify: {e}")
        return None


def create_playlist(sp, user_id, playlist_name):
    """Create a new Spotify playlist."""
    try:
        playlist = sp.user_playlist_create(
            user=user_id, name=playlist_name, public=False
        )
        print(f"Created playlist: {playlist_name}")
        return playlist["id"]
    except Exception as e:
        print(f"Error creating playlist: {e}")
        return None


def write_songs_not_found(filename, songs):
    """Write missing songs to a file."""
    counter = 0
    while os.path.exists(filename):
        counter += 1
        filename = f"SongsNotFound_{counter}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(songs))
    print(f"Missing songs written to {filename}")


def find_audio_files(directory):
    """Recursively find all audio files in a directory."""
    audio_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(
                (".mp3", ".wav", ".flac")
            ):  # Add more extensions if needed
                audio_files.append(os.path.join(root, file))
    return audio_files


# Main Function
def main():
    music_folder = input("Enter the path to your music folder: ").strip()
    playlist_name = input("Enter the name for the new Spotify playlist: ").strip()

    # Get Spotify user ID
    user_id = sp.me()["id"]

    # Create playlist
    playlist_id = create_playlist(sp, user_id, playlist_name)
    if not playlist_id:
        print("Failed to create playlist. Exiting...")
        return

    # Traverse folder and find songs
    audio_files = find_audio_files(music_folder)
    print(f"Found {len(audio_files)} audio files.")

    songs_not_found = []
    track_uris = []

    for file in audio_files:
        song_title = clean_title(os.path.splitext(os.path.basename(file))[0])
        track_uri = search_song_on_spotify(sp, song_title)
        if track_uri:
            track_uris.append(track_uri)
        else:
            songs_not_found.append(song_title)

    # Add found songs to the playlist
    if track_uris:
        sp.user_playlist_add_tracks(
            user=user_id, playlist_id=playlist_id, tracks=track_uris
        )
        print(f"Added {len(track_uris)} songs to playlist '{playlist_name}'.")
    else:
        print("No songs were added to the playlist.")

    # Handle missing songs
    if songs_not_found:
        write_songs_not_found("SongsNotFound.txt", songs_not_found)


if __name__ == "__main__":
    main()
