import reflex as rx

config = rx.Config(
    app_name="open_reper",
    logo="assets/logo_open_reper.png",
    breakpoints={
        "mobile": "480px",
        "tablet": "768px",
        "desktop": "1024px",
    },
    backend_port = 8001
)