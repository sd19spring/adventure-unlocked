import json, pprint
from generation import jsonable

class Notes(jsonable.Jsonable):
    """
    This class is used to represent the notes used to progress the story. It reads and writes these notes to a json file. Inherits from
    jsonable.
    """

    # Class variable counting number of notes created
    notes_num = 0

    def __init__(self, title, day, text, event=None):
        self.title = title
        self.day = day
        self.text = text
        self.event = event
        Notes.notes_num += 1
    
    def to_json(self, path):
        note = {
            'title': self.title,
            'day': self.day,
            'text': self.text,
            'event': self.event
        }

        super().to_json(path, 'note ' + str(Notes.notes_num), note)

if __name__ == "__main__":
    path = '../content/notes.json'
    Notes.setup(path)
    note1_text = "I’ve finally arrived at [Mansion Name]. I can’t wait to restart my research once again. I think I may finally have the means to complete my grand vision. Only time will tell…"
    note1 = Notes('Starting my research', 1, note1_text)
    note1.to_json(path)

    note2_text = "I have made a recent breakthrough. Manipulating atoms may not be as difficult as previously expected. I can likely use this to create any element that I desire. *Some fancy formulas that you don’t understand are also written*"
    note1 = Notes('Breakthrough!', 92, note2_text)
    note1.to_json(path)

    pprint.pprint(Notes.from_json(path))
