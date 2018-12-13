# midi.py

"""
util for tranforming and saving midi files
"""
from miditime.miditime import MIDITime

def save_midi_file(data = []):
	mymidi = MIDITime(200, 'myfile.mid')
	midinotes = []
	for i in xrange(1,10):
		midinotes.append([i + .5, 50 + i, 100, 0.5])
		midinotes.append([i + .2, 40 + i, 100, 0.5])
		midinotes.append([i, 50 - i, 200, 1])
	mymidi.add_track(midinotes)
	mymidi.save_midi()