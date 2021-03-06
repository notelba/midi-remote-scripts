# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\skin.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Skin
from .colors import Mono, Rgb

class Colors:

    class DefaultButton:
        On = Rgb.GREEN
        Off = Rgb.BLACK
        Disabled = Rgb.BLACK

    class Recording:
        On = Rgb.RED
        Off = Rgb.RED_HALF
        Transition = Rgb.RED_BLINK
        CaptureTriggered = Rgb.WHITE

    class FixedLength:
        On = Rgb.BLUE
        Off = Rgb.WHITE_HALF
        Held = Rgb.BLUE_PULSE
        Option = Rgb.BLACK
        OptionInRange = Rgb.BLUE_PULSE
        OptionHeld = Rgb.BLUE

    class Transport:
        PlayOff = Mono.OFF
        PlayOn = Mono.ON
        ContinueOff = Mono.OFF
        ContinueOn = Mono.HALF
        CaptureOff = Mono.OFF
        CaptureOn = Mono.HALF
        MetronomeOff = Rgb.RED_HALF
        MetronomeOn = Rgb.AQUA

    class Action:
        Undo = Rgb.CREAM
        UndoPressed = Rgb.WHITE
        Redo = Rgb.CREAM
        RedoPressed = Rgb.WHITE
        Delete = Rgb.WHITE_HALF
        DeletePressed = Rgb.WHITE
        Duplicate = Rgb.WHITE_HALF
        DuplicatePressed = Rgb.WHITE
        Quantize = Rgb.WHITE_HALF
        QuantizePressed = Rgb.WHITE
        Double = Rgb.CREAM
        DoublePressed = Rgb.WHITE

    class Session:
        RecordButton = Rgb.RED_HALF
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        ClipEmpty = Rgb.BLACK
        Scene = Rgb.BLACK
        SceneTriggered = Rgb.GREEN_BLINK
        NoScene = Rgb.BLACK
        StopClipTriggered = Rgb.RED_BLINK
        StopClip = Rgb.RED
        StopClipDisabled = Rgb.RED_HALF
        Navigation = Rgb.WHITE_HALF
        NavigationPressed = Rgb.WHITE
        Select = Rgb.WHITE_HALF
        SelectPressed = Rgb.WHITE
        Delete = Rgb.WHITE_HALF
        DeletePressed = Rgb.WHITE
        Duplicate = Rgb.WHITE_HALF
        DuplicatePressed = Rgb.WHITE
        Quantize = Rgb.WHITE_HALF
        QuantizePressed = Rgb.WHITE
        Double = Rgb.CREAM
        DoublePressed = Rgb.WHITE
        ActionTriggered = Rgb.WHITE

    class Zooming:
        Selected = Rgb.OFF_WHITE
        Stopped = Rgb.LIGHT_BLUE_HALF
        Playing = Rgb.GREEN_PULSE
        Empty = Rgb.BLACK

    class Mixer:
        SoloOn = Rgb.BLUE
        SoloOff = Rgb.BLUE_HALF
        MuteOn = Rgb.YELLOW_HALF
        MuteOff = Rgb.YELLOW
        ArmOn = Rgb.RED
        ArmOff = Rgb.RED_HALF
        EmptyTrack = Rgb.BLACK
        TrackSelected = Rgb.WHITE
        TrackNotSelected = Rgb.WHITE_HALF

    class DrumGroup:
        PadEmpty = Rgb.BLACK
        PadFilled = Rgb.YELLOW
        PadSelected = Rgb.LIGHT_BLUE
        PadSelectedNotSoloed = Rgb.LIGHT_BLUE
        PadMuted = Rgb.DARK_ORANGE
        PadMutedSelected = Rgb.LIGHT_BLUE
        PadSoloed = Rgb.DARK_BLUE
        PadSoloedSelected = Rgb.LIGHT_BLUE
        PadAction = Rgb.WHITE
        Navigation = Rgb.YELLOW_HALF
        NavigationPressed = Rgb.YELLOW

    class Mode:

        class Volume:
            On = Rgb.GREEN
            Off = Rgb.WHITE_HALF

        class Pan:
            On = Rgb.ORANGE
            Off = Rgb.WHITE_HALF

        class SendA:
            On = Rgb.VIOLET
            Off = Rgb.WHITE_HALF

        class SendB:
            On = Rgb.DARK_BLUE
            Off = Rgb.WHITE_HALF

        class Stop:
            On = Rgb.RED
            Off = Rgb.WHITE_HALF

        class Mute:
            On = Rgb.YELLOW
            Off = Rgb.WHITE_HALF

        class Solo:
            On = Rgb.BLUE
            Off = Rgb.WHITE_HALF

        class Arm:
            On = Rgb.RED
            Off = Rgb.WHITE_HALF

        class Launch:
            On = Rgb.WHITE_HALF


skin = Skin(Colors)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/skin.pyc
