import reflex as rx
from app.states.downloader_state import DownloaderState


def format_selector_card(
    item: dict, on_click: rx.event.EventType, is_selected: rx.Var[bool]
) -> rx.Component:
    return rx.el.button(
        rx.icon(
            item["icon"],
            class_name=rx.cond(
                is_selected,
                "text-orange-500",
                "text-gray-500 dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-gray-200",
            ),
            size=24,
        ),
        rx.el.span(
            item["name"],
            class_name=rx.cond(
                is_selected,
                "text-gray-800 dark:text-gray-50 font-semibold",
                "text-gray-600 dark:text-gray-300 group-hover:text-gray-800 dark:group-hover:text-gray-100",
            ),
        ),
        on_click=on_click,
        class_name=rx.cond(
            is_selected,
            "group flex flex-col items-center justify-center p-4 rounded-xl bg-orange-50 dark:bg-orange-500/10 border-2 border-orange-500 dark:border-orange-400 shadow-sm transition-all duration-200",
            "group flex flex-col items-center justify-center p-4 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 hover:bg-white dark:hover:bg-gray-800 hover:shadow-md hover:border-gray-300 dark:hover:border-gray-600 transition-all duration-200",
        ),
    )


def downloader_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Start Your Download",
                class_name="text-2xl font-bold text-gray-800 mb-2",
            ),
            rx.el.p(
                "Paste a link from any social media platform.",
                class_name="text-gray-500 mb-6",
            ),
            rx.el.div(
                rx.el.input(
                    placeholder="https://...",
                    default_value=DownloaderState.url,
                    on_change=DownloaderState.set_url.debounce(300),
                    class_name="w-full h-14 pl-12 pr-32 text-lg bg-white dark:bg-gray-800 dark:text-gray-100 border-2 border-gray-200 dark:border-gray-700 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all",
                ),
                rx.icon(
                    "link",
                    class_name="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500",
                    size=24,
                ),
                rx.el.button(
                    rx.icon("clipboard-paste", size=20, class_name="mr-2"),
                    "Paste",
                    on_click=DownloaderState.paste_from_clipboard,
                    class_name="absolute right-2 top-1/2 -translate-y-1/2 h-10 px-4 bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 font-semibold flex items-center transition-all",
                ),
                class_name="relative w-full mb-6",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("video", class_name="mr-2", size=18),
                    "Video",
                    on_click=lambda: DownloaderState.set_download_type("video"),
                    class_name=rx.cond(
                        DownloaderState.download_type == "video",
                        "px-6 py-2 rounded-lg bg-orange-500 text-white font-semibold shadow-sm",
                        "px-6 py-2 rounded-lg bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300 font-medium hover:bg-gray-200 dark:hover:bg-gray-600",
                    ),
                ),
                rx.el.button(
                    rx.icon("music-2", class_name="mr-2", size=18),
                    "Audio",
                    on_click=lambda: DownloaderState.set_download_type("audio"),
                    class_name=rx.cond(
                        DownloaderState.download_type == "audio",
                        "px-6 py-2 rounded-lg bg-orange-500 text-white font-semibold shadow-sm",
                        "px-6 py-2 rounded-lg bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300 font-medium hover:bg-gray-200 dark:hover:bg-gray-600",
                    ),
                ),
                class_name="flex space-x-2 p-1 bg-gray-200 dark:bg-gray-800 rounded-xl mb-6 w-fit mx-auto",
            ),
            rx.el.div(
                rx.cond(
                    DownloaderState.download_type == "video",
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Select Video Format",
                                class_name="text-lg font-semibold text-gray-700 dark:text-gray-300",
                            ),
                            rx.el.div(
                                rx.foreach(
                                    DownloaderState.video_formats,
                                    lambda item: format_selector_card(
                                        item,
                                        lambda: DownloaderState.set_video_format(
                                            item["format"]
                                        ),
                                        DownloaderState.selected_video_format
                                        == item["format"],
                                    ),
                                ),
                                class_name="grid grid-cols-2 md:grid-cols-3 gap-4",
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "Select Quality",
                                class_name="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4",
                            ),
                            rx.el.div(
                                rx.foreach(
                                    DownloaderState.quality_options,
                                    lambda q: rx.el.button(
                                        q.upper(),
                                        on_click=lambda: DownloaderState.set_selected_quality(
                                            q
                                        ),
                                        class_name=rx.cond(
                                            DownloaderState.selected_quality == q,
                                            "px-4 py-2 rounded-lg bg-orange-500 text-white font-semibold shadow-sm",
                                            "px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 font-medium hover:bg-gray-200 dark:hover:bg-gray-600",
                                        ),
                                    ),
                                ),
                                class_name="flex flex-wrap gap-2",
                            ),
                        ),
                        class_name="animate-fade-in",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Select Audio Format",
                            class_name="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(
                                DownloaderState.audio_formats,
                                lambda item: format_selector_card(
                                    item,
                                    lambda: DownloaderState.set_audio_format(
                                        item["format"]
                                    ),
                                    DownloaderState.selected_audio_format
                                    == item["format"],
                                ),
                            ),
                            class_name="grid grid-cols-2 md:grid-cols-4 gap-4",
                        ),
                        class_name="animate-fade-in",
                    ),
                ),
                class_name="mb-8",
            ),
            rx.el.button(
                rx.cond(
                    DownloaderState.is_loading,
                    rx.fragment(
                        rx.spinner(class_name="text-white mr-3", size="2"),
                        "Processing...",
                    ),
                    rx.fragment(
                        rx.icon("cloud_download", size=24, class_name="mr-3"),
                        "Download",
                    ),
                ),
                on_click=DownloaderState.start_download,
                disabled=DownloaderState.is_loading | (DownloaderState.url == ""),
                class_name="w-full h-16 text-xl flex items-center justify-center font-bold text-white bg-gradient-to-r from-orange-500 to-red-500 rounded-xl shadow-lg hover:shadow-xl hover:scale-[1.01] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            rx.cond(
                DownloaderState.error_message != "",
                rx.el.div(
                    rx.icon("flag_triangle_right", class_name="text-red-500 mr-2"),
                    rx.el.span(DownloaderState.error_message),
                    class_name="mt-4 text-red-600 bg-red-50 dark:bg-red-900/20 dark:text-red-400 p-3 rounded-lg flex items-center",
                ),
            ),
            rx.cond(
                DownloaderState.is_loading & (DownloaderState.media_info == None),
                rx.el.div(
                    rx.el.div(class_name="w-full h-40 bg-gray-200 rounded-lg"),
                    rx.el.div(
                        rx.el.div(class_name="h-6 bg-gray-200 rounded w-3/4 mb-2"),
                        rx.el.div(class_name="h-4 bg-gray-200 rounded w-1/2"),
                        class_name="mt-4",
                    ),
                    class_name="mt-8 p-4 border border-gray-200 rounded-xl animate-pulse",
                ),
            ),
            rx.cond(
                DownloaderState.media_info != None,
                rx.el.div(
                    rx.el.h3(
                        "Download Ready",
                        class_name="text-xl font-bold text-gray-800 dark:text-gray-100 my-4",
                    ),
                    rx.el.div(
                        rx.el.img(
                            src=DownloaderState.media_info.get(
                                "thumbnail", "/placeholder.svg"
                            ),
                            class_name="w-full h-auto object-cover rounded-lg shadow-md",
                        ),
                        rx.el.div(
                            rx.el.h4(
                                DownloaderState.media_info.get("title", ""),
                                class_name="font-bold text-lg mt-4 text-gray-800 dark:text-gray-100",
                            ),
                            rx.el.p(
                                f"by {DownloaderState.media_info.get('uploader', '')}",
                                class_name="text-sm text-gray-500 dark:text-gray-400",
                            ),
                            rx.el.p(
                                f"Duration: {DownloaderState.media_info.get('duration', '')}",
                                class_name="text-sm text-gray-500 dark:text-gray-400",
                            ),
                            class_name="p-4",
                        ),
                        class_name="bg-white dark:bg-gray-800/50 border dark:border-gray-700 rounded-xl overflow-hidden",
                    ),
                    class_name="mt-8 text-left animate-fade-in",
                ),
            ),
            class_name="w-full max-w-2xl text-center",
        ),
        class_name="w-full bg-white/70 dark:bg-gray-800/50 backdrop-blur-xl p-8 md:p-12 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-800",
    )