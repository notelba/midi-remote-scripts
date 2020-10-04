# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\DefaultSkin.py
# Compiled at: 2017-09-30 15:26:22
from _Framework.Skin import Skin
from DefaultColors import DefaultColors

class Colors():
    """ Skin to use for buttons with single color LEDs. """

    class DefaultButton:
        On = DefaultColors.ON
        Off = DefaultColors.OFF
        Disabled = DefaultColors.OFF

    class ButtonSlider:
        Slider = DefaultColors.ON
        Bipolar = DefaultColors.ON
        IncDecOn = DefaultColors.ON
        IncDecOff = DefaultColors.OFF
        OffOnOn = DefaultColors.ON
        OffOnOff = DefaultColors.OFF
        ClearOn = DefaultColors.ON
        ClearOff = DefaultColors.OFF

    class Navigation:
        StandardEnabled = DefaultColors.ON
        SessionEnabled = DefaultColors.ON
        DeviceEnabled = DefaultColors.ON
        DrumRackEnabled = DefaultColors.ON
        SimplerEnabled = DefaultColors.ON
        OctavesEnabled = DefaultColors.ON
        ScalesEnabled = DefaultColors.ON
        TonicsEnabled = DefaultColors.ON
        OffsetsEnabled = DefaultColors.ON
        PresetEnabled = DefaultColors.ON
        PageEnabled = DefaultColors.ON
        Pressed = DefaultColors.OFF
        Disabled = DefaultColors.OFF

    class Modes:
        Selected = DefaultColors.ON
        NotSelected = DefaultColors.OFF
        AltSelected = DefaultColors.ON

    class Pages:
        Selected = DefaultColors.ON
        NotSelected = DefaultColors.OFF

    class Global:
        LockOn = DefaultColors.ON
        LockOff = DefaultColors.OFF
        HasSnap = DefaultColors.SLOW_BLINK
        CanAdd = DefaultColors.ON
        CannotAdd = DefaultColors.OFF
        CanDelete = DefaultColors.ON
        CannotDelete = DefaultColors.OFF
        CanCapture = DefaultColors.ON
        CannotCapture = DefaultColors.OFF

    class Preset:
        Selected = DefaultColors.ON
        NotSelected = DefaultColors.OFF

    class Undo:
        Undo = DefaultColors.OFF
        UndoPressed = DefaultColors.ON
        Redo = DefaultColors.OFF
        RedoPressed = DefaultColors.ON

    class View:
        DetailOn = DefaultColors.ON
        DetailOff = DefaultColors.OFF
        ClipOn = DefaultColors.ON
        ClipOff = DefaultColors.OFF
        ArrangeOn = DefaultColors.ON
        ArrangeOff = DefaultColors.OFF

    class Transport:
        PlayOn = DefaultColors.ON
        PlayOff = DefaultColors.OFF
        ContinueOn = DefaultColors.ON
        ContinueOff = DefaultColors.OFF
        StopOn = DefaultColors.ON
        StopOff = DefaultColors.OFF
        OverdubOn = DefaultColors.ON
        OverdubOff = DefaultColors.OFF
        RecordOn = DefaultColors.ON
        RecordOff = DefaultColors.OFF
        MetronomeOn = DefaultColors.ON
        MetronomeOff = DefaultColors.OFF
        LoopOn = DefaultColors.ON
        LoopOff = DefaultColors.OFF
        RecordQuantizeOn = DefaultColors.ON
        RecordQuantizeOff = DefaultColors.OFF
        SeekPressed = DefaultColors.ON
        SeekIdle = DefaultColors.OFF
        CanJumpToNextCue = DefaultColors.ON
        CannotJumpToNextCue = DefaultColors.OFF
        CanJumpToPrevCue = DefaultColors.ON
        CannotJumpToPrevCue = DefaultColors.OFF
        Nudge = DefaultColors.OFF
        NudgePressed = DefaultColors.ON
        TapTempo = DefaultColors.OFF
        TapTempoPressed = DefaultColors.ON
        Revert = DefaultColors.OFF
        RevertPressed = DefaultColors.ON

    class Recording:
        Transition = DefaultColors.FAST_BLINK
        On = DefaultColors.ON
        Off = DefaultColors.OFF
        NewOn = DefaultColors.ON
        NewOff = DefaultColors.OFF
        CreateOn = DefaultColors.ON
        CreateOff = DefaultColors.OFF
        AutomationOn = DefaultColors.ON
        AutomationOff = DefaultColors.OFF
        CanDeleteAutomation = DefaultColors.ON
        CannotDeleteAutomation = DefaultColors.OFF
        CanEnableAutomation = DefaultColors.ON
        CannotEnableAutomation = DefaultColors.OFF

    class CuePoint:
        Present = DefaultColors.ON
        Selected = DefaultColors.ON
        Triggered = DefaultColors.FAST_BLINK

    class Modifiers:
        Shift = DefaultColors.OFF
        Select = DefaultColors.OFF
        Delete = DefaultColors.OFF
        Duplicate = DefaultColors.OFF
        Double = DefaultColors.OFF
        Quantize = DefaultColors.OFF
        Mute = DefaultColors.OFF
        Solo = DefaultColors.OFF
        Store = DefaultColors.ON
        Pressed = DefaultColors.ON

    class Session:
        StopClipTriggered = DefaultColors.FAST_BLINK
        StopClip = DefaultColors.ON
        Scene = DefaultColors.ON
        NoScene = DefaultColors.OFF
        SceneTriggered = DefaultColors.FAST_BLINK
        ClipTriggeredPlay = DefaultColors.FAST_BLINK
        ClipTriggeredRecord = DefaultColors.FAST_BLINK
        RecordButton = DefaultColors.OFF
        ClipStopped = DefaultColors.ON
        ClipStarted = DefaultColors.SLOW_BLINK
        ClipRecording = DefaultColors.SLOW_BLINK
        StopAll = DefaultColors.OFF
        StopAllPressed = DefaultColors.ON
        StoppedClip = DefaultColors.OFF
        BlockedGroupClip = DefaultColors.OFF

    class Zooming:
        Stopped = DefaultColors.ON
        Selected = DefaultColors.FAST_BLINK
        Playing = DefaultColors.SLOW_BLINK
        Empty = DefaultColors.OFF

    class Track:
        Muted = DefaultColors.OFF
        NotMuted = DefaultColors.ON
        Soloed = DefaultColors.ON
        NotSoloed = DefaultColors.OFF
        Armed = DefaultColors.ON
        NotArmed = DefaultColors.OFF
        Selected = DefaultColors.ON
        NotSelected = DefaultColors.OFF
        SelectedAndArmed = DefaultColors.FAST_BLINK
        NotSelectedAndArmed = DefaultColors.SLOW_BLINK
        Empty = DefaultColors.OFF

    class ResetStrip:
        VolumeCanReset = DefaultColors.ON
        VolumeCannotReset = DefaultColors.OFF
        PanCanReset = DefaultColors.ON
        PanCannotReset = DefaultColors.OFF
        SendACanReset = DefaultColors.ON
        SendACannotReset = DefaultColors.OFF
        SendBCanReset = DefaultColors.ON
        SendBCannotReset = DefaultColors.OFF

    class Sends:
        Selected0 = DefaultColors.ON
        NotSelected0 = DefaultColors.OFF
        Selected1 = DefaultColors.ON
        NotSelected1 = DefaultColors.OFF
        Selected2 = DefaultColors.ON
        NotSelected2 = DefaultColors.OFF
        Selected3 = DefaultColors.ON
        NotSelected3 = DefaultColors.OFF
        Selected4 = DefaultColors.ON
        NotSelected4 = DefaultColors.OFF
        Selected5 = DefaultColors.ON
        NotSelected5 = DefaultColors.OFF
        Selected6 = DefaultColors.ON
        NotSelected6 = DefaultColors.OFF
        Selected7 = DefaultColors.ON
        NotSelected7 = DefaultColors.OFF

    class Meters:
        LowDim = DefaultColors.ON
        LowHalf = DefaultColors.ON
        LowFull = DefaultColors.ON
        Mid = DefaultColors.ON
        High = DefaultColors.ON
        Volume = DefaultColors.ON

    class Device:
        Off = DefaultColors.OFF
        On = DefaultColors.ON
        NoDevice = DefaultColors.OFF
        BankEnabled = DefaultColors.ON
        BankDisabled = DefaultColors.OFF

    class Chain:
        Empty = DefaultColors.OFF
        DevicesVisible = DefaultColors.ON
        DevicesNotVisible = DefaultColors.OFF
        CanSelectChain = DefaultColors.ON
        CannotSelectChain = DefaultColors.OFF

    class HazMap:
        Modifier = DefaultColors.OFF
        ModifierPressed = DefaultColors.ON
        ModifierMapping = DefaultColors.SLOW_BLINK
        DeleteButton = DefaultColors.ON
        IsDeleting = DefaultColors.SLOW_BLINK
        MapButton = DefaultColors.ON
        IsMapping = DefaultColors.SLOW_BLINK
        NoAssign = DefaultColors.OFF
        HasAssign = DefaultColors.ON

    class DrumRack:
        PadEmpty = DefaultColors.OFF
        PadFilled = DefaultColors.ON
        PadSelected = DefaultColors.ON
        PadMuted = DefaultColors.SLOW_BLINK
        PadSoloed = DefaultColors.FAST_BLINK
        CanSelectPad = DefaultColors.ON
        CannotSelectPad = DefaultColors.OFF
        PadCopySource = DefaultColors.FAST_BLINK

    class GenericDrum:
        Quad_0 = DefaultColors.ON
        Quad_1 = DefaultColors.OFF
        Quad_2 = DefaultColors.ON
        Quad_3 = DefaultColors.OFF

    class Simpler:
        StartEnabled = DefaultColors.ON
        EndEnabled = DefaultColors.ON
        MultiEnabled = DefaultColors.ON
        NudgeEnabled = DefaultColors.ON
        WarpIncrementEnabled = DefaultColors.ON
        WarpIncrementPressed = DefaultColors.OFF
        WarpAsEnabled = DefaultColors.ON
        WarpAsPressed = DefaultColors.OFF
        ReverseEnabled = DefaultColors.ON
        ReversePressed = DefaultColors.OFF
        RemoveSliceEnabled = DefaultColors.ON
        RemoveSlicePressed = DefaultColors.OFF
        ResetSlicesEnabled = DefaultColors.ON
        ResetSlicesPressed = DefaultColors.OFF
        ClearSlicesEnabled = DefaultColors.ON
        ClearSlicesPressed = DefaultColors.OFF
        ConvertEnabled = DefaultColors.ON
        TriggerModeOn = DefaultColors.ON
        TriggerModeOff = DefaultColors.OFF
        PadSlicingOn = DefaultColors.ON
        PadSlicingOff = DefaultColors.OFF
        SlicePad = DefaultColors.ON
        SlicePadEmpty = DefaultColors.OFF
        SlicePadSelected = DefaultColors.ON

        class PlaybackMode:
            ToggleEnabled = DefaultColors.ON
            Selected = DefaultColors.ON
            NotSelected = DefaultColors.OFF

        class SlicingMode:
            ToggleEnabled = DefaultColors.ON
            Selected = DefaultColors.ON
            NotSelected = DefaultColors.OFF

        class SlicingStyle:
            ToggleEnabled = DefaultColors.ON
            Selected = DefaultColors.ON
            NotSelected = DefaultColors.OFF

    class Instrument:

        class Scales:
            Selected = DefaultColors.ON
            NotSelected = DefaultColors.OFF
            InKeyOff = DefaultColors.OFF
            InKeyOn = DefaultColors.ON
            SequentOff = DefaultColors.OFF
            SequentOn = DefaultColors.ON
            HorizontalOff = DefaultColors.OFF
            HorizontalOn = DefaultColors.ON

        class Tonics:
            Selected = DefaultColors.ON
            NotSelected = DefaultColors.OFF
            InKey = DefaultColors.OFF

        class Offsets:
            Selected = DefaultColors.ON
            NotSelected = DefaultColors.OFF

        class Notes:
            Tonic = DefaultColors.ON
            InKey = DefaultColors.ON
            OutOfKey = DefaultColors.OFF
            Natural = DefaultColors.ON
            Sharp = DefaultColors.OFF

        class FullVelocity:
            Off = DefaultColors.OFF
            On = DefaultColors.ON
            Inactive = DefaultColors.OFF

    class NoteRepeat:
        Off = DefaultColors.OFF
        On = DefaultColors.ON
        Inactive = DefaultColors.OFF

        class Rate:
            Selected = DefaultColors.ON
            NotSelected = DefaultColors.OFF

        class Swing:
            On = DefaultColors.ON
            Off = DefaultColors.OFF

    class VelocityLevels:
        Selected = DefaultColors.ON
        NotSelected = DefaultColors.OFF

    class Sequence:

        class Step:
            Muted = DefaultColors.ON
            Unusable = DefaultColors.OFF
            Off = DefaultColors.OFF

            class Even:
                OnHigh = DefaultColors.ON
                OnMid = DefaultColors.ON
                OnLow = DefaultColors.ON

            class Odd:
                OnHigh = DefaultColors.ON
                OnMid = DefaultColors.ON
                OnLow = DefaultColors.ON

            class Tonic:
                OnHigh = DefaultColors.ON
                OnMid = DefaultColors.ON
                OnLow = DefaultColors.ON

        class Fold:
            On = DefaultColors.ON
            Off = DefaultColors.OFF

        class Page:
            Playing = DefaultColors.SLOW_BLINK
            Selected = DefaultColors.FAST_BLINK
            InRange = DefaultColors.ON
            OutOfRange = DefaultColors.OFF

        class Velocity:
            Selected = DefaultColors.ON
            NotSelected = DefaultColors.OFF

        class Resolution:
            Selected = DefaultColors.ON
            NotSelected = DefaultColors.OFF

    class Clip:
        NoClip = DefaultColors.OFF
        StopActive = DefaultColors.ON
        StopInactive = DefaultColors.OFF
        DeleteActive = DefaultColors.ON
        DoubleActive = DefaultColors.ON
        DuplicateActive = DefaultColors.ON
        QuantizeActive = DefaultColors.ON
        LegatoOn = DefaultColors.ON
        LegatoOff = DefaultColors.OFF

        class Loop:
            On = DefaultColors.ON
            Off = DefaultColors.OFF

            class Even:
                InRange = DefaultColors.ON
                PartiallyInRange = DefaultColors.ON
                OutOfRange = DefaultColors.OFF

            class Odd:
                InRange = DefaultColors.ON
                PartiallyInRange = DefaultColors.ON
                OutOfRange = DefaultColors.OFF

        class Pitch:
            Ascending = DefaultColors.OFF
            Descending = DefaultColors.OFF
            Selected = DefaultColors.ON

        class Playhead:
            Even = DefaultColors.ON
            Odd = DefaultColors.ON

        class Scrubhead:
            Even = DefaultColors.ON
            Odd = DefaultColors.ON

    class LaunchQuantize:
        Selected = DefaultColors.FAST_BLINK
        NotSelected = DefaultColors.ON

    class GlobalQuantize:
        Selected = DefaultColors.FAST_BLINK
        NotSelected = DefaultColors.ON

    class VisualMetronome:
        Off = DefaultColors.OFF
        Beat = DefaultColors.ON
        Bar = DefaultColors.ON

    class XY:
        X = DefaultColors.ON
        Y = DefaultColors.ON
        Point = DefaultColors.ON
        X_LearnOn = DefaultColors.FAST_BLINK
        X_LearnOff = DefaultColors.OFF
        Y_LearnOn = DefaultColors.FAST_BLINK
        Y_LearnOff = DefaultColors.OFF

    class ColorChoices:
        OFF = DefaultColors.OFF
        ON = DefaultColors.ON


def make_default_skin():
    return Skin(Colors)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/DefaultSkin.pyc
