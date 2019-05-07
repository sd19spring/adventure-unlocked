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
        res = "Item[ Name: "+ name + "\nInventory ["
        for property in self.properties:
            res += "\n    "+ property
        res += "    ]\n]\n"
        return res

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
        res = "Player[\n    Inventory ["
        for item in self.inventory:
            res += "    \n"+ item
        res += "\n    ]\nActions ["
        for action in self.actions:
            res += "\n    "+ action
        res +="\n    ]\n]\n"
        return res
    def viewInventory(self):
        """ Displays current state of Inventory"""
        res = "Items Currently in your Inventory: "
        i = ', '.join(self.inventory)
        if i == '':
            i = 'None'
        res += i
        return res
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
    def __init__(self, name, discovered = False, rooms = None, inventory = None, locked = None):
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
        self.discovered = False
    def __str__(self):
        res = "Player[ Name: "+ name + "\nInventory ["
        for item in self.inventory:
            res += "    \n"+ item
        res += "\n    ]\nActions ["
        for action in self.actions:
            res += "\n    "+ action
        res += "\n    ]\nRooms ["
        for room in self.rooms:
            res += "\n    "+ room
        res +="\n    ]\n]\n"
        return res
    def viewInventory(self):
        """ Displays current state of Inventory"""
        res = "Items in this room: "
        i = ', '.join(self.inventory)
        if i == '':
            i = 'None'
        res += i
        return res
    def removeItem(self, item):
        self.inventory.remove(item)
    def addItem(self, item):
        self.inventory.append(item)
    def switchRoom(self, direction): #TODO Update for Locks
        """Goes to a connected room if room is unlocked"""
        direction = direction.casefold()
        if direction.find("north") > 0:
            direction = 0
        elif direction.find("east") > 0:
            direction = 1
        elif direction.find("south") > 0:
            direction = 2
        elif direction.find("west") > 0:
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
    def __init__(self, startRoom  = "1", rooms = None,items= None, attributes=
    None, actions= None, notes = None):
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
        if notes is None:
            notes = {}
        self.notes = notes
        self.currentRoom = rooms[startRoom]
        self.currentRoom.discovered = True
    def switchRoom(self, direction):
        """Handles room switching at the game level"""
        res = ""
        if(self.currentRoom.switchRoom(direction) == 0):
            res += "Not a valid Direction. Please try another command."
        elif(self.currentRoom.switchRoom(direction) == ""):
            res +="There's no room there!"
        else:
            self.currentRoom = self.rooms[self.currentRoom.switchRoom(direction)]
            self.currentRoom.discovered = True
        return res
    def prepare_item(self,input):
        """
        Checks if an item exists and then if the associated command exists
        input: String input from user
        """
        item = ""
        command = ""
        items = []
        items.extend( self.player.inventory)
        items.extend( self.currentRoom.inventory)
        for element in items:
            if input.casefold().find(element)>=0:
                item = element
                for attribute in self.items[item].properties:
                    for action in self.attributes[attribute]:
                        if input.casefold().find(action)>=0:
                            command = action
                            break

                break
        return item, command

    def execute_command(self,command, item, notes):
        """Finds the appropriate reaction to command and executes it """
        res = ""
        if self.actions[command] == "move to inventory" :
            self.currentRoom.removeItem(item)
            self.player.addItem(item)
            res += item + " moved to inventory"
        elif self.actions[command] == "move to placeable" :
            self.player.removeItem(item)
            self.currentRoom.addItem(item)
            res += item + " removed from Inventory"
        elif self.actions[command] == "no reaction":
            res += "Legit Nothing Happens"
        elif self.actions[command] == "examine _":
            # Record note has been viewed
            if not item in notes:
                notes[item] = 1

            note = self.notes[item]
            res += "\n" + item.upper()+ "\n********\n"
            res += note['title'] + "\n"
            res += "Day " + str(note['day']) + '\n'
            res += note['text'] + "\n********\n"
        else:
            res+="Sorry that command doesn't do anything"
        return res
    def help(self):
        """Displays all possible commands"""
        res= "These are all the recognized commands in Adventured Unlocked\n"
        for attribute in self.attributes:
            if not self.attributes[attribute] == []:
                res += ', '.join(self.attributes[attribute])
                res += '\n'
        res += "go north\n"
        res += "go east\n"
        res += "go south\n"
        res += "go west\n"
        res += "view\n"
        res += "view inventory"
        return res
    def helpitem(self, item):
        """Displays all possible commands associated with an item"""
        res = "These are all the way to interact with " + item + "\n"
        for attribute in self.items[item].properties:
            res += ', '.join(self.attributes[attribute])
            res += '\n'
        return res
    def handleInput(self, input, notes):
        """First point of contact for user input. Parses user input resing and
        responds with appropriate reaction
        input: user input
        """
        res = []
        item,command = self.prepare_item(input)
        if(input.casefold().find("go ")>=0):
            s = self.switchRoom(input)
            if s:
                res.append(s)
        elif(input.casefold().find("view")>=0):
            if(input.casefold().find("inventory")>=0):
                res.append(self.player.viewInventory())
            else:
                res.append( self.currentRoom.viewInventory())

        elif item and (input.casefold().find("help")>=0):
            res.append(self.helpitem(item))
        elif (input.casefold().find("help")>=0):
            res.append(self.help())
        elif not item:
            res.append("This item is not in this room")
        elif not command:
            res.append("You can't do that to this item")
        elif item and command:
            res.append(self.execute_command(command, item, notes))
        else:
            res.append( "Sorry this action is not supported just yet")

        res.append("You are in the " + self.currentRoom.name)
        res.append("Around you are the following rooms:")
        if self.currentRoom.rooms[0]:
            room = self.currentRoom.rooms[0]
            if self.rooms[room].discovered:
                res.append("North: "+ room)
            else:
                res.append("North: ?")
        if self.currentRoom.rooms[1]:
            room = self.currentRoom.rooms[1]
            if self.rooms[room].discovered:
                res.append("East: "+ room)
            else:
                res.append("East: ?")
        if self.currentRoom.rooms[2]:
            room = self.currentRoom.rooms[2]
            if self.rooms[room].discovered:
                res.append("South: "+ room)
            else:
                res.append("South: ?")
        if self.currentRoom.rooms[3]:
            room = self.currentRoom.rooms[3]
            if self.rooms[room].discovered:
                res.append("West: "+ room)
            else:
                res.append("West: ?")
        res.append( "What do you do?")
        return clean_output(res)
def clean_output(res):
    out = []
    wrap_len = 125
    for chunk in res:
        arr =  chunk.split("\n")
        for line in arr:
            while len(line) > wrap_len:
                out.append(line[:wrap_len])
                line = line[wrap_len:]
            out.append(line)

            # out.append("")
    return out

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
        rooms[room] = Room(str(room),False, roomsdata[room]["directions"],
        roomsdata[room]["items"], None) #roomsdata[room]["locks"]
    return rooms, startRoom
def load_notes(notesFile):
    with open(notesFile, 'r') as file:
        data = file.read().replace('"', '\"')
    notesdata = json.loads(data)
    return notesdata

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



def startGame():
    """
    Method to set up game Object for gameplay and start music thread
    """
    # mythread = MusicThread(name = "Thread-{}".format(1))  # ...Instantiate a thread and pass a unique ID to it
    # mythread.start()

    attributes, actions = load_attibutes("content/attributes.json")
    items = load_items("content/items.json")
    rooms, startRoom = load_rooms("content/rooms.json")
    notes = load_notes("content/notes.json")
    game = Game(startRoom,rooms,items, attributes, actions, notes)
    res = []
    res.append("You are in the " + game.currentRoom.name)
    res.append("Around you are the following rooms:")
    if game.currentRoom.rooms[0]:
        res.append("North: ?")
    if game.currentRoom.rooms[1]:
        res.append("East: ?")
    if game.currentRoom.rooms[2]:
        res.append("South: ?")
    if game.currentRoom.rooms[3]:
        res.append("West: ?")
    res.append( "What do you do?")
    return game, res

if __name__ == '__main__':
    game, res = startGame()
    for stuff in res:
        print(stuff)

    while True:
        for stuff in game.handleInput(input("")):
            print(stuff)
