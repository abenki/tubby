# Tubby - YouTube Video Downloader

Tubby is a simple web application for downloading YouTube videos. It features a Vue.js frontend and Flask backend.

## Features

- 🔍 Preview video details before downloading
- ⬇️ Download videos
- 🎨 Clean, modern UI built with Vue.js and TailwindCSS / DaisyUI
- 🚀 Fast downloads powered by yt-dlp

## Project Structure

The project is organized into two main components:

- **frontend**: Vue.js application with Tailwind CSS and DaisyUI
- **backend**: Flask API that handles video information retrieval and downloads

## Getting Started

### Prerequisites

- Python 3.13+
- uv package manager (recommended) or pip
- Node.js 18+
- A YouTube Data API key from the [Google Developer Console](https://console.developers.google.com/)

### Installation

1. Clone the repository

2. Set up the backend:
   ```bash
   cd backend
   uv sync
   ```

3. Create a YouTube API Key if you don't already have one.

4. Create a `.env` file in the backend directory:
   ```
   YOUTUBE_API_KEY=your_youtube_api_key_here
   ```

5. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

### Running the App

1. Start the backend server (from the backend directory):
   ```bash
   # Make sure your virtual environment is activated
   uv run app.py
   ```

2. Start the frontend development server (from the frontend directory):
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to http://localhost:5173

## Disclaimer

The authors of this project are not responsible/liable for any misuse of this program that may violate local copyright/DMCA laws. Users use this application at their own risk.

## Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The heart of the video downloading feature
