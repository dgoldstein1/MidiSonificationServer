# midi.py

"""
util for tranforming and saving midi files
"""
import os
import datetime

# midi utils
from miditime.miditime import MIDITime

# s3 utils
import boto
from boto.s3.key import Key



# saves midi file locally
def create_midi_file(fileName, bpm = 120, data = [], outputRange=2, key="C"):
	# (bpm, filename, sec per year, base octave,octave range)
	mymidi = MIDITime(120, fileName, 5, 5, outputRange)
	# add {'event_date': , 'magnitude': }
	transformedData = [{'days_since_epoch': mymidi.days_since_epoch(datetime.datetime.fromtimestamp(d[0] / 1e3)), 'magnitude': d[1]} for d in data]

	mymidi.save_midi()

# uploads specified file to s3
# returns url
def push_to_s3(fileName):
	conn = boto.connect_s3(os.environ["S3_ACCESS_KEY"], os.environ["S3_SECRET_ACCESS_KEY"])
	bucket = conn.get_bucket(os.environ["S3_BUCKET_NAME"], validate=True)
	k = Key(bucket)
	k.key = os.environ["S3_FOLDER_PATH"] + "/" + fileName
	k.set_contents_from_filename(fileName)
	k.set_acl('public-read')
	return os.environ["S3_BUCKET_URL"] + "/" + os.environ["S3_FOLDER_PATH"] + "/" + fileName