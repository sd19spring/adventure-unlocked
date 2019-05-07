# Structures the Notes item in game
# Generates these notes and writes to file
# And interprets JSON files and reconstruct them as Notes objects
import json, pprint

class Notes():
    # Class variable counting number of notes created
    notes_num = 0

    def __init__(self, title, day, text, events=None):
        self.title = title
        self.day = day
        self.text = text
        self.events = events
        Notes.notes_num += 1
    
    def to_json(self, path):
        note = {
            'title': self.title,
            'day': self.day,
            'text': self.text,
            'events': self.events
        }

        with open(path, 'r+') as f:
            data = json.load(f)
            data['note ' + str(Notes.notes_num)] = note
            f.seek(0) 
            json.dump(data, f)
    
    @staticmethod
    def from_json(path):
        with open(path, 'r') as f:
            data = f.read().replace('"', '\"')
            note = json.loads(data)
        return note

    @staticmethod
    def setup(path):
        with open(path, 'w') as f:
            json.dump({}, f)

if __name__ == "__main__":
    path = './content/notes.json'
    Notes.setup(path)
    note1_text = "I’ve finally arrived at [Mansion Name]. I can’t wait to restart my research once again. I think I may finally have the means to complete my grand vision. Only time will tell…"
    note1 = Notes('Starting my research', 1, note1_text)
    note1.to_json(path)

    note2_text = "I have made a recent breakthrough. Manipulating atoms may not be as difficult as previously expected. I can likely use this to create any element that I desire. *Some fancy formulas that you don’t understand are also written*"
    note1 = Notes('Breakthrough!', 92, note2_text)
    note1.to_json(path)

    pprint.pprint(Notes.from_json(path))
