# Spot-a-Song

**Spot-a-Song** is a Python-based application that allows users to automatically create a Spotify playlist by scanning a local folder for audio files, extracting metadata, and searching for the songs on Spotify. If the song is found on Spotify, it is added to the playlist; otherwise, the song details are saved in a file for later review.

## Features:

- Scan a folder (including subfolders) for supported audio files.
- Extract song metadata (title and artist) from the audio files using TinyTag.
- Search for songs on Spotify by both title and artist. If not found, attempt to search by title alone.
- Create a new Spotify playlist and add matching songs to it.
- Log unmatched songs into a `SongsNotFound.txt` file.
- Graceful error handling to ensure the program continues to function correctly even if something goes wrong.

## Requirements:

- Python 3.6 or higher
- Spotify Developer Account for API credentials
- `.env` file to store your Spotify credentials

### Libraries used:

- **Spotipy**: Python library for Spotify Web API integration.
- **TinyTag**: A lightweight library to read metadata from audio files.
- **Dotenv**: Loads environment variables from a `.env` file.

---

## Installation

1. **Clone the repository:**

   - First, clone the project repository to your local machine.

     ```bash
     git clone [https://github.com/yourusername/Spot-a-Song.git](https://github.com/yourusername/Spot-a-Song.git)
     cd Spot-a-Song
     ```

2. **Set up a Spotify Developer Application:**

   - You will need to create a Spotify Developer Application to get the credentials (Client ID, Client Secret, and Redirect URI).

     - Visit the Spotify Developer Dashboard.
     - Create a new application and note down the Client ID, Client Secret, and set the Redirect URI (e.g., `http://localhost:8888/callback`).

3. **Create a `.env` file:**

   - Create a `.env` file in the root directory of the project with the following variables:

     ```
     SPOTIPY_CLIENT_ID=your_spotify_client_id
     SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
     SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
     ```

4. **Install dependencies:**

   - Install the required libraries using pip:

     ```bash
     pip install -r requirements.txt
     ```

   - Alternatively, you can manually install each required package:

     ```bash
     pip install spotipy tinytag python-dotenv
     ```

## Usage

1. **Run the application:**

   - After completing the setup, run the script:

     ```bash
     python spot_a_song.py
     ```

2. **Input Folder Path and Playlist Name:**

   - When prompted, enter the folder path where your audio files are stored (e.g., `D:\music\`). The application will scan this folder (and its subfolders) for supported audio files and attempt to match them with Spotify.

   - You will also be asked for a name for the new playlist that will be created on your Spotify account.

3. **Check the Output:**

   - The program will create a new playlist on Spotify and add matched songs.
   - If any songs are not found on Spotify, their details (title and artist) will be saved to a file called `SongsNotFound.txt` in the project folder.

4. **Error Handling:**

   - The script gracefully handles errors like missing metadata, API issues, and invalid folder paths.
   - If the script is interrupted (e.g., using Ctrl+C), it will exit cleanly.
   - If a song is not found, it will try searching by title alone after attempting with both title and artist.

## Folder Structure:

`Spot-a-Song/
├── spot_a_song.py      # Main Python script
├── .env                # Spotify credentials (do not share this file)
├── requirements.txt    # List of dependencies
├── SongsNotFound.txt  # Log of unmatched songs
├── README.md           # Project documentation`

## Supported Audio Formats:

- `.mp3`
- `.wav`
- `.flac`
- `.m4a`
- `.aac`
- `.ogg`
- `.m3u`

  - You can add more formats as per your requirements in the `index.py` code.

## Notes:

- The application uses the Spotify Web API to search for songs and modify playlists. Make sure to not exceed the API rate limits.
- The script is designed to work with local audio files that have proper metadata (title and artist). If metadata is missing or incomplete, it falls back on the file name.
- The `SongsNotFound.txt` file will contain the details of songs that could not be found on Spotify. This file can be used to manually review the songs and ensure that the correct metadata is available for future runs.