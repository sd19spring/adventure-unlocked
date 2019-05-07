"""
This python file describes the world variables
"""

ATTRIBUTES = {
    "portable": {
        "prompts": [["pick up", "lift", "get", "equip"], ["put down", "drop"]],
        "reactions": ["move to inventory", "move to placeable"]
    },
    "edible": {
        "prompts": [["eat", "consume"]],
        "reactions": ["no reaction"]
    },
    "withstand": { # Can have portable objects placed onto or into it
        "reactons": ["supports portable"]
    },
    "usable": {
        "prompts": [["use"]],
        "reactions": ["use _"]
    },
    "event": {
        "reactions": ["trigger _"] # upon interacting with an item with an event, triggers the item name event to start and progress
    }
}
OBJECT_TYPES = {
    "container": ["openable", "withstand"], # implements opeanble, withstand
    "supporter": ["withstand"],
    "food": ["portable", "edible"],
    "tan_object": ["portable", "usable"],
}
ITEMS = {
    "lamp": ["portable"],
    "apple": ["food"], # extends portable
    "chest": ["container"],
    "desk": ["supporter"],
    "sword": ["tan_object"],
    "phone": ["event", "tan_object"],
    "human blood": ["event"], # TODO: Think of what triggers the event. Examine human blood maybe?
    "mirror": ["event", "tan_object"],
}
ROOMS = ["kitchen", "living room", "bedroom", "ballroom", "dining hall", "bathroom", "guest room", "closet", 
        "library", "gym", "theater", "butler's quarters", "spa", "bar", "lab", "office", "parlor", "billard room"]
OUTSIDE = ["shed", "patio", "garden", "pond", "forest", "pool"]
LOWER_FLOORS = ["wine celler", "dungeon", "batcave", "cave", "secret room", "why is it damp here", "creepy corner", "a homeless man seems to be living here"]

