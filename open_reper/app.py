import reflex as rx
from open_reper.frontend.pages.send_game import send_game
from open_reper.frontend.pages.recommended_opening import recommended_opening

app = rx.App()
app.add_page(send_game)
app.add_page(recommended_opening)

app.run()
