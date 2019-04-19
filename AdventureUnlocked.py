"""
A Text Based Adventure Game
SofDes Final Project
"""
import json

class Item ():
    """
    An Object that a player can interact with

    properties: A list of way that the player can interact with an Object
    reactions: A list of what happens when a player interacts with an Object
    """
    def __init__(self, name, properties = None, reactions = None):
        self.name = name
        if properties is None:
            properties = []
        self.properties = properties
        if reactions is None:
            reactions = []
        self.reactions = reactions
    def __str__():
        str = "Item[ Name: "+ name + "\nInventory ["
        for property in self.properties:
            str += "\n    "+ property
        str += "    ]\nReactions ["
        for reaction in self.reactions:
            str += "\n    "+ reaction
        str += "    ]\n]\n"
        return str
    def check_property(self, input):
        """
        Checks if the users input is a valid interaction and returns the
        corresponding reaction
        """
        for i, value in enumerate(self.properties):
            if input == property:
                return reactions[i]


# Alternate Implemenation of Item where Properties are the keys for Reaction Values
# class Item ():
#     """
#     An Object that a player can interact with
#
#     properties: A list of way that the player can interact with an Object
#     reactions: A list of what happens when a player interacts with an Object
#     """
#     def __init__(self, name, properties = None, reactions = None):
#         self.name = name
#         if properties is None:
#             properties = {}
#         self.properties = properties
#     def __str__():
#         str = "Item[ Name: "+ name + "\nProperties ["
#         for property in self.properties:
#             str += "\n    "+ property + " " + properties[property]
#         str +="   ]\n]\n"
#         return str
#     def check_property(self, input):
#         if input in self.properties:
#             return self.properties[input]
#         else:
#             # TODO: Implement Add actions.
#             # TODO: Maps user inputs to Similar inputs and adds to list


class Player():
    """
    An Object to store the current state of the user
    inventory: a list of items in the users players possession
    actions: Actions that an user an do.
    """
    def __init__ (self, inventory = None, actions = None):
        if inventory is None:
            inventory = []
        self.inventory = inventory
        if actions is None:
            actions = []
        self.actions = actions
    def __str__():
        str = "Player[ Name: "+ name + "\nInventory ["
        for item in self.inventory:
            str += "    \n"+ item
        str += "\n    ]\nActions ["
        for action in self.actions:
            str += "\n    "+ action
        str +="\n    ]\n]\n"
        return str
    def viewInventory(self):
        """ Displays current state of Inventory"""
        str = "Items Currently in your Inventory ["
        for item in self.inventory:
            str += "    \n"+ item
        str += "\n    ]
        return str
    def removeItem(self, item):
        self.inventory.remove(item)
    def addItem(self, item):
        self.inventory.append(item)
    def viewActions(self):
        """Displays current Actions"""
        str = "Actions ["
        for action in self.actions:
            str += "\n    "+ action
        str +="\n    ]"
        return str
    def updateActions(self, actions):


class Room():
    def __init__(self, name, rooms = None,inventory = None, actions = None):
        self.name = name
        if rooms is None:
            rooms = []
        self.rooms = rooms
        if inventory is None:
            inventory = []
        self.inventory = inventory
        if actions is None:
            actions = []
        self.actions = actions
    def __str__():
        str = "Player[ Name: "+ name + "\nInventory ["
        for item in self.inventory:
            str += "    \n"+ item
        str += "\n    ]\nActions ["
        for action in self.actions:
            str += "\n    "+ action
        str += "\n    ]\nRooms ["
        for room in self.rooms:
            str += "\n    "+ room
        str +="\n    ]\n]\n"
        return str
    def viewInventory(self):
        """ Displays current state of Inventory"""
        str = "Items Currently in your Inventory ["
        for item in self.inventory:
            str += "    \n"+ item
        str += "\n    ]
        return str
    def removeItem(self, item):
        self.inventory.remove(item)
    def addItem(self, item):
        self.inventory.append(item)
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
