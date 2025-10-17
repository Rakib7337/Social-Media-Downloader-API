import reflex as rx


def hero() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Download Videos & Audio ",
                rx.el.span(
                    "Effortlessly",
                    class_name="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-red-500",
                ),
                class_name="text-4xl md:text-6xl font-extrabold text-gray-800 dark:text-gray-100 mb-6 text-center leading-tight",
            ),
            rx.el.p(
                "Your one-stop solution for downloading content from YouTube, TikTok, Instagram, and more. Fast, free, and simple.",
                class_name="text-lg md:text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto text-center",
            ),
            class_name="py-16 md:py-24",
        ),
        class_name="w-full",
    )