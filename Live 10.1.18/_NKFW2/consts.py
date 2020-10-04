# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\consts.py
# Compiled at: 2018-01-15 18:16:49
import Live
LSR = Live.Song.RecordingQuantization
LCG = Live.Clip.GridQuantization
LSQ = Live.Song.Quantization
try:
    import ClyphX_Pro.clyphx_pro.ClyphX_ProComponent
    HAS_CX_PRO = True
except:
    HAS_CX_PRO = False

MIDI_RANGE = xrange(128)
ZERO_DB_VALUE = 0.850000023842
PARAM_REL_STEP = 0.0078125
MAX_DR_SCROLL_POS = 28
SIMPLER_START_NOTE = 36
DEF_SEQ_CLIP_LENGTH = 8.0
NOTE_PITCH = 0
NOTE_TIME = 1
NOTE_LENGTH = 2
NOTE_VELO = 3
NOTE_MUTED = 4
NOTE_TUPLE_LENGTH = 5
NOTE_TUPLE_RANGE = xrange(NOTE_TUPLE_LENGTH)
NOTE_NAMES = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
NOTE_NAMES_WITH_FLATS = ('C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb',
                         'B')
COMPOUND_NOTE_NAMES = ('C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab',
                       'A', 'A#/Bb', 'B')
NUM_TONICS = 12
SHARP_NOTES = (1, 3, 6, 8, 10)
RESOLUTIONS = [
 2.0 / 24, 0.125, 4.0 / 24, 0.25, 8.0 / 24, 0.5, 16.0 / 24, 1.0]
NO_TRIPLET_RESOLUTIONS = [
 0.125, 0.25, 0.5, 1.0]
RESOLUTION_NAMES = ('1/32T', '1/32', '1/16T', '1/16', '1/8T', '1/8', '1/4T', '1/4')
NO_TRIPLET_RESOLUTION_NAMES = ('1/32', '1/16', '1/8', '1/4')
CLIP_GRID_RESOLUTIONS = (
 LCG.g_thirtysecond, LCG.g_thirtysecond,
 LCG.g_sixteenth, LCG.g_sixteenth,
 LCG.g_eighth, LCG.g_eighth,
 LCG.g_quarter, LCG.g_quarter)
NO_TRIPLET_CLIP_GRID_RESOLUTIONS = (
 LCG.g_thirtysecond, LCG.g_sixteenth,
 LCG.g_eighth, LCG.g_quarter)
DEFAULT_RESOLUTION_INDEX = 3
NO_TRIPLET_DEFAULT_RESOLUTION_INDEX = 1
MIN_CLIP_LOOP_LENGTH = 0.25
WARP_MODE_NAMES = {Live.Clip.WarpMode.beats: 'Beats', Live.Clip.WarpMode.tones: 'Tones', 
   Live.Clip.WarpMode.texture: 'Texture', 
   Live.Clip.WarpMode.repitch: 'Repitch', 
   Live.Clip.WarpMode.complex: 'Complex', 
   Live.Clip.WarpMode.complex_pro: 'Pro', 
   Live.Clip.WarpMode.rex: 'Rex'}
RECORD_QUANTIZE_RATES = [
 LSR.rec_q_quarter,
 LSR.rec_q_eight,
 LSR.rec_q_eight_triplet,
 LSR.rec_q_eight_eight_triplet,
 LSR.rec_q_sixtenth,
 LSR.rec_q_sixtenth_triplet,
 LSR.rec_q_sixtenth_sixtenth_triplet,
 LSR.rec_q_thirtysecond]
RECORD_QUANTIZE_NAMES = ('1/4', '1/8', '1/8T', '1/8+T', '1/16', '1/16T', '1/16+T',
                         '1/32')
GLOBAL_QUANTIZE_NAMES = ('None', '8 Bars', '4 Bars', '2 Bars', '1 Bar', '1/2', '1/2T',
                         '1/4', '1/4T', '1/8', '1/8T', '1/16', '1/16T', '1/32')
DEFAULT_CLIP_QUANTIZE_INDEX = 4
LAUNCH_QUANTIZE_RATES = [
 13, 12, 11, 10, 9, 8, 7]
NO_TRIPLET_LAUNCH_QUANTIZE_RATES = [
 13, 11, 9, 7]
LAUNCH_QUANTIZE_NAMES = ('1/32', '1/16T', '1/16', '1/8T', '1/8', '1/4T', '1/4')
NO_TRIPLET_LAUNCH_QUANTIZE_NAMES = ('1/32', '1/16', '1/8', '1/4')
DEFAULT_LAUNCH_QUANTIZE_INDEX = 2
NO_TRIPLET_DEFAULT_LAUNCH_QUANTIZE_INDEX = 1
NOTE_RATE_GLOBAL_QUANTIZE_RATES = [
 LSQ.q_thirtytwoth,
 LSQ.q_sixtenth_triplet, LSQ.q_sixtenth,
 LSQ.q_eight_triplet, LSQ.q_eight,
 LSQ.q_quarter_triplet, LSQ.q_quarter]
NO_TRIPLET_NOTE_RATE_GLOBAL_QUANTIZE_RATES = [
 LSQ.q_thirtytwoth, LSQ.q_sixtenth,
 LSQ.q_eight, LSQ.q_quarter]
ASCII_A = 65
MAX_SENDS = 12
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/consts.pyc
