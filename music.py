from midiutil import MIDIFile
from midi2audio import FluidSynth
import os
import pickle
import random

"""Synthesizes a blues solo algorithmically."""

import atexit
import os
from random import choice, randint
import time

from psonic import *

# The sample directory is relative to this source file's directory.
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")

SAMPLE_FILE = os.path.join(SAMPLES_DIR, "bass_D2.wav")
SAMPLE_NOTE = D2  # the sample file plays at this pitch


def play_note(note, beats=1, bpm=60, amp=3):
    """Play note for `beats` beats. Return when done."""
    # `note` is this many half-steps higher than the sampled note
    half_steps = note - SAMPLE_NOTE
    # An octave higher is twice the frequency. There are twelve half-steps per
    # octave. Ergo, each half step is a twelth root of 2 (in equal temperament).
    rate = (2 ** (1 / 12)) ** half_steps
    assert os.path.exists(SAMPLE_FILE)
    # Turn sample into an absolute path, since Sonic Pi is executing from a
    # different working directory.
    sample(os.path.realpath(SAMPLE_FILE), rate=rate, amp=amp)
    sleep(beats * 60 / bpm)


def stop():
    """Stop all tracks."""
    msg = osc_message_builder.OscMessageBuilder(address='/stop-all-jobs')
    msg.add_arg('SONIC_PI_PYTHON')
    msg = msg.build()
    synth_server.client.send(msg)

# stop all tracks when the program exits normally or is interrupted
atexit.register(stop)

# These are the piano key numbers for a 3-octave blues scale in A.
# See: http://en.wikipedia.org/wiki/Blues_scale
BLUES_SCALE = [40, 43, 45, 46, 47, 50, 52, 55, 57, 
               58, 59, 62, 64, 67, 69, 70, 71, 74, 76]
BEATS = [1/4, 1/8, 1/16, 1/8, 1/8, 1/16] #maybe add dotted notes later
BEATS_PER_MINUTE = 20
VOLUME = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 3, 3, 3, 3, 2.5, 2.5, 3.5, 3.5]

def next_beat(prev_length):
    """
    picks a beat value based on the previous note's length

    this function puts more weight on certain related beats
    
    returns a beat length
    """
    if prev_length == (BEATS[2] or BEATS[3]):
        return choice((BEATS + [prev_length]*3)) 
    else:
        return choice((BEATS + [BEATS[2]]*2 + [BEATS[3]]))

def next_note(prev_note):
    """
    selects a note based on the previous note

    gives higher likelihood for a nearby note to be played
    (1st or third)

    returns note
    """

    prev_index = BLUES_SCALE.index((prev_note))

    if prev_index < 6:
        return choice(BLUES_SCALE + [BLUES_SCALE[prev_index+1]]*8
                                  + [BLUES_SCALE[prev_index+3]]*5
                                  + [BLUES_SCALE[prev_index+5]]*1)
    elif prev_index > len(BLUES_SCALE)-8:
        return choice(BLUES_SCALE + [BLUES_SCALE[prev_index-1]]*8
                                  + [BLUES_SCALE[prev_index-3]]*5
                                  + [BLUES_SCALE[prev_index-5]]*1)
    if randint(0,1) == 1:
        return choice(BLUES_SCALE + [BLUES_SCALE[prev_index-1]]*8
                                  + [BLUES_SCALE[prev_index-3]]*5
                                  + [BLUES_SCALE[prev_index-5]]*1)
    return choice(BLUES_SCALE + [BLUES_SCALE[prev_index+1]]*8
                              + [BLUES_SCALE[prev_index+3]]*5
                              + [BLUES_SCALE[prev_index+5]]*1)
    
def note_volume(prev_volume):
    """
    generates volume of note based on the volume of a previous note

    returns volume
    """
    return choice(VOLUME + [prev_volume]*4
                         + [prev_volume + .5]*2
                         + [prev_volume - .5]*2)


def generate_lick(beats, start_note, start_beat, start_vol):
    """
    generates a random lick with n beats that starts on
    start_note with length of start_beat. Total lick length
    will equal to total beats

    returns a random lick
    """
    
    lick = [(start_note, start_beat, start_vol)]
    total_beats = start_beat

    i = 1
    while total_beats < beats:
        lick.append((next_note(lick[i-1][0]),
                     next_beat(lick[i-1][1]),
                     note_volume(lick[i-1][2])))
        total_beats += lick[i][1]
        i+=1
    print (lick)
    return lick

def generate_licks(n, beats):
    """
    generates a list of n licks where each lick
    is beats beats long
    
    returns a list of n licks
    """

    licks = []
    for _ in range(n):
        licks.append(generate_lick(beats, 
                                   choice(BLUES_SCALE), 
                                   choice(BEATS),
                                   choice(VOLUME)))
    return licks

def play_lick(lick):
    """
    plays the given lick
    """
    for note in lick:
        play_note(note[0], note[1], BEATS_PER_MINUTE, lick[2])

def play_song(licks, n):
    """
    plays licks in licks n times
    """
    for _ in range(n):
        lick = choice(licks)
        for note in lick:
            play_note(note[0], note[1], BEATS_PER_MINUTE, note[2])

def play_music():
    play_song(generate_licks(100,.5), 10)


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
    def __init__(self, degrees, tempo, time_signature=4/4, noteprobs=[1,1,1,1,1,1,1,1], beatprobs=[1,5,12,10]):
        scales()

        self.noteprobs = noteprobs
        self.beatprobs = beatprobs

        self.timesig = time_signature

        self.degrees  = degrees

        beats = [2, 1, 1/2, 1/4]
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

        # FluidSynth().play_midi('song.mid')
        # fs = FluidSynth()
        # fs.midi_to_audio('song.mid', 'output.wav')

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
    def __init__(self, degrees=0, key=60, tempo=0, time_signature=4/4, 
                 noteprobs=[2,10,12,2,12,2,0,2,0], beatprobs=[1,5,12,10]):
        # sets key range to three octaves
        scales()
        if not degrees:
            with open('scales.txt', 'rb') as myfile:
                scale = pickle.load(myfile)['major']
            
            degrees = build_scale(scale, key)
        
        if not tempo:
            tempo = random.randint(90,130)

        Song.__init__(self, degrees, tempo, time_signature, noteprobs, beatprobs)

class Sad(Song):
    def __init__(self, degrees=0, key=60, tempo=0, time_signature=4/4, 
                 noteprobs=[2,20,12,8,4,8,2,2,2], beatprobs=[1,5,12,10]):
        # sets key range to three octaves
        scales()
        if not degrees:
            with open('scales.txt', 'rb') as myfile:
                scale = pickle.load(myfile)['minor']
            
            degrees = build_scale(scale, key)
        
        if not tempo:
            tempo = random.randint(90,130)

        Song.__init__(self, degrees, tempo, time_signature, noteprobs, beatprobs)

class Disonant(Song):
    def __init__(self, degrees=0, key=60, tempo=0, time_signature=4/4, 
                 noteprobs=[2,10,12,2,6,10,3,2,3], beatprobs=[1,5,12,10]):
        # sets key range to three octaves
        scales()
        if not degrees:
            with open('scales.txt', 'rb') as myfile:
                scale = pickle.load(myfile)['minor']
            
            degrees = build_scale(scale, key)
        
        if not tempo:
            tempo = random.randint(70,100)

        Song.__init__(self, degrees, tempo, time_signature, noteprobs, beatprobs)


if __name__ == "__main__":
    test = Sad()
