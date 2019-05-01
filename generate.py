"""
Generates JSON file that composes the game interactions
"""

import json, os, errno, random
from queue import *
from collections import defaultdict
from world import ATTRIBUTES, OBJECT_TYPES, ITEMS, ROOMS

def write_attributes():
    """
    Writes item attributes to /content/attributes.json 
    """
    with open_w('content/attritubes.json') as f:
        json.dump(ATTRIBUTES, f)


def generate_items(n):
    """Generates n items and writes to /content/items.json
    
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
        print(item, properties)
        for p in properties:
            # TODO: Add random contextual attribute
            attributes = []
            if p in OBJECT_TYPES.keys():
                attributes += OBJECT_TYPES[p]
            elif p in ATTRIBUTES:
                attributes.append(p)

            items[item] = attributes

    # Write items to a json file
    with open_w('content/items.json') as f:
        json.dump(items, f)
    
    return items


def generate_rooms(n, items):
    """Generates n rooms and writes to /content/rooms.json 
    
    Rooms describe what items are in it and what other rooms (directions) are possible to navigate to.

    Args:
        n (int): Number of unique rooms to generate
        items (dict): Dictionary of possible unique items in the world
    """
    rooms = defaultdict(dict)

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

    while not frontier.empty():
        current = frontier.get()

        # Decrement variable
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
        
        # TODO: Make items placed in rooms contexual, Not enough items? 
        item = random.sample(list(items.keys()), random.randint(1, len(items)-1))
        print(item)
        rooms[current] = { "directions": adj_rooms, "items": item }

    with open_w('content/rooms.json') as f:
        json.dump(rooms, f)

def generate_world(i=5, r=3):
    """Generates the world environment (items, rooms)
    
    Args:
        i (int): Number of unique items to generate
        r (int): Number of unique rooms to generate
    """
    items = generate_items(i)
    generate_rooms(r, items)
    

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
    write_attributes()
    generate_world(4, 6)