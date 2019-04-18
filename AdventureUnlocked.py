"""
A Text Based Adventure Game
SofDes Final Project
"""
import json

class Item ():
    def __init__(self, name, properties = None, reactions = None):
        self.name = name
        if properties is None:
            properties = {}
        self.properties = properties
    def __str__():
        str = "Item[ Name: "+ name + "\nInventory"
        for property in properties:
            str += "    \n"+ property + " " + properties[property]
        str +="\n]\n"
        return str
class Player():
    def __init__ (self, inventory = None):
        if inventory is None:
            inventory = []
        self.inventory = inventory
    def __str__():
        str = "Player[ Name: "+ name + "\nInventory";
        for item in inventory:
            str += "    \n"+ item
        str +="\n]\n"
        return str
class Event():
    def __init__(self, actions = None, events = None ):
        if actions is None:
            self.inventory = {}
        if events is None:
            self.events = []
class Game():
    def __init__(self, events = None):
        self.player = Player()
        if events is None:
            events = {}
        self.events = events
        self.currentEvent = events["start"][0]
    def getEvent(event):
        self.event = events[event]

def load_game(game):
    with open('test.json', 'r') as file:
        data = file.read().replace('"', '\"')

    return json.loads(data)



if __name__ == '__main__':
    game = Game(load_game("test1.json"))
    while game.events[game.currentEvent][0] != 0:
        print(game.currentEvent)
        print("\nYour chioces\n")
        # print(len(game.events[game.currentEvent[0]]))
        for i in range(len(game.events[game.currentEvent])):
            # print(str(game.events[game.currentEvent]))
            print("Type " + str(i) + " for " + str(game.events[game.currentEvent][i]))
        choice = input("What is your decision")
        game.currentEvent = game.events[game.currentEvent][int(choice)]
    print("oops. You died. Sucker.")
