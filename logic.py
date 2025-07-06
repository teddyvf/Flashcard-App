# flashcard logic

from collections.abc import MutableSequence
import random
import json
import os
import re

class Card():
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def __repr__(self):
        return "Card({self.question!r}, {self.answer!r})"
    
    def __str__(self):
        return  "Question: {}\nAnswer: {}".format(self.question, self.answer)
    
class Deck(MutableSequence):
    def __init__(self, name):
        self._cards = []
        self.name = name

    def __len__(self):
        return len(self._cards)
    
    def __delitem__(self, index):
        del self._cards[index]

    def __getitem__(self, index):
        return self._cards[index]
    
    def __setitem__(self, index, value):
        self._cards[index] = value

    def insert(self, index, value):
        self._cards.insert(index, value)

    def append(self):
        q = input("Enter Question: ")
        a = input("Enter Answer: ")
        self._cards.append(Card(q, a))

    def remove(self):
        print("Please enter the question of the card you wish to delete")
        question = input("Question: ") 
        for index, card in enumerate(self._cards):
            if question.lower().strip() == card.question.lower().strip():
                del self._cards[index]

    def shuffle(self):
        random.shuffle(self._cards)

    def save_to_file(self):
        filename = f'{self.name.title().replace(" ", "")}.json'
        #convert to dict for json serialization
        card_dict = {}
        if self._cards:
            for card in self._cards:
                card_dict[card.question] = card.answer
        data_path = os.path.join(os.path.dirname(__file__), "data", filename)
        with open(data_path, 'w') as file:
            json.dump(card_dict, file, indent=2)

    def load_file(self, filename):
        data_path = os.path.join(os.path.dirname(__file__), "data", filename + '.json')
        try:
            with open(data_path, 'r') as file:
                card_dict = json.load(file)
                # check if file was empty
                if not card_dict:
                    return
            # convert dict back to Card objects
            for question, answer in card_dict.items():
                self._cards.append(Card(question, answer))
        except FileNotFoundError:
            print("Error. Starting with an empty deck.")

    def __str__(self):
        return "\n\n".join(str(card) for card in self._cards)
    
class Library(MutableSequence):
    def __init__(self):
        self._decks = []

    def __len__(self):
        return len(self._decks)
    
    def __delitem__(self, index):
        del self._decks[index]

    def __getitem__(self, index):
        return self._decks[index]
    
    def __setitem__(self, index, value):
        self._decks[index] = value

    def insert(self, index, value):
        self._decks.insert(index, value)

    def append(self):
        deck_name = input("\nPlease enter name of the deck: ")
        self._decks.append(Deck(deck_name))
        self._decks[-1].save_to_file()
        print(f"\nSuccess! {deck_name.title()} has been created.")

    def load_library(self):
        self._decks = []
        # read all files in /data
        dir_path = 'data'
        target_extension = '.json'

        for filename in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, filename)):
                filename, file_extension = os.path.splitext(filename)
                if file_extension.lower() == target_extension.lower():

                    # separate filename from .json
                    name_without_ext = os.path.splitext(filename)[0]

                    #convert StateCaptials to State Capitals
                    deck_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', name_without_ext)

                    # create deck object from name of deck and append to self._decks
                    self._decks.append(Deck(deck_name))

                    # load cards from that deck (if any)
                    self._decks[-1].load_file(filename)

        if not self._decks:
            return -1

    def __str__(self):
        return "\n\n".join(str(deck.name) for deck in self._decks)
        # have to say deck.name... when said deck, there were no cards! It was accessing decks __str__ which 
        #  accesses card's __str__.
    
class Quiz():
    def __init__(self, deck):
        self.deck = deck
        self.score = 0
        self.total = len(self.deck)

    def run_quiz(self):
        self.deck.shuffle()
        for card in self.deck:
            print(card.question + "?")
            user_attempt = input("Your answer: ")
            if user_attempt.lower().strip() == card.answer.lower().strip():
                print("Correct!\n")
                self.score += 1
            else:
                print("Incorrect. The correct answer was:")
                print(card.answer + "\n")
        print("\n\nFlashcards complete!")
        print(f"Your results: {self.score}/{self.total}!")

    # extend functionality to allow multiple decks and track score for each

