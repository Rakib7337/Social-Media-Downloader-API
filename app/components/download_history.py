import reflex as rx
from app.states.downloader_state import DownloaderState, DownloadHistoryItem


def history_item_card(item: DownloadHistoryItem) -> rx.Component:
    return rx.el.div(
        rx.el.img(
            src=item["thumbnail"],
            fallback="/placeholder.svg",
            class_name="w-24 h-24 object-cover rounded-lg flex-shrink-0 bg-gray-100 dark:bg-gray-700",
        ),
        rx.el.div(
            rx.el.h4(
                item["title"],
                class_name="font-bold text-gray-800 dark:text-gray-100 truncate",
            ),
            rx.el.p(
                f"by {item['uploader']}",
                class_name="text-sm text-gray-500 dark:text-gray-400",
            ),
            rx.el.p(
                f"Duration: {item['duration']}",
                class_name="text-sm text-gray-500 dark:text-gray-400",
            ),
            rx.el.button(
                rx.icon("download", size=16, class_name="mr-2"),
                "Download Again",
                on_click=rx.download(
                    url=item["download_url"], filename=item["filename"]
                ),
                class_name="mt-2 px-3 py-1 text-xs font-semibold text-orange-600 bg-orange-100 dark:bg-orange-900/50 dark:text-orange-300 rounded-md hover:bg-orange-200 dark:hover:bg-orange-800/50 transition-colors",
            ),
            class_name="flex-grow min-w-0 ml-4",
        ),
        class_name="flex items-center p-4 bg-white dark:bg-gray-800/50 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md hover:border-gray-200 dark:hover:border-gray-600 transition-all",
    )


def download_history() -> rx.Component:
    return rx.cond(
        DownloaderState.download_history.length() > 0,
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Download History",
                    class_name="text-xl font-bold text-gray-800 dark:text-gray-100",
                ),
                rx.el.button(
                    rx.icon("trash-2", size=16, class_name="mr-2"),
                    "Clear History",
                    on_click=DownloaderState.clear_history,
                    class_name="px-3 py-1 text-sm font-semibold text-red-600 bg-red-100 dark:bg-red-900/50 dark:text-red-400 rounded-md hover:bg-red-200 dark:hover:bg-red-900/80 transition-colors",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.el.div(
                rx.foreach(DownloaderState.download_history, history_item_card),
                class_name="grid gap-4",
            ),
            class_name="w-full max-w-4xl mt-12 animate-fade-in",
        ),
    )