# midi.py

"""
util for tranforming and saving midi files
"""
import os

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

# uploads specified file to s3
# returns url
def push_to_s3(fileName):
	conn = tinys3.Connection(os.environ["S3_ACCESS_KEY"],os.environ["S3_SECRET_ACCESS_KEY"],tls=True)
	f = open(fileName,'rb')
	conn.upload(fileName,f,os.environ["S3_BUCKET_NAME"])
	return os.environ["S3_BUCKET_URL"] + "/" + fileName
