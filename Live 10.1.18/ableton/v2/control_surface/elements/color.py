# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\elements\color.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from ...base import EventObject, listenable_property, listens, liveobj_valid, nop

def to_midi_value(int_or_color):
    if hasattr(int_or_color, b'midi_value'):
        return int_or_color.midi_value
    else:
        return int(int_or_color)


class Color(object):
    """
    Basic interface for showing a color.
    """
    midi_value = 0

    def __init__(self, midi_value=None, *a, **k):
        super(Color, self).__init__(*a, **k)
        if midi_value is not None:
            self.midi_value = midi_value
        return

    def draw(self, interface):
        """
        Draws the color into the interface.  Depending on the color
        type, interface might require special capabilities.
        """
        interface.send_value(self.midi_value)


class DynamicColorFactory(object):

    def __init__(self, transformation=nop, *a, **k):
        assert callable(transformation)
        super(DynamicColorFactory, self).__init__(*a, **k)
        self._transform = transformation

    def instantiate(self, song):
        raise NotImplementedError


def is_dynamic_color_factory(skin_element):
    return isinstance(skin_element, DynamicColorFactory)


class DynamicColorBase(Color, EventObject):
    midi_value = listenable_property.managed(0)

    def __init__(self, transformation=nop, *a, **k):
        assert callable(transformation)
        super(DynamicColorBase, self).__init__(*a, **k)
        self._transformation = transformation

    def _update_midi_value(self, colored_object):
        color_index = colored_object.color_index if liveobj_valid(colored_object) else None
        self.midi_value = self._transformation(color_index)
        return


class SelectedTrackColor(DynamicColorBase):

    def __init__(self, song_view=None, *a, **k):
        assert liveobj_valid(song_view)
        super(SelectedTrackColor, self).__init__(*a, **k)
        self.__on_color_changed.subject = song_view
        self.__on_color_changed()

    @listens(b'selected_track.color_index')
    def __on_color_changed(self, *a):
        self._update_midi_value(self.__on_color_changed.subject.selected_track)


class SelectedClipColor(DynamicColorBase):

    def __init__(self, song_view=None, *a, **k):
        assert liveobj_valid(song_view)
        super(SelectedClipColor, self).__init__(*a, **k)
        self.__on_color_changed.subject = song_view
        self.__on_color_changed()

    @listens(b'detail_clip.color_index')
    def __on_color_changed(self, *a):
        view = self.__on_color_changed.subject
        self._update_midi_value(view.detail_clip)


class SelectedTrackColorFactory(DynamicColorFactory):

    def instantiate(self, song):
        return SelectedTrackColor(song_view=song.view, transformation=self._transform)


class SelectedClipColorFactory(DynamicColorFactory):

    def instantiate(self, song):
        return SelectedClipColor(song_view=song.view, transformation=self._transform)


class AnimatedColor(Color):
    _channel = None

    def __init__(self, color1=None, color2=None, *a, **k):
        super(AnimatedColor, self).__init__(*a, **k)
        self._color1 = color1
        self._color2 = color2

    def draw(self, interface):
        interface.send_value(self._color1.midi_value)
        interface.send_value(self._color2.midi_value, channel=self._channel)


class SysexRGBColor(Color):

    def __init__(self, midi_value=None, *a, **k):
        assert isinstance(midi_value, tuple) and len(midi_value) == 3
        super(SysexRGBColor, self).__init__(midi_value, *a, **k)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ableton/v2/control_surface/elements/color.pyc
