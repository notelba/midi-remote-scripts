# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\BLOCKS\skin.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Skin
from ableton.v2.control_surface.elements import Color
from .colors import Rgb

class Colors:

    class DefaultButton:
        On = Rgb.WHITE
        Off = Rgb.BLACK
        Disabled = Rgb.BLACK

    class Session:
        RecordButton = Rgb.RED
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        ClipStopped = Rgb.AMBER
        Scene = Rgb.GREEN
        SceneTriggered = Rgb.GREEN_BLINK
        NoScene = Rgb.BLACK
        StopClipTriggered = Rgb.RED_PULSE
        StopClip = Rgb.RED
        StopClipDisabled = Rgb.BLACK
        ClipEmpty = Rgb.BLACK

    class DrumGroup:
        PadEmpty = Rgb.BLACK
        PadFilled = Rgb.YELLOW
        PadSelected = Rgb.LIGHT_BLUE
        PadSelectedNotSoloed = Rgb.LIGHT_BLUE
        PadMuted = Rgb.DARK_ORANGE
        PadMutedSelected = Rgb.LIGHT_BLUE
        PadSoloed = Rgb.DARK_BLUE
        PadSoloedSelected = Rgb.LIGHT_BLUE
        PadInvisible = Rgb.BLACK
        PadAction = Rgb.RED


skin = Skin(Colors)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/BLOCKS/skin.pyc
