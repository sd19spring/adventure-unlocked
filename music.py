from midiutil import MIDIFile
import os
import pickle
import random

# from midiutil import MIDIFile

# degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number 60 is middle C
# track    = 0
# channel  = 0
# time     = 0    # In beats
# duration = 1    # In beats
# tempo    = 60   # In BPM
# volume   = 100  # 0-127, as per the MIDI standard

# MyMIDI = MIDIFile(1)  

# MyMIDI.addTempo(track, time, tempo)

# for i, pitch in enumerate(degrees):
#     MyMIDI.addNote(track, channel, pitch, time, duration, volume)
#     time += .5

# with open("major-scale.mid", "wb") as output_file:
#     MyMIDI.writeFile(output_file)

def scales(myfile='scales.txt'):
    
    if not os.path.isfile(myfile):
        scale_library = {'major' : (0,2,4,5,7,9,11,12),
                         'minor' : (0,2,3,4,7,8,10,12),}

        with open(myfile, "wb") as output_file:
            pickle.dump(scale_library, output_file)
    
    print("STATUS: SCALES COMPILED")

def build_scale(scale, key, octaves=3):
    notes = [key]

    for octave in range(octaves):
        curkey = notes[-1]

        for interval in scale:
            notes.append(curkey+interval)

    return notes

class Song:
    def __init__(self, degrees, tempo):
        scales()

        self.degrees  = degrees
        self.track    = 0
        self.channel  = 0
        self.time     = 0       # In beats
        self.duration = 1       # In beats
        self.tempo = tempo      # In BPM
        # volume is from 0-127, as per the MIDI standard  

        self.MyMIDI = MIDIFile(1)  

        self.MyMIDI.addTempo(self.track, self.time, self.tempo) 

    def export(self, file_name = "song"):
        """
        Exports file with given file_name
        """
        with open(os.path.join(file_name,".mid"), "wb") as output_file:
            MyMIDI.writeFile(output_file)
    
class Happy(Song):
    def __init__(self, key=60, tempo=0, degrees=0):
        # sets key range to three octaves
        scales()
        if not degrees:
            with open('scales.txt', 'rb') as myfile:
                scale = pickle.load(myfile)['major']
            
            degrees = build_scale(scale, key)
        
        if not tempo:
            tempo = random.randint(110,150)

        Song.__init__(self, degrees, tempo)

    # def note_probs(self):

class Sad(Song):
    def __init__(self, key=60, tempo=0, degrees=0):
        # sets key range to three octaves
        scales()
        if not degrees:
            with open('scales.txt', 'rb') as myfile:
                scale = pickle.load(myfile)['minor']
            
            degrees = build_scale(scale, key)
        
        if not tempo:
            tempo = random.randint(100,120)

        Song.__init__(self, degrees, tempo)

    # def note_probs(self):
        
if __name__ == "__main__":
    test = Happy()
    print(len(test.degrees))