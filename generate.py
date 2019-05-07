"""
Generates JSON file that composes the game interactions
"""

import json, os, errno, random
from queue import *
from collections import defaultdict
from generation.world import ATTRIBUTES, OBJECT_TYPES, ITEMS, ROOMS, OUTSIDE, LOWER_FLOORS
from generation.notes import Notes
from generation.event import Event

def write_attributes():
    """
    Writes item attributes to ./content/attributes.json 
    """
    with open_w('./content/attributes.json') as f:
        json.dump(ATTRIBUTES, f)

def generate_items(n):
    """Generates n items and writes to ./content/items.json
    
    Items contains list of attributes that describe their properties. 

    Args:
        n (int): Number of unique items to generate

    Returns:
        Dictionary of generated items
    """
    items = defaultdict(dict)

    # Fill n items with correctly mapped attributes and store in items dictionary
    for i in range(n):
        item, properties = random.choice(list(ITEMS.items()))
        # print(item, properties)
        attributes = []
        for p in properties:
            # TODO: Add random contextual attribute
            if p in OBJECT_TYPES.keys():
                attributes.extend(OBJECT_TYPES[p])
            elif p in ATTRIBUTES:
                attributes.append(p)

        items[item] = attributes
    
    # Add notes as items
    path = './content/notes.json'
    notes = Notes.from_json(path)
    for i in notes.keys():
        if i == 'note 2' or i == 'note 4':
            items[i] = ['event', 'portable']
        else:
            items[i] = ['portable']

    # Generate events for all items that have an event attribute
    path = './content/events.json'
    Event.setup(path)
    for i in list(items.keys()):
        if 'event' in items[i]:
            generate_event(i, path)

    # Write items to a json file
    with open_w('./content/items.json') as f:
        json.dump(items, f)
    
    return items

def generate_event(item, path):
    """
    Generates events for items that have the event attribute. Writes these events to a json file.
    """
    text, goal, reaction, exit_trigger = None, None, None, None
    if item == 'note 2':
        text = 'Monologue: I wonder what he has figured out. Seems interesting though'
    elif item == 'note 4':
        text = 'Monologue: What have I gotten myself into..'
        goal = 'Solve the murder'
        reaction = 'move key to inventory'
    elif item == 'mirror':
        text = 'Am I the murderer?'
        reaction = 'end game'

    event = Event(item, text, goal, reaction, exit_trigger)
    event.to_json(path)

def generate_rooms(n, f, items):
    """Generates n rooms and writes to /content/rooms.json 
    
    Rooms describe what items are in it and what other rooms (directions) are possible to navigate to. Directions are
    ordered in north, east, south, west or up, right, down, left directions.

    Args:
        n (int): Number of unique rooms to generate
        f (int): Number of floors
        items (dict): Dictionary of possible unique items in the world
    """
    rooms = defaultdict(dict)

    # Choose n rooms and fill 2D list of rooms by floor
    # TODO: Basements
    # possible_rooms = []
    # for i in range(f - 1):
    #     # n rooms left, need to reserve f - i rooms for stairways in floors left, 
    #     # need to reserve (f - i - 1) rooms so that no floor is just a stairway
    #     r_num = random.randint(1, n - (f - i) - (f - i - 1)) 
    #     possible_rooms += [random.sample(ROOMS, r_num)]
    #     possible_rooms[i].append("stairway")
    #     n -= r_num + 1

    #     # Shuffle chosen rooms
    #     random.shuffle(possible_rooms[i])

    # possible_rooms += [random.sample(ROOMS, n - 1)]
    # possible_rooms[-1].append("stairway")
    # random.shuffle(possible_rooms[-1])

    # print(possible_rooms)

    # Choose n unique rooms
    possible_rooms = random.sample(ROOMS, n)

    # Shuffle chosen rooms
    random.shuffle(possible_rooms)

    # BFS generation
    # TODO: Make sure start room is not locked
    start = possible_rooms.pop()

    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None

    print('start', start)

    locked = {}

    while not frontier.empty():
        current = frontier.get()

        if current == "stairway":
            pass

        # Reserve one travel direction for room that current came from
        dec = 1 if came_from[current] else 0

        # Adjacent rooms (which rooms you can travel to from current room)
        lower_bound = 0 if not (frontier.empty() and len(possible_rooms)) else 1
        upper_bound = len(possible_rooms) if len(possible_rooms) < 4 - dec else 4 - dec
        adj_rooms = [possible_rooms.pop() for i in range(random.randint(lower_bound, upper_bound))]
        
        # Pad adj_rooms with empty strings if no room to travel in that direction
        while len(adj_rooms) < 4 - bool(came_from[current]):
            adj_rooms.insert(random.randint(0, 4), '')

        # Insert as an adj_room the room player came from so that the graph is bidirecitonal
        if came_from[current]:
            i, cf_room = came_from[current]
            # Determine opposite direction: 0 -> 2, 1 -> 3, 2 -> 0, 3 -> 1
            i = i + 2 if i < 2 else i - 2
            adj_rooms.insert(i, cf_room)

        for idx, next in enumerate(adj_rooms):
            if next == "": continue
            if next not in came_from:
                frontier.put(next)
                # idx corresponds to what direction coming from, 0 is north, 1 is east, 2 is south, 3 is west
                came_from[next] = (idx, current)
        
        # TODO: Place items in current room based on context

        rooms[current] = { "directions": adj_rooms, "items": [] }

    # Randomly place rest of items
    items = list(items.keys())
    random.shuffle(items)
    for i in items:
        rand_room = random.choice(list(rooms.keys()))
        rooms[rand_room]['items'].append(i)

    # A* to determine path to key. This is to make sure key (note 4) is reachable

    # Randomly choose locked rooms that is not in the path of the key

    with open_w('./content/rooms.json') as f:
        json.dump(rooms, f)

def generate_world(i=5, r=10, f=4):
    """Generates the world environment (items, rooms)
    
    Args:
        i (int): Number of unique items to generate
        r (int): Number of unique rooms to generate
    """
    if f > r:
        raise ValueError("Number of floors cannot be less than the number of rooms to generate")

    items = generate_items(i)
    generate_rooms(r, f, items)
    
def generate_notes():
    """
    Generates the notes placed in the world used to progress the plot line
    """
    # TODO: Add variations of core notes, and generate from list
    path = './content/notes.json'
    Notes.setup(path)
    note_text = "I’ve finally arrived at [Mansion Name]. I can’t wait to restart my research once again. I think I may finally have the means to complete my grand vision. Only time will tell…"
    note = Notes('Starting my research', 1, note_text)
    note.to_json(path)

    note_text = "I have made a recent breakthrough. Manipulating atoms may not be as difficult as previously expected. I can likely use this to create any element that I desire. *Some fancy formulas that you don’t understand are also written*"
    note = Notes('Breakthrough!', 92, note_text)
    note.to_json(path)

    note_text = "In recent days, I have made more and more breakthroughs, but I feel that someone has been watching me. I will continue to be wary of those around me."
    note = Notes('Someone is Watching…', 141, note_text)
    note.to_json(path)

    note_text = "Someone has found me. I am writing this note in desperation. If you find it, I am likely dead. Find my murderer. Protect my research. *The writing looks rushed and there is blood on the note. A key is taped to the back.*"
    note = Notes('Someone is out to get me…', 169, note_text)
    note.to_json(path)


def mkdir(path):
    """
    Makes directory at given path if not already existing
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def open_w(path):
    """
    Open "path" for writing, creating any parent directories as needed.
    """
    mkdir(os.path.dirname(path))
    return open(path, 'w')

if __name__ == "__main__":
    generate_notes()
    write_attributes()
    generate_world()