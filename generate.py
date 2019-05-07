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
            items[i] = ['event', 'portable', 'readable']
        else:
            items[i] = ['portable', 'readable']

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

def generate_world(i=len(ITEMS), r=len(ROOMS), f=4):
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
    text = ["I’ve finally arrived at the mansion. I can’t wait to restart my research once again. They just didn’t understand my work. Stupid … stupid. I’ll show them, and this time I’m so close. I think I may finally have everything I need. Only time will tell…",
    "I heard a knock on the front door today. The only thing was that when I went to check, no one was there. It’s probably just my imagination. Also things are looking good, and the experiment seems to be successful. I just need time to examine the results and confirm my hypothesis.",
    "It’s been a sad three days. Experiment 4 that I thought proved to be a success ended up slowly decaying, and now I have to find somewhere to dispose of it’s carcass. Maybe all of this is not worth it. The academy was right.",
    "AHHHHHHHHHHHHHHHHHHH!!!! AHHHHHHHHHHH!", "I miss her so much. Sometimes at night, I hallucinate and see her standing outside my window and just watching me. But I know that’s not possible. It’s already been five years since the accident. I just miss her touch so much. She always understood me and my work. Unlike those filthy pigs at the academy.",
    "I somehow lost Experiment 13. I’m sure last night I strapped it back in, double checking that it was restrained. However, when I went to check today, it wasn’t there anymore. Very strange. What’s even more confusing is it seems that the chains were cleanly cut, but that’s not possible.",
    "I’ve made a breakthrough! I was just going about it the wrong way. Hehehe, and they said it couldn’t be done. I’m finally so close. *Some fancy formulas that you don’t understand are also written below*",
    "Happy birthday to me. Happy birthday to me. Happy birthday to meeeeee!", "Someone must have remembered my birthday! I went outside today for the first time in weeks and found Experiment 13’s collar in the mailbox. Maybe it was the milkman.",
    "I heard another knock on the door today. And once again when I went to check who it was, there wasn’t anybody there. I looked around and checked around the mansion, but still found nothing. I think I’ve been spending too much time in the lab. Doctor did say to get Vitamin D … or was it C? Which one gave you scurvy? I can’t remember.",
    "Molly appeared in my dream. She was so vivid and realistic, and she came so close to me I could almost count each individual mole on her neck that formed a star. Her silky smooth blonde hair seems just as soft as I remember. If only I could feel it against my skin again, oh there’s nothing that I wouldn’t do.",
    "Molly appeared in my dream once again. It’s two nights in a row, and this time there were two of her. I was so ecstatic I tried running up to both of her, in the dream of course, and I ended up hitting my toe on the nightstand. What confuses me is that I woke up today with a big welt on the same toe I stubbed in my dream. My sleepwalking must be getting worse.",
    "The doctor prescribed me some medication for my toe. For some reason, every night since that dream, when I wake up in the morning the welt seems to get bigger and hurt even more. So I went to the doctor and he gave me some percocets. That dream made me miss Molly even more. If only I could have an infinite number of Molly’s to be with me and understand me. What was I talking about? Oh yeah, percocets. But Molly... percocets.",
    "In recent days, I have made more and more breakthroughs, but I feel that someone has been watching me. Whenever I’m in the lab and working on an experiment, I get a feeling that someone is looking over my shoulder. I’m worried it’s those dirty pigs from the academy. They must be after my research especially now that I’m so close to succeeding. But I’ll never let them get a hold of this. Not on my life.",
    "Someone is after me. I am writing this note in desperation. If you find it, I am likely dead. Whoever reads this, protect my research. That’s all that I care abou- *The writing looks rushed and there is blood on the note. This seems to be the last note.*"]
    titles = ['Starting my research', 'A knock', 'Failure', '[Untitled]', 'Molly', 'Experiment 13', 'Breakthrough!', 'Happy day', 'A present', 'Another one', 'A dream', 'Some pains', 'Medication', 'Someone is watching…', 'Someone is out to get me…']
    days = [1, 7, 13, 30, 35, 57, 92, 100, 101, 118, 119, 120, 125, 141, 169]

    for i in range(len(days)):
        note = Notes(titles[i], days[i], text[i])
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
    mkdir('./content')
    generate_notes()
    write_attributes()
    generate_world()