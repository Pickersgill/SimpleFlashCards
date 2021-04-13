import re, sys, os, random

START_MATCH = "\<\<"
END_MATCH = "\>\>"
SPLIT = "---"
HINT_NUM = 3

deckSet = set()
failSet = set()

class Deck:
    def __init__(self, title, cards):
        self.title = title
        self.cards = cards

    def get_cards(self, n):
        return random.sample(self.cards, k=n)
    
    def get_hints(self, card, n):
        return random.sample(set(self.cards) - set([card]), k=n)

    def __str__(self):
        return self.title + "\n" + "".join(list((str(c) + "\n") for c in self.cards))

    def __len__(self):
        return len(self.cards)

class Card:
    def __init__(self, strBlock):
        self.front = None
        self.back = None
        self.decode(strBlock)

    def decode(self, string):
        components = re.sub(START_MATCH + "|" + END_MATCH, "", string).split(SPLIT)
        self.front = components[0]
        self.back = components[1]

    def __str__(self):
        return "<<front: %s, back: %s>>" % (self.front, self.back)
    

def load_deck(deckFile):
    lines = list(filter(lambda x : x is not "", list((re.sub("\\n", "", l) for l in open(deckFile)))))
    title = lines[0]
    cards = list((Card(l) for l in re.findall((START_MATCH + ".*?" + END_MATCH), "".join(lines[1:]))))
    return Deck(title, cards)

def ask_deck(deck):

    failed = set()

    os.system("clear")
    print("LOADED DECK:\n\n " + deck.title)
    print("\nPRESS ANY KEY TO BEGIN")
    num_of_cards = int(input("How many cards?")) if not all_cards else len(deck)
    cards = deck.get_cards(num_of_cards)
    input()
    
    for card in cards:
        os.system("clear")
        print("Prompt: \n" + card.front)
        correct = False
        if hint and len(deck) > HINT_NUM:
            print("Select from: ")
            hints = deck.get_hints(card, HINT_NUM) + [card]
            random.shuffle(hints)
            for i, h in enumerate(hints):
                print("(%d) %s\n" % (i, h.back))
                correct_ans = i if h == card else 0

            response = input("Enter you answer: ")
            try:
                correct = int(response) is not None and int(response) == correct_ans
            except:
                correct = False
        else:
            input("Press any key to reveal...")
            print(card.back)
            correct = input("\nDid you know it?(Y/n)") is not "n"
        if not correct:
            failed.add(card)

    print("You got %d out of %d cards correct." % (len(deck) - len(failed), len(deck)))
    if len(failed) == 0:
        repeat = False
    else:
        repeat = input("Would you like to repeat failed cards?(y/N)") is "y"

    if repeat:
        (ask_deck(Deck(deck.title, failed)))

    return failed

def run(files):
    global deckSet
    for f in files:
        deckSet.add(load_deck(f))

    for deck in deckSet:
        failed = ask_deck(deck)
        os.system("clear")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_dests = list(filter(lambda x : re.match(".*\.deck", x) is not None, sys.argv[1:]))
    else:
        print("File names not given")

    hint = "hint" in sys.argv
    all_cards = "all" in sys.argv
    
    os.system("clear")   
 
    run(file_dests)

