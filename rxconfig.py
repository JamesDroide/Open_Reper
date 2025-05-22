import reflex as rx

class AppConfig(rx.Config):
    app_name: str = "open_reper"
    logo: str = "assets/logo_open_reper.png"
    breakpoints: dict = {
        "mobile": "480px",
        "tablet": "768px",
        "desktop": "1024px",
    }
    backend_port: int = 8000

config = AppConfig()
