#main.py

import ui
from logic import Library

if __name__ == '__main__':

    ui.DeckUI(Library()).event_loop()