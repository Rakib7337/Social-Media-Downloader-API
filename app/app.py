import reflex as rx
from app.components.header import header
from app.components.hero import hero
from app.components.downloader_form import downloader_form
from app.api import api
from app.components.download_history import download_history
from app.states.downloader_state import DownloaderState


def index() -> rx.Component:
    return rx.el.main(
        header(),
        rx.el.div(
            hero(),
            downloader_form(),
            download_history(),
            class_name="container mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 pb-24",
        ),
        rx.window_event_listener(on_key_down=DownloaderState.handle_key_down),
        class_name="font-['Open_Sans'] bg-gray-50 dark:bg-gray-900 min-h-screen transition-colors duration-300",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
        rx.el.script(
            src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.2/dist/confetti.browser.min.js"
        ),
    ],
)
app.add_page(index)
app.api = api