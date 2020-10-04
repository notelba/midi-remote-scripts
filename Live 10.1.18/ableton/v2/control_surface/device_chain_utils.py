# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\device_chain_utils.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
import Live
from itertools import imap, chain
from functools import partial
from ..base import find_if, liveobj_valid

def find_instrument_devices(track_or_chain):
    """
    Returns a list with all instruments from a track or chain.
    """
    if liveobj_valid(track_or_chain):
        instrument = find_if(lambda d: d.type == Live.Device.DeviceType.instrument, track_or_chain.devices)
        if liveobj_valid(instrument):
            if not instrument.can_have_drum_pads and instrument.can_have_chains:
                return chain([
                 instrument], *imap(find_instrument_devices, instrument.chains))
            return [
             instrument]
    return []


def find_instrument_meeting_requirement(requirement, track_or_chain):
    if liveobj_valid(track_or_chain):
        instrument = find_if(lambda d: d.type == Live.Device.DeviceType.instrument, track_or_chain.devices)
        if liveobj_valid(instrument):
            if requirement(instrument):
                return instrument
            if instrument.can_have_chains:
                recursive_call = partial(find_instrument_meeting_requirement, requirement)
                return find_if(bool, imap(recursive_call, instrument.chains))
    return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ableton/v2/control_surface/device_chain_utils.pyc
