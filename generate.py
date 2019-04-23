"""
Generates JSON file that composes the game interactions
"""

import json, os, errno, random
from collections import defaultdict
from world import ATTRIBUTES, OBJECT_TYPES, ITEMS, ROOMS

def write_attributes():
    """
    Writes attributes to file
    """

def generate_items(n):
    """
    Generates n items to items.json, describing the item attributes and actions
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
            print(attributes)
            for a in attributes:
                items[item][a] = ATTRIBUTES[a]

    # Write items to a json file
    with open_w('content/items.json') as f:
        json.dump(items, f)


def generate_rooms(n):
    """
    Generates n rooms to rooms.json, describing the items in room and the navigation
    """
    rooms = defaultdict(dict)

    # Choose n unique rooms
    room_rand = random.sample(ROOMS, n)

    # TODO: Make rooms direction similar across all rooms to navigate
    for room in room_rand:
        # Choose n-1 or 4 other rooms to navigate to
        other_rooms = random.sample(list(filter(lambda r: r != room, room_rand)), n-1 if n-1 < 4 else 4)

        # TODO: Make items picked contexual
        item = random.sample(list(ITEMS.keys()), random.randint(0, len(ITEMS)-1))
        rooms[room] = { "directions": other_rooms, "items": item }

    with open_w('content/rooms.json') as f:
        json.dump(rooms, f)


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
    generate_items(5)
    generate_rooms(3)