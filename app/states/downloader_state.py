import reflex as rx
from typing import TypedDict, Literal, Any
import asyncio
import logging


class VideoFormat(TypedDict):
    icon: str
    name: str
    format: str


class AudioFormat(TypedDict):
    icon: str
    name: str
    format: str


class MediaInfo(TypedDict):
    title: str
    thumbnail: str
    duration: str
    uploader: str


class DownloadResult(TypedDict):
    download_url: str
    filename: str


class DownloadHistoryItem(TypedDict):
    title: str
    thumbnail: str
    duration: str
    uploader: str
    download_url: str
    filename: str
    timestamp: float


class DownloaderState(rx.State):
    url: str = ""
    is_loading: bool = False
    download_type: Literal["video", "audio"] = "video"
    selected_video_format: str = "mp4"
    selected_audio_format: str = "mp3"
    selected_quality: str = "best"
    quality_options: list[str] = ["best", "1080p", "720p", "480p"]
    media_info: MediaInfo | None = None
    error_message: str = ""
    download_result: DownloadResult | None = None
    download_history: list[DownloadHistoryItem] = []
    video_formats: list[VideoFormat] = [
        {"icon": "video", "name": "MP4", "format": "mp4"},
        {"icon": "film", "name": "WebM", "format": "webm"},
        {"icon": "clapperboard", "name": "MKV", "format": "mkv"},
    ]
    audio_formats: list[AudioFormat] = [
        {"icon": "music-2", "name": "MP3", "format": "mp3"},
        {"icon": "music-3", "name": "M4A", "format": "m4a"},
        {"icon": "music-4", "name": "WAV", "format": "wav"},
        {"icon": "file-audio", "name": "FLAC", "format": "flac"},
    ]

    def _reset_status(self):
        self.is_loading = False
        self.media_info = None
        self.error_message = ""
        self.download_result = None

    @rx.event
    def set_download_type(self, type: Literal["video", "audio"]):
        self.download_type = type

    @rx.event
    def set_video_format(self, format: str):
        self.selected_video_format = format

    @rx.event
    def set_audio_format(self, format: str):
        self.selected_audio_format = format

    @rx.event
    def set_selected_quality(self, quality: str):
        self.selected_quality = quality

    @rx.event
    def clear_history(self):
        self.download_history = []
        yield rx.toast.info("Download history cleared.")

    @rx.event
    def handle_key_down(self, key: str):
        if key == "Enter":
            yield DownloaderState.start_download

    @rx.event
    def paste_from_clipboard(self):
        return rx.call_script(
            "navigator.clipboard.readText()", callback=DownloaderState.set_url
        )

    @rx.event
    async def start_download(self):
        if not self.url.strip():
            self.error_message = "Please enter a valid URL."
            yield rx.toast.error(self.error_message)
            return
        self._reset_status()
        self.is_loading = True
        yield rx.toast.info("Fetching media information...")
        try:
            yield rx.call_script(
                f"fetch(`/api/info?url=${{encodeURIComponent('{self.url}')}}`).then(res => res.json())",
                callback=DownloaderState.handle_info_response,
            )
            return
        except Exception as e:
            logging.exception(f"Failed to fetch info: {e}")
            self.is_loading = False
            self.error_message = f"Failed to fetch info: {e}"
            yield rx.toast.error(self.error_message)

    @rx.event
    def handle_info_response(self, response: Any):
        if not response or response.get("error"):
            self.error_message = (
                response.get("error", "No response from server")
                if response
                else "No response from server"
            )
            self.is_loading = False
            return rx.toast.error(self.error_message)
        self.media_info = response
        self.is_loading = False
        yield rx.toast.success("Metadata loaded!")
        return DownloaderState.process_download

    @rx.event
    async def process_download(self):
        self.is_loading = True
        yield rx.toast.info("Starting download... This may take a moment.")
        download_format = (
            self.selected_video_format
            if self.download_type == "video"
            else self.selected_audio_format
        )
        try:
            api_url = f"/api/download?url={self.url}&format={download_format}&type={self.download_type}&quality={self.selected_quality}"
            yield rx.call_script(
                f"fetch(`{api_url}`).then(res => res.json())",
                callback=DownloaderState.handle_download_response,
            )
            return
        except Exception as e:
            logging.exception(f"Download failed: {e}")
            self.is_loading = False
            self.error_message = f"Download failed: {e}"
            yield rx.toast.error(self.error_message)

    @rx.event
    def handle_download_response(self, response: Any):
        if not response or response.get("error"):
            self.error_message = (
                response.get("error", "No response from server during download.")
                if response
                else "No response from server during download."
            )
            self.is_loading = False
            return rx.toast.error(self.error_message)
        self.download_result = response
        self.is_loading = False
        if self.media_info:
            history_item: DownloadHistoryItem = {
                **self.media_info,
                **response,
                "timestamp": asyncio.get_event_loop().time(),
            }
            self.download_history.insert(0, history_item)
        yield rx.toast.success("Download starting...")
        yield rx.download(url=response["download_url"], filename=response["filename"])
        yield rx.call_script(
            "confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } })"
        )