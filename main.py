# Importing necessary libraries
import tkinter as tk
from tkinter import filedialog
import os
import requests
from pytube import YouTube

# Function to fetch the YouTube video details using the YouTube Data API
def get_youtube_video_details(video_id):
    api_key = 'AIzaSyAsHCT-ARhtxiKG70gIV1nVC_Rch2hgMbI'  # Replace with your YouTube Data API key
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet'
    response = requests.get(url)
    data = response.json()
    return data['items'][0]['snippet']['title']

# Function to replace invalid characters in the filename with underscores
def clean_filename(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

# Function to download audio from a YouTube URL as an MP3 file
def download_audio_from_youtube():
    try:
        url = url_entry.get()  # Get the YouTube URL from the entry widget
        
        # Extract the video ID from the URL
        video_id = url.split('v=')[1].split('&')[0]
        
        # Fetch video details using the YouTube Data API
        video_title = get_youtube_video_details(video_id)
        
        # Creating a YouTube object
        yt = YouTube(url)
        
        # Selecting the best available audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        # Create the 'downloads' folder if it doesn't exist
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
        
        # Clean the video title to replace invalid characters in the filename
        cleaned_video_title = clean_filename(video_title)
        
        # Defining the output file path and filename
        output_file_path = os.path.join('downloads', f"{cleaned_video_title}.mp3")
        
        # Downloading the audio stream as an MP3 file
        audio_stream.download(output_path='downloads', filename=f"{cleaned_video_title}.mp3")
        
        result_label.config(text=f"Audio downloaded successfully as MP3:\n{output_file_path}")
    except Exception as e:
        # Print the error message to the console
        print("An error occurred:", e)
        result_label.config(text=f"An error occurred. See console for details.")

# Creating the main application window
app = tk.Tk()
app.title("YouTube Audio Downloader")

# Creating and placing widgets on the window
url_label = tk.Label(app, text="Enter YouTube URL:")
url_label.pack()

url_entry = tk.Entry(app, width=50)
url_entry.pack()

download_button = tk.Button(app, text="Download Audio", command=download_audio_from_youtube)
download_button.pack()

result_label = tk.Label(app, text="")
result_label.pack()

# Start the main event loop
app.mainloop()
