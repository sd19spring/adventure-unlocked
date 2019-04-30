"""
Generates JSON file that composes the game interactions
"""

import json, os, errno, random
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
    room_rand = random.sample(ROOMS, n)

    # TODO: Make rooms direction similar across all rooms to navigate. Random walk generation
    for room in room_rand:
        # Choose n-1 or 4 other rooms to navigate to
        other_rooms = random.sample(list(filter(lambda r: r != room, room_rand)), n-1 if n-1 < 4 else 4)

        # TODO: Make items placed in rooms contexual, Not enough items? 
        item = random.sample(list(items.keys()), random.randint(0, len(items)-1))
        rooms[room] = { "directions": other_rooms, "items": item }

    with open_w('content/rooms.json') as f:
        json.dump(rooms, f)

def generate_world(i, r):
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
    generate_world(5, 3)