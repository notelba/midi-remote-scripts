# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SessionSnap.py
# Compiled at: 2017-03-07 13:28:53
import Live
LSQ = Live.Song.Quantization

class SessionSnap(object):
    """ SessionSnap is a simple object that stores/recalls the playing state of tracks
    in session. """

    def __init__(self, song):
        self._song = song
        self._data = {}

    def disconnect(self):
        self._song = None
        self._data = None
        return

    @property
    def data(self):
        """ Returns stored data as a dict that can be saved to file/clip. """
        return {k.name:v for k, v in self._data.iteritems()}

    def rebuild(self, data):
        """ Rebuilds snap data based on the given data dict. """
        self._data = {}
        if data is not None:
            for k, v in data.iteritems():
                for track in self._song.tracks:
                    if k == track.name:
                        self._data[track] = v
                        break

        return

    def store(self):
        """ Store the current playing state of all tracks. """
        self._data = {}
        for track in self._song.tracks:
            self._data[track] = track.playing_slot_index

    def recall(self, quantized=True):
        """ Recall the stored playing state of all tracks with or without
        quantization. """
        if self._data:
            qntz = LSQ.q_no_q
            if quantized:
                qntz = self._song.clip_trigger_quantization
            num_scenes = len(self._song.scenes)
            for track, slot_index in self._data.iteritems():
                if track in self._song.tracks and slot_index < num_scenes:
                    if slot_index < 0:
                        track.stop_all_clips(quantized)
                    elif track.clip_slots[slot_index].has_clip:
                        track.clip_slots[slot_index].fire(launch_quantization=qntz)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SessionSnap.pyc
