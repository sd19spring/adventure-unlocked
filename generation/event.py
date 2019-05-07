import json, jsonable

class Event(jsonable.Jsonable):
    """
    This class is used to represent the notes used to progress the story. It reads and writes these notes to a json file. Inherits from
    jsonable.
    """

    # Events are triggered by interacting with an item, TODO: event triggered by room?
    def __init__(self, trigger, text='Something spooky is going on', goal=None, reaction=None, exit_trigger=None):
        self.trigger = trigger
        self.text = text
        self.goal = goal
        self.reaction = reaction
        self.exit_trigger = exit_trigger

    def to_json(self, path):
        e = {
            'text': self.text,
            'goal': self.goal,
            'reaction': self.reaction,
            'exit_trigger': self.exit_trigger
        }

        super().to_json(path, self.trigger, e)
