from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from starlette.responses import FileResponse
import yt_dlp
import logging
import reflex as rx
from pathlib import Path
import time
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
api = FastAPI()
DOWNLOAD_DIR = Path(".web/public/downloads")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def format_duration(seconds: int | float | None) -> str:
    if seconds is None:
        return "N/A"
    try:
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = seconds % 3600 // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        return f"{minutes:02d}:{secs:02d}"
    except (ValueError, TypeError) as e:
        logging.exception(f"Error formatting duration: {e}")
        return "N/A"


def sanitize_filename(filename: str) -> str:
    return re.sub("[^a-zA-Z0-9_.-]", "_", filename)


@api.get("/api/info")
async def get_info(url: str = Query(...)):
    logger.info(f"Fetching info for URL: {url}")
    ydl_opts = {"noplaylist": True, "quiet": True, "no_warnings": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return JSONResponse(
                content={
                    "title": info.get("title", "Unknown Title"),
                    "thumbnail": info.get("thumbnail", "/placeholder.svg"),
                    "duration": format_duration(info.get("duration")),
                    "uploader": info.get("uploader", "Unknown Uploader"),
                }
            )
    except Exception as e:
        logging.exception(f"Error fetching info for {url}: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@api.get("/api/download")
async def download_media(
    url: str = Query(...),
    format: str = Query("mp4"),
    type: str = Query("video"),
    quality: str = Query("best"),
):
    logger.info(f"Starting download for URL: {url} with format: {format}")
    try:
        with yt_dlp.YoutubeDL(
            {"noplaylist": True, "quiet": True, "no_warnings": True}
        ) as ydl:
            info = ydl.extract_info(url, download=False)
        title = sanitize_filename(info.get("title", f"download_{int(time.time())}"))
        filename = f"{title}.{format}"
        filepath = DOWNLOAD_DIR / filename
        ydl_opts = {
            "outtmpl": str(filepath),
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
        }
        if type == "audio":
            ydl_opts.update(
                {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {"key": "FFmpegExtractAudio", "preferredcodec": format}
                    ],
                }
            )
        else:
            quality_selector = {
                "best": "bestvideo+bestaudio/best",
                "1080p": f"bestvideo[height<=1080][ext={format}]+bestaudio/bestvideo[height<=1080]+bestaudio/best",
                "720p": f"bestvideo[height<=720][ext={format}]+bestaudio/bestvideo[height<=720]+bestaudio/best",
                "480p": f"bestvideo[height<=480][ext={format}]+bestaudio/bestvideo[height<=480]+bestaudio/best",
            }.get(quality, "bestvideo+bestaudio/best")
            ydl_opts["format"] = quality_selector
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        downloaded_file = next(DOWNLOAD_DIR.glob(f"{title}.*"), None)
        if not downloaded_file:
            raise FileNotFoundError("Downloaded file not found.")
        return JSONResponse(
            content={
                "download_url": f"/downloads/{downloaded_file.name}",
                "filename": downloaded_file.name,
            }
        )
    except Exception as e:
        logging.exception(f"Error downloading {url}: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)