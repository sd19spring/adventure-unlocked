import pickle
import time
import os
import subprocess
from random import choice, randint

from psonic import *

class Song:
    def __init__(self, bpm=-1, notes=-1, beats=-1, volumes = -1):
        # selects sound file to play music off of
        self.SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")
        self.SAMPLE_FILE = os.path.join(self.SAMPLES_DIR, "bass_D2.wav")
        self.SAMPLE_NOTE = D2

        # sets tempo of song
        if bpm == -1:
            self.new_tempo()
        else:
            self.bpm = bpm

        # creates list of notes to select from
        if notes == -1:
            notes = [40, 43, 45, 46, 47, 50, 52, 55, 57, 
               58, 59, 62, 64, 67, 69, 70, 71, 74, 76]
        self.notes = notes
        
        # creates list of beat lengths to select from
        if beats == -1:
            beats = [2, 1, 1/2, 1/4, 1/2, 1, 1]
        self.beats = beats

        # creates list of volumes to select from
        if volumes == -1:
            volumes = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 3, 3, 3, 3, 2.5, 2.5, 3.5, 3.5]
        self.volumes = volumes

        # holds phrases that are currently part of the song
        self.phrases = []

        # initializes song by opening sonicpi and generating phrases
        self.open_sonicpi()
        self.generate_phrases()
        time.sleep(10)

    def open_sonicpi(self,name='sonic-pi'):
        """
        Opens sonicpi using subprocesses

        returns whether or not sonic pi is open
        """
        # tries to open sonic pi
        try:
            self.sonic = subprocess.Popen([name])
            self.sonic_is_open = True
        # catches case where sonic pi is not downloaded
        except OSError:
            print('Ahhhhh! Please install Sonic Pi.')
            self.sonic_is_open = False

    def close_sonicpi(self):
        """Closes sonicpi using subprocesses"""
        # tries to kill sonicpi
        try:
            self.sonic.kill()
        # catches case where sonicpi has not yet been opened
        except AttributeError:
            print('Sonic Pi has not yet been opened.')
        
    def new_tempo(self, min_bpm=70, max_bpm=140):
        """Updates song's tempo"""
        self.bpm = choice(list(range(min_bpm,max_bpm,1)))

    def play_note(self, note, beats, amp):
        """Play note for `beats` beats. Return when done."""
        # `note` is this many half-steps higher than the sampled note
        half_steps = note - self.SAMPLE_NOTE
        # An octave higher is twice the frequency. There are twelve half-steps per
        # octave. Ergo, each half step is a twelth root of 2 (in equal temperament).
        rate = (2 ** (1 / 12)) ** half_steps
        assert os.path.exists(self.SAMPLE_FILE)
        # Turn sample into an absolute path, since Sonic Pi is executing from a
        # different working directory.
        sample(os.path.realpath(self.SAMPLE_FILE), rate=rate, amp=amp)
        sleep(beats * 60 / self.bpm)

    def next_beat(self, prev_length):
        """
        picks a beat value based on the previous note's length

        this function puts more weight on certain related beats
        
        returns a beat length
        """
        if prev_length == (self.beats[2] or self.beats[3]):
            return choice((self.beats + [prev_length]*3)) 
        else:
            return choice((self.beats + [self.beats[2]]*2 + [self.beats[3]]))

    def next_note(self, prev_note):
        """
        selects a note based on the previous note

        gives higher likelihood for a nearby note to be played
        (1st or third)

        returns note
        """

        prev_index = self.notes.index((prev_note))

        if prev_index < 6:
            return choice(self.notes + [self.notes[prev_index+1]]*8
                                    + [self.notes[prev_index+3]]*5
                                    + [self.notes[prev_index+5]]*1)
        elif prev_index > len(self.notes)-8:
            return choice(self.notes + [self.notes[prev_index-1]]*8
                                    + [self.notes[prev_index-3]]*5
                                    + [self.notes[prev_index-5]]*1)
        if randint(0,1) == 1:
            return choice(self.notes + [self.notes[prev_index-1]]*8
                                    + [self.notes[prev_index-3]]*5
                                    + [self.notes[prev_index-5]]*1)
        return choice(self.notes + [self.notes[prev_index+1]]*8
                                + [self.notes[prev_index+3]]*5
                                + [self.notes[prev_index+5]]*1)
    
    def note_volume(self, prev_volume):
        """
        generates volume of note based on the volume of a previous note

        returns volume
        """
        return choice(self.volumes + [prev_volume]*4
                                   + [prev_volume + .5]*2
                                   + [prev_volume - .5]*2)

    def generate_phrase(self, beats=4, note=-1):
        """
        generates a random phrase with beats beats that starts on
        start_note with length of start_beat. Total phrase length
        will equal to total beats

        returns a random phrase
        """
        if note == -1:
            note = choice(self.notes)
        
        phrase = [(note, choice(self.beats),
                 choice(self.volumes))]
        total_beats = phrase[0][1]

        i = 1
        while total_beats < beats:
            phrase.append((self.next_note(phrase[i-1][0]),
                         self.next_beat(phrase[i-1][1]),
                         self.note_volume(phrase[i-1][2])))
            total_beats += phrase[i][1]
            i+=1
        self.phrases.append(phrase)

    def generate_phrases(self, n=3):
        """
        generates a list of n phrases where each phrase
        is beats beats long
        
        returns a list of n phrases
        """
        for i in range(n):
            self.generate_phrase(choice([4,6,8]))

    def play_phrase(self):
        """
        plays phrase in phrases
        """
        phrase = choice(self.phrases)
        for note in phrase:
            self.play_note(note[0], note[1], note[2])

    def update_song(self):
        self.phrases = []
        self.generate_phrases
        self.new_tempo


if __name__ == "__main__":
    song = Song()

    game = True
    text = 'asdf'
    temp = text

    while song.sonic_is_open and game:
        if temp != text:
            song.update_song()
        song.play_phrase()
        temp = text

    song.close_sonicpi()
