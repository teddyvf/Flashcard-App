# ui.py

import os
from logic import Quiz

class DeckUI():
    def __init__(self, library):
        self.library = library

    def event_loop(self):
        while True:
            self.menu()

    def menu(self):
        print("\nHello! Let's get started:")
        print("(1) Create a new deck")
        print("(2) Choose from existing decks") 
        print("(3) Delete a deck")
        print("(4) Quit")
        selection = input("Selection: ")
        self.advance_screen(int(selection))

    def advance_screen(self, selection):
        if selection == 1:
            self.library.append()
        if selection == 2:
            self.choose_deck()
        if selection == 3:
            pass # for now
        if selection == 4:
            os._exit(0)

    def choose_deck(self):
        # load all decks in /data
        load = self.library.load_library()
        if load == -1:
            print("No decks detected... returning.")
            return

        print("\nPlease choose a deck from below:")

        # view all decks in /data and print them to menu
        for index, deck in enumerate(self.library):
            print(f"({index+1}) {deck.name.title()}") #index+1
        print(f"({index + 2}) Back")
        selection = int(input("Selection: "))

        # if user selected 'back' return to previous menu
        if selection == index + 2:
            return
        
        print(f"Loading {self.library[selection-1].name.title()}")
        # send chosen deck to system2 to handle cards
        CardUI(self.library[selection-1]).event_loop()

class CardUI():
    def __init__(self, deck):
        self.deck = deck

    def event_loop(self):
        while True:
            self.print_screen()

    def print_screen(self):
        print("\nReady to learn with flashcards?")
        print("Select a menu item below:")
        print("(1) View all flashcards")
        print("(2) Add a flashcard")
        print("(3) Delete a flashcard")
        print("(4) Practice")
        print("(5) Load Data")
        print("(6) Save Data")
        print("(7) Quit")
        try:
            selection = input("\nSelection: ") # ensure only integer 1-5
            self.advance_screen(int(selection))
        except:
            print("Please enter a number 1-7...")
            
    def advance_screen(self, selection):
        if selection == 1:
            print("Viewing all flashcards...")
            print(self.deck)
        elif selection == 2:
            print("Adding a flashcard...")
            self.deck.append()
        elif selection == 3:
            print("Deleting a flashcard...")
            self.deck.remove()
        elif selection == 4:
            quiz = Quiz(self.deck)
            quiz.run_quiz()
        elif selection == 5:
            self.deck.load_file()
        elif selection == 6:
            self.deck.save_to_file()
        elif selection == 7:
            save_option = input("Would you like to save before exiting (y/n): ")
            if save_option.lower().strip() == 'y':
                self.deck.save_to_file()
            os._exit(0)

    def clear_screen(self):
        _ = os.system('clear')
