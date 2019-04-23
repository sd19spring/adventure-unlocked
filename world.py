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
        "reactions": ["health increase"]
    },
    "openable": {
        "prompts": [["open",  "open up"]],
        "reactions": ["state open"]
    },
    "withstand": { # Can have portable objects placed onto or into it
        "reactons": ["supports portable"]
    },
    "usable": {
        "propmts": [["use"]],
        "reactions": ["use _"]
    },
    "slippery": {
        "reactions": ["drop _"]
    },
    "poisonous": {
        "reactions": ["health decrease"]
    },
    "heavy": {
        "reactions": ["movement_speed decrease"]
    }
}
OBJECT_TYPES = {
    "container": ["openable", "withstand"], # implements opeanble, withstand
    "supporter": ["withstand"],
    "food": ["portable", "edible"],
    "weapon": ["portable", "usable"]
}
ITEMS = {
    "lamp": ["portable"],
    "apple": ["food"], # extends portable
    "chest": ["container"],
    "desk": ["supporter"],
    "sword": ["weapon"]
}
ROOMS = ["kitchen", "living room", "bedroom", "balcony", "stairway", "hallway"]