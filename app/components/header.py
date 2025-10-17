import reflex as rx
from app.states.downloader_state import DownloaderState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon("download", class_name="text-orange-500", size=28),
                        rx.el.span(
                            "Media",
                            rx.el.span(
                                "Downloader", class_name="font-bold text-orange-500"
                            ),
                            class_name="text-2xl font-medium text-gray-800 dark:text-gray-100 ml-2",
                        ),
                        class_name="flex items-center",
                    ),
                    href="/",
                ),
                rx.el.nav(
                    rx.el.a(
                        "Features",
                        href="#",
                        class_name="text-gray-600 dark:text-gray-300 hover:text-orange-500 font-medium transition-colors",
                    ),
                    rx.el.a(
                        "FAQ",
                        href="#",
                        class_name="text-gray-600 dark:text-gray-300 hover:text-orange-500 font-medium transition-colors",
                    ),
                    rx.el.a(
                        "Contact",
                        href="#",
                        class_name="text-gray-600 dark:text-gray-300 hover:text-orange-500 font-medium transition-colors",
                    ),
                    class_name="hidden md:flex items-center space-x-8",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon(
                            tag=rx.color_mode_cond(light="moon", dark="sun"),
                            class_name="text-gray-600 dark:text-gray-300 group-hover:text-orange-500 transition-colors",
                        ),
                        on_click=rx.toggle_color_mode,
                        class_name="group p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800",
                    ),
                    rx.el.button(
                        rx.icon("menu", size=24),
                        class_name="md:hidden text-gray-600 dark:text-gray-300 hover:text-orange-500",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="flex items-center justify-between w-full",
            ),
            class_name="container mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-20",
        ),
        class_name="w-full bg-white/50 dark:bg-gray-900/50 backdrop-blur-lg border-b border-gray-100 dark:border-gray-800 sticky top-0 z-40",
    )