# midi.py

"""
util for tranforming and saving midi files
"""
import os

# midi utils
from miditime.miditime import MIDITime

# s3 utils
import boto
from boto.s3.key import Key



# saves midi file locally
def save_midi_file(fileName, bpm = 200, data = []):
	# first transform data

	
	mymidi = MIDITime(200, fileName)
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