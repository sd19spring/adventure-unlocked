"""
A Text Based Adventure Game
SofDes Final Project
"""
import json
import threading
import music

class Item ():
    """
    An Object that a player can interact with

    properties: A list of way that the player can interact with an Object
    reactions: A list of what happens when a player interacts with an Object
    """
    def __init__(self, name, properties = None):
        self.name = name
        if properties is None:
            properties = []
        self.properties = properties
    def __str__(self):
        str = "Item[ Name: "+ name + "\nInventory ["
        for property in self.properties:
            str += "\n    "+ property
        str += "    ]\n]\n"
        return str
    def check_property(self, input):
        """
        Checks if the users input is a valid interaction and returns the
        corresponding reaction
        """
        for i, value in enumerate(self.properties):
            return input == property

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
    def __str__(self):
        str = "Player[\n    Inventory ["
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
        str += "\n    ]"
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
        pass

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
    def __str__(self):
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
        str = "Items in this room ["
        for item in self.inventory:
            str += "    \n"+ item
        str += "\n    ]"
        return str
    def removeItem(self, item):
        self.inventory.remove(item)
    def addItem(self, item):
        self.inventory.append(item)
    def switchRoom(self, direction):
        direction = direction.casefold()
        if direction.find("up") > 0 or direction.find("north") > 0:
            direction = 0
        elif direction.find("left") > 0 or direction.find("east") > 0:
            direction = 1
        elif direction.find("down") > 0 or direction.find("south") > 0:
            direction = 2
        elif direction.find("right") > 0 or direction.find("west") > 0:
            direction = 3
        else:
            return 0
        return self.rooms[direction]

class Game():
    def __init__(self, startRoom, rooms = None):
        self.player = Player()
        if rooms is None:
            rooms = {}
        self.rooms = rooms
        print(startRoom)
        self.currentRoom = rooms[startRoom]
         #TODO Start Room with Rich
    def switchRoom(self, direction):
        if(self.currentRoom.switchRoom(direction) == 0):
            print("Not a valid Direction. Please try another command.")
        elif(self.currentRoom.switchRoom(direction) == ""):
            print("There's no room there!")
        else:
            print(self.currentRoom.switchRoom(direction))
            self.currentRoom = self.rooms[self.currentRoom.switchRoom(direction)]


def load_items(itemsFile):
    with open(itemsFile, 'r') as file:
        data = file.read().replace('"', '\"')
    itemsdata = json.loads(data)
    items = {}
    for item in itemsdata:
        items[item] = Item(item,itemsdata[item])
    return items
    return json.loads(data)

def load_rooms(roomsFile):
    with open(roomsFile, 'r') as file:
        data = file.read().replace('"', '\"')
    roomsdata = json.loads(data)
    rooms = {}
    for i,room in enumerate(roomsdata):
        if i == 0:
            startRoom = room
            print(type(startRoom))
        rooms[room] = Room(str(room),roomsdata[room]["directions"], roomsdata[room]["items"], None)

    return startRoom, rooms
class MusicThread(threading.Thread):
    def run(self):
        test = music.Song()
        test.play_song()



if __name__ == '__main__':

    mythread = MusicThread(name = "Thread-{}".format(1))  # ...Instantiate a thread and pass a unique ID to it
    mythread.start()
    startRoom, rooms = load_rooms("content/rooms.json")
    game = Game(startRoom, rooms)
    print("Welcome to Adventure Unlocked")
    while True:
        print("You are in: " + game.currentRoom.name)
        choice = input("What do you do?")
        if(choice.casefold().find("go")>=0):
            game.switchRoom(choice)
        elif(choice.casefold().find("inventory")>=0):
            game.player.viewInventory()
            print(game.currentRoom.viewInventory())
        else:
            print("Sorry this action is not supported just yet")
