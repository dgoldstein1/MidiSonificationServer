# midi.py

"""
util for tranforming and saving midi files
"""
# midi utils
from miditime.miditime import MIDITime

# s3 utils
import tinys3

def save_midi_file(fileName, bpm = 200, data = []):
	mymidi = MIDITime(200, fileName)
	midinotes = []
	for i in xrange(1,10):
		midinotes.append([i + .5, 50 + i, 100, 0.5])
		midinotes.append([i + .2, 40 + i, 100, 0.5])
		midinotes.append([i, 50 - i, 200, 1])
	mymidi.add_track(midinotes)
	mymidi.save_midi()

def push_to_s3(fileName):
	print "uploading '" + fileName + "'"
	conn = tinys3.Connection('AKIAJH4M5UKXPA4QJ6OQ','11/5NWgXiEqJUKgf4pjGgzF8M/MJrD715RZJV9of',tls=True)
	f = open(fileName,'rb')
	conn.upload(fileName,f,'decipher-hackathon-2018')
	print "https://s3.amazonaws.com/decipher-hackathon-2018/" + fileName
