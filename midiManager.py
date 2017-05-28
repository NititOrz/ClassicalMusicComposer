from mido import Message, MidiFile, MidiTrack, MetaMessage

class MidiMananger(object):
	"""docstring for MidiMananger"""
	def __init__(self):
		pass

	def creatMidiSong(self, song):
		mid = MidiFile()
		track = MidiTrack()
		mid.tracks.append(track)
		for x in song:
			# print(x)
			time = int(x[2])
			note = int(x[1])
			note_type = x[0]
			# print(type(time))
			track.append(Message(note_type, channel=0, note=note, velocity=60, time=time))

		mid.save('SONG.mid')

# 	track.append(Message('note_on', channel=0, note=60, velocity=61, time=60))