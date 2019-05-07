class Event():
    # Events are triggered by interacting with an item, TODO: event triggered by room?
    def __init__(self, trigger, text, goal=None, reaction=None, exit=None):
        self.trigger = trigger
        self.text = text
        self.goal = goal
        self.reaction = reaction
        self.exit = exit
