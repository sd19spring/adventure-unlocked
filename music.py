from midiutil import MIDIFile
import os
import pickle
import random

def scales(file_name='scales.txt'):
    
    if not os.path.isfile(file_name):
        scale_library = {'major' : (0,2,4,5,7,9,11,12),
                         'minor' : (0,2,3,4,7,8,10,12),}

        with open(file_name, "wb") as output_file:
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
    def __init__(self, degrees, tempo, time_signature=4/4, noteprobs=[2,7,5,3,4,3,2,4,1], beatprobs=[2, 6, 9, 4, 2]):
        scales()

        self.noteprobs = noteprobs
        self.beatprobs = beatprobs

        self.timesig = time_signature

        self.degrees  = degrees

        beats = [2, 1, 1/2,1/4,1/8]
        self.beatprobs = []
        for i in range(len(beats)):
            self.beatprobs = self.beatprobs + ([beats[i]]*beatprobs[i]) 

        self.track    = 0
        self.channel  = 0
        self.time     = 0       # In beats
        self.duration = 1       # In beats
        self.tempo = tempo      # In BPM
        # volume is from 0-127, as per the MIDI standard  

        self.MyMIDI = MIDIFile(1) 

        self.write_midi() 

    def beat_select(self, measures):
        probs = self.beatprobs
        beatlist = [random.choice(probs)]
        totaltime = beatlist[0]
        count = 0

        while totaltime < (measures*self.timesig):
            temp = random.choice(probs)

            if not (totaltime+temp) > (measures*self.timesig):
                beatlist = beatlist + [temp]
                totaltime = totaltime + temp
        
        return beatlist

    def build_notelist(self, note):
        notes = self.degrees
        noteprobs = self.noteprobs
        probs = []
        
        pos = notes.index(note)
        for i in range(len(notes)):
            if i > pos-len(noteprobs) and i < pos:
                probs = probs + ([notes[i]]*noteprobs[pos-i])
            elif i >= pos and i < pos+len(noteprobs):
                probs = probs + ([notes[i]]*noteprobs[i-pos])
        return probs

    def note_select(self, numnotes):
        notes = self.degrees
        notelist = [random.choice(notes)]
        for i in range(numnotes):
            temp_probs = self.build_notelist(notelist[i])
            notelist.append(random.choice(temp_probs))
        return notelist

    def export(self, file_name="song"):
        """
        Exports file with given file_name
        """
        with open(file_name+".mid", "wb") as output_file:
            self.MyMIDI.writeFile(output_file)

    def write_midi(self):
        beats = self.beat_select(100)
        notes = self.note_select(len(beats))

        self.MyMIDI.addTempo(self.track, self.time, self.tempo) 

        curtime = 0
        for i in range(len(beats)):
            curtime = curtime + beats[i]
            self.MyMIDI.addNote(self.track, self.channel, 
                                notes[i], curtime, beats[i], 100)

        self.export()


class Happy(Song):
    def __init__(self, degrees=0, key=60, tempo=0):
        # sets key range to three octaves
        scales()
        if not degrees:
            with open('scales.txt', 'rb') as myfile:
                scale = pickle.load(myfile)['major']
            
            degrees = build_scale(scale, key)
        
        if not tempo:
            tempo = random.randint(110,150)

        Song.__init__(self, degrees, tempo)


if __name__ == "__main__":
    test = Happy()
