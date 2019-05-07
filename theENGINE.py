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

class Room():
    """
    An Object that is part of the map that the user will explore
    rooms: other rooms that this room connects to
    inventory: a list of items in the rooms possession
    locked: whether paths to other rooms are locked or not
    """
    def __init__(self, name, rooms = None, inventory = None, locked = None):
        self.name = name
        if rooms is None:
            rooms = []
        self.rooms = rooms
        if inventory is None:
            inventory = []
        self.inventory = inventory
        if locked is None:
            locked = []
        self.locked = locked
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
            str += "\n    "+ item
        str += "\n]"
        return str
    def removeItem(self, item):
        self.inventory.remove(item)
    def addItem(self, item):
        self.inventory.append(item)
    def switchRoom(self, direction): #TODO Update for Locks
        """Goes to a connected room if room is unlocked"""
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
    """
    A class that controls the gameplay. This class handles room changes and
     other actions
    startRoom: Room that the player begins in
    rooms: a Dictionary of all rooms
    items: a Dictionary of all items
    attributes: a Dictionary of all attributes
    actions: a Dictionary of all actions
    """
    def __init__(self, startRoom  = "1", rooms = None,items= None, attributes= None, actions= None ):
        self.player = Player()
        if rooms is None:
            rooms = {}
        self.rooms = rooms
        if items is None:
            items = {}
        self.items = items
        if attributes is None:
            attributes = {}
        self.attributes = attributes
        if actions is None:
            actions = {}
        self.actions = actions
        self.currentRoom = rooms["lab"] # TODO Change back to startRoom
    def switchRoom(self, direction):
        """Handles room switching at the game level"""
        str = ""
        if(self.currentRoom.switchRoom(direction) == 0):
            str += "Not a valid Direction. Please try another command."
        elif(self.currentRoom.switchRoom(direction) == ""):
            str +="There's no room there!"
        else:
            str += self.currentRoom.switchRoom(direction)
            self.currentRoom = self.rooms[self.currentRoom.switchRoom(direction)]
        return str
    def prepare_item(self,input):
        """
        Checks if an item exists and then if the associated command exists
        input: String input from user
        """
        item = ""
        command = ""
        for element in self.currentRoom.inventory:
            if input.casefold().find(element)>=0:
                item = element
                for attribute in self.items[item].properties:
                    for action in self.attributes[attribute]:
                        if input.casefold().find(action)>=0:
                            command = action
                            break

                break
        return item, command

    def execute_command(self,command, item):
        """Finds the appropriate reaction to command and executes it """
        str = ""
        if self.actions[command] == "move to inventory" :
            self.currentRoom.removeItem(item)
            self.player.addItem(item)
            str += item + "moved to inventory"
        elif self.actions[command] == "move to placeable" :
            self.player.removeItem(item)
            self.currentRoom.addItem(item)
            str += item + "removed to Inventory"
        elif self.actions[command] == "no reaction":
            str += "Legit Nothing Happens"
        elif self.actions[command] == "use _":
            #TODO Interact with doors
            pass
        else:
            str+="Sorry that command doesn't do anything"
    def help(self):
        """Displays all possible commands"""
        str= "These are all the recognized commands in Adventured Unlocked\n"
        for attribute in self.attributes:
            if not self.attributes[attribute] == []:
                str += ', '.join(self.attributes[attribute])
                str += '\n'
        str += "go north\n"
        str += "go east\n"
        str += "go south\n"
        str += "go west"
        return str
    def helpitem(self, item):
        """Displays all possible commands associated with an item"""
        str = "These are all the way to interact with " + item + "\n"
        for attribute in self.items[item].properties:
            str += ', '.join(self.attributes[attribute])
            str += '\n'
        return str












    def handleInput(self, input):
        """First point of contact for user input. Parses user input string and
        responds with appropriate reaction
        input: user input
        """
        str = []
        item,command = self.prepare_item(input)


        if(input.casefold().find("go ")>=0):
            str.append(self.switchRoom(input))
        elif(input.casefold().find("view")>=0):
            if(input.casefold().find("inventory")>=0):
                str.append(self.player.viewInventory())
            else:
                str.append( game.currentRoom.viewInventory())

        elif item and (input.casefold().find("help")>=0):
            str.append(self.helpitem(item))
        elif (input.casefold().find("help")>=0):
            str.append(self.help())
        elif not item:
            str.append("This item is not in this room")
        elif not command:
            str.append("You can't do that to this item")
        elif item and command:
            str.append(self.execute_command(command, item))
        else:
            str.append( "Sorry this action is not supported just yet\n\n")

        str.append("You are in: " + game.currentRoom.name + "\n")
        str.append( "What do you do?")
        return str

def load_attibutes(attributeFile):
    """Loads attributes file"""
    with open(attributeFile, 'r') as file:
        data = file.read().replace('"', '\"')
    adata = json.loads(data)
    attributes = {}
    actions = {}
    for attribute in adata:
        attributes[attribute] = []
        if 'prompts' in adata[attribute]:
            for i, actionset in enumerate(adata[attribute]['prompts']):
                attributes[attribute].extend(actionset)
                for action in actionset:
                    actions[action] = adata[attribute]['reactions'][i]
            else: #TODO handle non prompts case
                pass
    return attributes, actions


def load_items(itemsFile):
    """Loads items file"""
    with open(itemsFile, 'r') as file:
        data = file.read().replace('"', '\"')
    itemsdata = json.loads(data)
    items = {}
    for item in itemsdata:
        items[item] = Item(item,itemsdata[item])
    return items

def load_rooms(roomsFile):
    """Loads rooms file"""
    with open(roomsFile, 'r') as file:
        data = file.read().replace('"', '\"')
    roomsdata = json.loads(data)
    rooms = {}
    for i,room in enumerate(roomsdata):
        if i == 0:
            startRoom = room
        rooms[room] = Room(str(room),roomsdata[room]["directions"],
        roomsdata[room]["items"], None) #roomsdata[room]["locks"]
    return rooms, startRoom

class MusicThread(threading.Thread):
    """
    Class to handle creation of music class. Creates a seperate thread to run
    parallel to game
    """
    def run(self):
        song = music.Song()

        game = True
        text = 'asdf'
        temp = text

        while song.sonic_is_open and game:
            if temp != text:
                song.update_song()
            song.play_phrase()
            temp = text

        song.close_sonicpi()



def startGame(rooms,startRoom,items, attributes, actions):
    """
    Method to set up game Object for gameplay and start music thread
    """
    # mythread = MusicThread(name = "Thread-{}".format(1))  # ...Instantiate a thread and pass a unique ID to it
    # mythread.start()

    game = Game(startRoom,rooms,items, attributes, actions)
    str = ""
    # str +="Welcome to Adventure Unlocked \n "
    str += "You are in: " + game.currentRoom.name
    return game, str
    # while True:
    #
    #     print(game.handleInput(input("")))
        # if(choice.casefold().find("go")>=0):
        #     game.switchRoom(choice)
        # elif(choice.casefold().find("inventory")>=0):
        #     game.player.viewInventory()
        #     print(game.currentRoom.viewInventory())
        # else:
        #     print("Sorry this action is not supported just yet")

if __name__ == '__main__':
    attributes, actions = load_attibutes("content/attributes.json")
    items = load_items("content/items.json")
    rooms, startRoom = load_rooms("content/rooms.json")
    game, str = startGame(rooms, startRoom,items, attributes, actions)
    print("Welcome to Adventure Unlocked")
    print("You are in: " + game.currentRoom.name)
    while True:
        for stuff in game.handleInput(input("")):
            print(stuff)
