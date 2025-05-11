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
    api_url: str = "https://92eed86c-d28d-4ac0-8041-8f06ec9be746.fly.dev"
    backend_host: str = "92eed86c-d28d-4ac0-8041-8f06ec9be746.fly.dev"
    cors_allowed_origins: list = [
        "https://open-reper-cyan-grass.reflex.run",
        "wss://open-reper-cyan-grass.reflex.run",
        "http://localhost:3000"
    ]
    cors_credentials: bool = True

config = AppConfig()