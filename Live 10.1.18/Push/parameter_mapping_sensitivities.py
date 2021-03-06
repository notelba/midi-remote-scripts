# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\parameter_mapping_sensitivities.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface import is_parameter_quantized
DEFAULT_SENSITIVITY_KEY = b'normal_sensitivity'
FINE_GRAINED_SENSITIVITY_KEY = b'fine_grained_sensitivity'
CONTINUOUS_MAPPING_SENSITIVITY = 2.0
FINE_GRAINED_CONTINUOUS_MAPPING_SENSITIVITY = 0.01
QUANTIZED_MAPPING_SENSITIVITY = 1.0 / 15.0
PARAMETER_SENSITIVITIES = {b'UltraAnalog': {b'OSC1 Octave': {DEFAULT_SENSITIVITY_KEY: 0.05}, b'OSC2 Octave': {DEFAULT_SENSITIVITY_KEY: 0.05}, b'OSC1 Semi': {DEFAULT_SENSITIVITY_KEY: 0.05}, b'OSC1 Detune': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'OSC2 Semi': {DEFAULT_SENSITIVITY_KEY: 0.05}, b'OSC2 Detune': {DEFAULT_SENSITIVITY_KEY: 0.5}}, b'LoungeLizard': {b'Noise Pitch': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Damp Balance': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'P Amp < Key': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Semitone': {DEFAULT_SENSITIVITY_KEY: 0.1}}, b'Collision': {b'Res 1 Decay': {DEFAULT_SENSITIVITY_KEY: 0.5}}, b'InstrumentImpulse': {b'1 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'2 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'3 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'4 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'5 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'6 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'7 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'8 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1}}, b'OriginalSimpler': {b'Mode': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Playback': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Start': {DEFAULT_SENSITIVITY_KEY: 0.2}, b'End': {DEFAULT_SENSITIVITY_KEY: 0.2}, b'Sensitivity': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'S Start': {DEFAULT_SENSITIVITY_KEY: 0.2}, b'S Length': {DEFAULT_SENSITIVITY_KEY: 0.2}, b'S Loop Length': {DEFAULT_SENSITIVITY_KEY: 0.2}, b'Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Detune': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Gain': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Env. Type': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Filter Freq': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Filt < Vel': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Filt < Key': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Filt < LFO': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Fe < Env': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'LR < Key': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Vol < LFO': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Pan < RND': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Pan < LFO': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'L Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.5}}, b'Operator': {b'A Coarse': {DEFAULT_SENSITIVITY_KEY: 0.05}, b'B Coarse': {DEFAULT_SENSITIVITY_KEY: 0.05}, b'C Coarse': {DEFAULT_SENSITIVITY_KEY: 0.05}, b'D Coarse': {DEFAULT_SENSITIVITY_KEY: 0.05}, b'LFO Sync': {DEFAULT_SENSITIVITY_KEY: 0.1}}, b'MidiArpeggiator': {b'Style': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Synced Rate': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Offset': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Transp. Steps': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Transp. Dist.': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Repeats': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Ret. Interval': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Groove': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Retrigger Mode': {DEFAULT_SENSITIVITY_KEY: 0.1}}, b'MidiNoteLength': {b'Synced Length': {DEFAULT_SENSITIVITY_KEY: 0.1}}, b'MidiScale': {b'Base': {DEFAULT_SENSITIVITY_KEY: 0.05}, b'Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1}}, b'Amp': {b'Bass': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Middle': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Treble': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Presence': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Gain': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Volume': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'Dry/Wet': {DEFAULT_SENSITIVITY_KEY: 0.5}}, b'AutoFilter': {b'Frequency': {DEFAULT_SENSITIVITY_KEY: 1}, b'Env. Modulation': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'LFO Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'LFO Phase': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'LFO Offset': {DEFAULT_SENSITIVITY_KEY: 0.5}}, b'AutoPan': {b'Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.1}}, b'BeatRepeat': {b'Grid': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Interval': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Offset': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Gate': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Pitch': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Variation': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Mix Type': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Grid': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'Variation Type': {DEFAULT_SENSITIVITY_KEY: 0.1}}, b'Corpus': {b'LFO Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.1}}, b'Eq8': {b'Band': {DEFAULT_SENSITIVITY_KEY: 0.5}, b'1 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4}, b'2 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4}, b'3 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4}, b'4 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4}, b'5 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4}, b'6 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4}, b'7 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4}, b'8 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4}}, b'Flanger': {b'Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.1}}, b'GrainDelay': {b'Pitch': {DEFAULT_SENSITIVITY_KEY: 0.1}}, b'Phaser': {b'LFO Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.1}}, b'Resonator': {b'II Pitch': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'III Pitch': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'IV Pitch': {DEFAULT_SENSITIVITY_KEY: 0.1}, b'V Pitch': {DEFAULT_SENSITIVITY_KEY: 0.1}}, b'InstrumentVector': {b'Osc 1 Pitch': {DEFAULT_SENSITIVITY_KEY: 5.0, FINE_GRAINED_SENSITIVITY_KEY: 0.4}, b'Osc 2 Pitch': {DEFAULT_SENSITIVITY_KEY: 5.0, FINE_GRAINED_SENSITIVITY_KEY: 0.4}}}

def sensitivity_mapping_for_parameter(parameter, fine_grain=False):
    is_quantized = is_parameter_quantized(parameter, parameter and parameter.canonical_parent)
    if is_quantized:
        return QUANTIZED_MAPPING_SENSITIVITY
    if fine_grain:
        return FINE_GRAINED_CONTINUOUS_MAPPING_SENSITIVITY
    return CONTINUOUS_MAPPING_SENSITIVITY


def parameter_mapping_sensitivity(parameter, device_class=None):
    parameter_name = parameter.name if liveobj_valid(parameter) else b''
    try:
        return PARAMETER_SENSITIVITIES[device_class][parameter_name][DEFAULT_SENSITIVITY_KEY]
    except KeyError:
        return sensitivity_mapping_for_parameter(parameter)


def fine_grain_parameter_mapping_sensitivity(parameter, device_class=None):
    parameter_name = parameter.name if liveobj_valid(parameter) else b''
    try:
        return PARAMETER_SENSITIVITIES[device_class][parameter_name][FINE_GRAINED_SENSITIVITY_KEY]
    except KeyError:
        return sensitivity_mapping_for_parameter(parameter, fine_grain=True)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push/parameter_mapping_sensitivities.pyc
