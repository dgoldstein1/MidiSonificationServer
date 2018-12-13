# midi.py

"""
util for tranforming and saving midi files
"""
import os
import datetime
from statistics import stdev 

# midi utils
from miditime.miditime import MIDITime

# s3 utils
import boto
from boto.s3.key import Key


def mag_to_pitch_tuned(magnitude, mymidi, min, max):
    # Where does this data point sit in the domain of your data? (I.E. the min magnitude is 3, the max in 5.6). In this case the optional 'True' means the scale is reversed, so the highest value will return the lowest percentage.
    # scale_pct = mymidi.linear_scale_pct(min, max, magnitude)

    # Another option: Linear scale, reverse order
    # scale_pct = mymidi.linear_scale_pct(3, 5.7, magnitude, True)

    # Another option: Logarithmic scale, reverse order
    scale_pct = mymidi.log_scale_pct(min, max, magnitude)

    # Pick a range of notes. This allows you to play in a key.
    c_major = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

    #Find the note that matches your data point
    note = mymidi.scale_to_note(scale_pct, c_major)

    #Translate that note to a MIDI pitch
    midi_pitch = mymidi.note_to_midi_pitch(note)


    return midi_pitch

# saves midi file locally
def create_midi_file(fileName, bpm = 120, data = [], outputRange=2):
	# first normalize data by deviation
	magnitudeMin = min([d[1] for d in data])
	magnitudeMax = max([d[1] for d in data])
	magnitudeRange = magnitudeMax - magnitudeMin

	# (bpm, filename, sec per year, base octave,octave range)
	mymidi = MIDITime(120, fileName, 5, 5, outputRange)
	# add {'event_date': , 'magnitude': }

	note_list = []

	# tie everything to 60 beats
	# [time, pitch, velocity, duration]
	numberOfBeats = int(os.environ["SONG_BEAT_LENGTH"])
	beatsPerDataPoint = float(numberOfBeats) / len(data)
	i = 0
	for d in data:
	    note_list.append([
	        i * beatsPerDataPoint, # beat
	        mag_to_pitch_tuned(d[1], mymidi, magnitudeMin, magnitudeMax),
	        100,  # velocity
	        i * beatsPerDataPoint  # duration, in beats
	    ])
	    i=i+1

	# Add a track with those notes
	mymidi.add_track(note_list)

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