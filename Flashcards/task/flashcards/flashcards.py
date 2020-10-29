# Write your code here
import random
import json
import argparse


def print2(print_object):
    with open("mylog.txt", "a") as logger:
        print(print_object)
        logger.write(print_object)
        logger.write("\n")


def input2():
    with open("mylog.txt", "a") as logger:
        input_object = input()
        logger.write(input_object)
        logger.write("\n")
    return input_object


def save_cards(card_dictionary, file_name=None):
    if not file_name:
        print2("File name:")
        file_name = input2()

    with open(file_name, mode="w") as card_file:
        card_file.writelines(json.dumps(card_dictionary))
    print2("{} cards have been saved.".format(str(len(card_dictionary))))
    return


def load_cards(card_dictionary: dict, file_name=None):
    if not file_name:
        print2("File name:")
        file_name = input2()

    try:
        with open(file_name, mode="r") as card_file:
            loaded_cards = json.load(card_file)
        print2("{} cards have been loaded.".format(str(len(loaded_cards))))
        return {**card_dictionary, **loaded_cards}
    except FileNotFoundError:
        print2("File not found.")
        return card_dictionary


def define_cards():
    cards_dictionary = {}
    number_of_cards = int(input("Input the number of cards:\n"))
    for i in range(number_of_cards):
        print2("The term for card #{}:".format(str(i + 1)))
        while True:
            term = input2()
            if term in cards_dictionary.keys():
                print2('The term "{}" already exists. Try again:'.format(term))
            else:
                break
        print2("The definition for card #{}:".format(str(i + 1)))
        while True:
            definition = input2()
            if definition in cards_dictionary.values():
                print2('The definition "{}" already exists. Try again:'.format(definition))
            else:
                break
        cards_dictionary[term] = (definition, 0)
    return cards_dictionary


def add_card(card_dictionary):
    print2("The card:")
    while True:
        term = input2()
        if term in card_dictionary.keys():
            print2('The term "{}" already exists.'.format(term))
            # return card_dictionary
        else:
            break
    print2("The definition of the card:")
    while True:
        definition = input2()
        values = [value for (value, count) in card_dictionary.values()]
        if definition in values:
            print2('The definition "{}" already exists.'.format(definition))
            # return card_dictionary
        else:
            break
    card_dictionary[term] = (definition, 0)
    print2('The pair ("{}":"{}") has been added.'.format(term, definition))
    return card_dictionary


def remove_card(card_dictionary: dict) -> dict:
    print2("Which card?")
    while True:
        term = input2()
        if term not in card_dictionary.keys():
            print2('Can\'t remove "{}": there is no such card.'.format(term))
            break
        else:
            card_dictionary.pop(term)
            print2("The card has been removed")
            break
    return card_dictionary


def use_flashcard(term, definition, cards_dictionary):
    print('Print the definition of "{}":'.format(term))
    answer = input2()
    if answer == definition:
        print2("Correct")
    else:
        values = [value for (value, count) in cards_dictionary.values()]
        if answer in values:
            term = [key for key, value in cards_dictionary.items() if value[0] == answer][0]
            print2('Wrong. The right answer is "{}", but your definition is correct for "{}"'.format(definition, term))
        else:
            print2('Wrong. The right answer is "{}."'.format(definition))
        cards_dictionary[term] = (cards_dictionary[term][0], cards_dictionary[term][1] + 1)
    return cards_dictionary


def ask(card_dictionary: dict) -> dict:
    print2("How many times to ask?")
    ask_times = int(input2())
    if len(card_dictionary) > 0:
        for _ in range(ask_times):
            random_item = random.choice(list(card_dictionary.items()))
            card_dictionary = use_flashcard(random_item[0], random_item[1][0], card_dictionary)
    else:
        print2("No cards available.")
    return card_dictionary


def hardest_card(card_dictionary: dict):
    highest_mistake_count = 0
    hardest_cards = []
    for card in card_dictionary.items():
        term = card[0]
        mistake_count = card[1][1]
        if 0 < mistake_count >= highest_mistake_count:
            if mistake_count > highest_mistake_count:
                hardest_cards = []
            highest_mistake_count = mistake_count
            hardest_cards.append('"{}"'.format(term))
    if highest_mistake_count == 0:
        print2("There are no cards with errors")
    elif len(hardest_cards) == 1:
        term = hardest_cards[0]
        print2('The hardest card is {}. You have {} errors answering it.'.format(term, str(highest_mistake_count)))
    else:
        terms = ", ".join(hardest_cards)
        print2('The hardest cards are {}. You have {} errors answering them.'.format(terms, str(highest_mistake_count)))


def reset_stats(card_dictionary: dict) -> dict:
    for term in card_dictionary.keys():
        card_dictionary[term] = (card_dictionary[term][0], 0)
    print2("Card statistics has been reset.")
    return card_dictionary


def save_log():
    print2("File name:")
    file_name = input2()
    with open("mylog.txt", "r") as log:
        log = log.readlines()
    with open(file_name, "w") as new_log:
        new_log.writelines(log)

    print2("The log has been saved.")
    return


def main_menu():
    cards = {}
    starting_arguments = parse_arguments()
    init_logfile()
    if starting_arguments.get("import_from"):
        cards = load_cards(cards, starting_arguments["import_from"])
    possible_actions = ["add", "remove", "import", "export", "ask", "exit", "log", "hardest card", "reset stats"]
    while True:
        print2("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        action = input2()
        if action not in possible_actions:
            print2("Unknown command")
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
            cards = ask(cards)
        elif action == "exit":
            if starting_arguments.get("export_to"):
                save_cards(cards, starting_arguments.get("export_to"))
            else:
                print2("bye bye")
            return
        elif action == "log":
            save_log()
        elif action == "hardest card":
            hardest_card(cards)
        elif action == "reset stats":
            cards = reset_stats(cards)
        else:
            print2("What the f happened?")


def parse_arguments() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument('--import_from')
    parser.add_argument('--export_to')
    args = parser.parse_args()
    arguments = {}
    unparsed_arguments = []
    if args.import_from:
        arguments["import_from"] = args.import_from
    if args.export_to:
        arguments["export_to"] = args.export_to
    # for argument in unparsed_arguments:
    #         argument_parts = argument.split("=")
    #         arguments[argument_parts[0]] = argument_parts[1]
    return arguments


def init_logfile():
    with open("mylog.txt", "w") as _:
        pass  # create initial file


main_menu()
