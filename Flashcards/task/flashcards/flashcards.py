# Write your code here
import random
import json


def save_cards(card_dictionary):
    print("File name:")
    file_name = input()

    with open(file_name, mode="w") as card_file:
        card_file.writelines(json.dumps(card_dictionary))
    print(len(card_dictionary), "cards have been saved.")
    return


def load_cards(card_dictionary: dict):
    print("File name:")
    file_name = input()

    try:
        with open(file_name, mode="r") as card_file:
            loaded_cards = json.load(card_file)
        print(len(loaded_cards), "cards have been loaded.")
        return {**card_dictionary, **loaded_cards}
    except FileNotFoundError:
        print("File not found.")
        return card_dictionary


def define_cards():
    cards_dictionary = {}
    number_of_cards = int(input("Input the number of cards:\n"))
    for i in range(number_of_cards):
        print("The term for card #{}:".format(str(i + 1)))
        while True:
            term = input()
            if term in cards_dictionary.keys():
                print('The term "{}" already exists. Try again:'.format(term))
            else:
                break
        print("The definition for card #{}:".format(str(i + 1)))
        while True:
            definition = input()
            if definition in cards_dictionary.values():
                print('The definition "{}" already exists. Try again:'.format(definition))
            else:
                break
        cards_dictionary[term] = definition
    return cards_dictionary


def add_card(card_dictionary):
    print("The card:")
    while True:
        term = input()
        if term in card_dictionary.keys():
            print('The term "{}" already exists.'.format(term))
            # return card_dictionary
        else:
            break
    print("The definition of the card:")
    while True:
        definition = input()
        if definition in card_dictionary.values():
            print('The definition "{}" already exists.'.format(definition))
            # return card_dictionary
        else:
            break
    card_dictionary[term] = definition
    print('The pair ("{}":"{}") has been added.'.format(term, definition))
    return card_dictionary


def remove_card(card_dictionary: dict) -> dict:
    print("Which card?")
    while True:
        term = input()
        if term not in card_dictionary.keys():
            print('Can\'t remove "{}": there is no such card.'.format(term))
            break
        else:
            card_dictionary.pop(term)
            print("The card has been removed")
            break
    return card_dictionary


def use_flashcard(term, definition, cards_dictionary):
    answer = input('Print the definition of "{}":\n'.format(term))
    if answer == definition:
        print("Correct")
    else:
        if answer in cards_dictionary.values():
            term = [key for (key, value) in cards_dictionary.items() if value == answer][0]
            print('Wrong. The right answer is "{}", but your definition is correct for "{}"'.format(definition, term))
        else:
            print('Wrong. The right answer is "{}."'.format(definition))


def ask(card_dictionary: dict):
    print("How many times to ask?")
    ask_times = int(input())
    for _ in range(ask_times):
        random_item = random.choice(list(card_dictionary.items()))
        use_flashcard(random_item[0], random_item[1], card_dictionary)


def main_menu():
    cards = {}
    possible_actions = ["add", "remove", "import", "export", "ask", "exit"]
    while True:
        print("Input the action (add, remove, import, export, ask, exit):")
        action = input()
        if action not in possible_actions:
            print("Unknown command")
            continue
        if action == "add":
            cards = add_card(cards)
        elif action == "remove":
            cards = remove_card(cards)
        elif action == "import":
            cards = load_cards(cards)
        elif action == "export":
            save_cards(cards)
        elif action == "ask":
            ask(cards)
        elif action == "exit":
            print("bye bye")
            return
        else:
            print("What the f happened?")


main_menu()


