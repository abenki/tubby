# Tubby Backend

This is the backend component of the Tubby project, built with Flask. It handles YouTube video information retrieval and download functionality.

## Technologies Used

- **Flask**: A lightweight Python web framework
- **yt-dlp**: A feature-rich YouTube downloader
- **Pydantic**: For data validation and request/response validation
- **Flask-CORS**: For handling Cross-Origin Resource Sharing
- **YouTube Data API**: For fetching video metadata

## Project Structure

```
backend/
├── .env                  # Environment variables (you need to create this)
├── .gitignore            # Git ignore file
├── .python-version       # Python version to be installed in project venv
├── app.py                # Main Flask application
├── pyproject.toml        # Python project configuration
├── README.md             # Project documentation
└── uv.lock               # Cross-platform lockfile (info about project dependencies)
```
