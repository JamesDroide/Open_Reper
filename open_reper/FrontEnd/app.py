''' frontend/app.py
import reflex as rx
from FrontEnd.views.index import index_view
from FrontEnd.views.send_game import send_game_view
from FrontEnd.views.recommended import recommended_view

app = rx.App()

app.add_page(index_view, route="/")
app.add_page(send_game_view, route="/send-game")
app.add_page(recommended_view, route="/opening-recommended")

if __name__ == "__main__":
    app.run()'''