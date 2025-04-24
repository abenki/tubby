from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import yt_dlp
import os
import uuid
import re
import requests
from pydantic import BaseModel, HttpUrl, Field, field_validator
from typing import Optional
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)

load_dotenv()
YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY environment variable is not set")
DOWNLOADS_DIR: str = os.path.expanduser('~/Downloads')

class DownloadRequest(BaseModel):
    url: HttpUrl
    format: str = Field(default="best", description="Video format to download")

class VideoInfo(BaseModel):
    title: str
    ext: str = "mp4" # file extension

class DownloadResponse(BaseModel):
    success: bool
    message: str
    title: Optional[str] = None
    format: Optional[str] = None
    path: Optional[str] = None
    error: Optional[str] = None

class VideoDetailsRequest(BaseModel):
    url: HttpUrl

    @field_validator('url')
    @classmethod
    def validate_youtube_url(cls, v: str) -> str:
        if not extract_video_id(str(v)):
            raise ValueError("Invalid YouTube URL")
        return v

class VideoDetailsData(BaseModel):
    title: str
    channel: str
    thumbnail: str
    duration: str

class VideoDetailsResponse(BaseModel):
    success: bool
    data: Optional[VideoDetailsData] = None
    error: Optional[str] = None

def extract_video_id(url: str) -> Optional[str]:
    """
    Extract YouTube video ID from URL

    Args:
        url: A YouTube URL

    Returns:
        The video ID if found, None otherwise
    """
    regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|\S+\?v=|\S*\/)?([^&\/\n\s]+))'
    match = re.search(regex, url)
    return match.group(1) if match else None

@app.route("/")
def hello_world() -> str:
    return "<p>Hello, World!</p>"

@app.route('/api/video_details', methods=['GET'])
def get_video_details() -> tuple[Response, int]:
    try:
        # Get URL from query parameters
        url = request.args.get('url')
        if not url:
            return jsonify({"success": False, "error": "No URL provided"}), 400

        # Validate URL using Pydantic
        try:
            video_request = VideoDetailsRequest.model_validate({"url": url})
        except ValueError as e:
            return jsonify({"success": False, "error": str(e)}), 400

        # Extract video ID
        video_id = extract_video_id(str(video_request.url))

        # Fetch video details from YouTube API
        api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={YOUTUBE_API_KEY}"
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if 'items' not in data or len(data['items']) == 0:
            return jsonify({"success": False, "error": "Video not found"}), 404

        video = data['items'][0]
        video_details = VideoDetailsData(
            title=video['snippet']['title'],
            channel=video['snippet']['channelTitle'],
            thumbnail=video['snippet']['thumbnails']['high']['url'],
            duration=video['contentDetails']['duration']
        )

        result = VideoDetailsResponse(success=True, data=video_details)
        return jsonify(result.model_dump(exclude_none=True)), 200

    except requests.RequestException as e:
        result = VideoDetailsResponse(success=False, error=f"YouTube API error: {str(e)}")
        return jsonify(result.model_dump(exclude_none=True)), 500
    except Exception as e:
        result = VideoDetailsResponse(success=False, error=f"Unexpected error: {str(e)}")
        return jsonify(result.model_dump(exclude_none=True)), 500

@app.route('/api/download', methods=['POST'])
def download_video() -> tuple[Response, int]:
    try:
        # Parse and validate the request data
        data = request.get_json()
        download_request = DownloadRequest.model_validate(data)

        # Generate a unique filename
        unique_id = str(uuid.uuid4())[:4]
        output_template = os.path.join(DOWNLOADS_DIR, f'%(title)s-{unique_id}.%(ext)s')

        # Configure yt-dlp options
        yt_dlp_options = {
            'format': download_request.format,
            'outtmpl': output_template,
            'quiet': False,
            'no_warnings': False,
            'progress': True
        }

        # Download the video
        with yt_dlp.YoutubeDL(yt_dlp_options) as ydl:
            info_dict = ydl.extract_info(str(download_request.url), download=True)

            if info_dict is None:
                response = DownloadResponse(
                    success=False,
                    message="Failed to extract video information",
                    error="No video information returned"
                )
                return jsonify(response.model_dump(exclude_none=True)), 500

            # Create a VideoInfo object from the returned info
            try:
                video_info = VideoInfo(
                    title=info_dict.get('title', 'video'),
                    ext=info_dict.get('ext', 'mp4')
                )
            except Exception as e:
                response = DownloadResponse(
                    success=False,
                    message="Failed to process video information",
                    error=str(e)
                )
                return jsonify(response.model_dump(exclude_none=True)), 500

            # Determine the actual filename based on the template
            filename = f"{video_info.title}-{unique_id}.{video_info.ext}"
            filepath = os.path.join(DOWNLOADS_DIR, filename)

        # Create success response
        response = DownloadResponse(
            success=True,
            message=f"Video downloaded successfully as {filename}",
            title=video_info.title,
            format=download_request.format,
            path=filepath
        )
        return jsonify(response.model_dump(exclude_none=True)), 200

    except Exception as e:
        response = DownloadResponse(
            success=False,
            message="Download failed",
            error=str(e)
        )
        return jsonify(response.model_dump(exclude_none=True)), 500

if __name__ == '__main__':
    app.run(debug=True)
