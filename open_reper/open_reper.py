"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx


def index():

    return rx.text("Hola Mundo")

app = rx.App()
app.add_page(index)
