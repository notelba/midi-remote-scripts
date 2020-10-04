# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\MidiMap.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.InputControlElement import MIDI_NOTE_TYPE, MIDI_CC_TYPE
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.Dependency import depends
from _Framework.Resource import PrioritizedResource
from SpecialButtonElement import SpecialButtonElement
from BlinkingButtonElement import BlinkingButtonElement, OverridingBlinkingButtonElement
from MultiButtonElement import MultiButtonElement
from SpecialEncoderElement import SpecialEncoderElement, PushEncoderElement
from SpecialComboElement import SpecialComboElement

@depends(skin=None)
def make_button(name, channel, number, msg_type, is_mty, skin=None, **k):
    """ Returns a standard SpecialButtonElement. """
    return SpecialButtonElement(is_mty, msg_type, channel, number, name=name, skin=skin, **k)


@depends(skin=None)
def make_blinking_button(name, channel, number, msg_type, is_mty, skin=None, **k):
    """ Returns a BlinkingButtonElement. """
    return BlinkingButtonElement(is_mty, msg_type, channel, number, name=name, skin=skin, **k)


@depends(skin=None)
def make_overriding_blinking_button(name, channel, number, msg_type, is_mty, skin=None, **k):
    """ Returns an OverridingBlinkingButtonElement. """
    return OverridingBlinkingButtonElement(is_mty, msg_type, channel, number, name=name, skin=skin, **k)


@depends(skin=None)
@depends(slave_channels=None)
def make_multi_button(name, channel, number, msg_type, is_mty, skin=None, slave_channels=None, **k):
    """ Returns a MultiButtonElement. """
    return MultiButtonElement(is_mty, msg_type, channel, number, name=name, skin=skin, slave_channels=slave_channels, **k)


def make_encoder(name, channel, number, msg_type, map_mode, feed_delay, takeover, **k):
    """ Sets up and returns a standard SpecialEncoderElement. """
    element = SpecialEncoderElement(msg_type, channel, number, map_mode, name=name)
    element.set_feedback_delay(feed_delay)
    element.set_needs_takeover(takeover)
    return element


@depends(push_button=None)
def make_push_encoder(name, channel, number, msg_type, map_mode, feed_delay, takeover, push_button=None, **k):
    """ Returns a PushEncoderElement. """
    element = PushEncoderElement(msg_type, channel, number, map_mode, name=name, push_button=push_button)
    element.set_feedback_delay(feed_delay)
    element.set_needs_takeover(takeover)
    return element


def _one_dimensional_name(base_name, x, _):
    return '%s_%d' % (base_name, x)


def _two_dimensional_name(base_name, x, y):
    return '%s_%d_%d' % (base_name, x, y)


def _default_matrix_element_factory(name, numbers, channel, msg_type, factory, **k):
    name_factory = _two_dimensional_name if len(numbers) > 1 else _one_dimensional_name
    return [ [ factory(name_factory(name, column, row), channel, identifier, msg_type, **k) for column, identifier in enumerate(identifiers) ] for row, identifiers in enumerate(numbers)
           ]


def _multi_channel_matrix_element_factory(name, numbers, _, msg_type, factory, channel_start=0, **k):
    name_factory = _two_dimensional_name if len(numbers) > 1 else _one_dimensional_name
    return [ [ factory(name_factory(name, column, row), (column + channel_start), identifier, msg_type, **k) for column, identifier in enumerate(identifiers) ] for row, identifiers in enumerate(numbers)
           ]


@depends(push_buttons=None)
def _push_encoder_matrix_element_factory(name, numbers, channel, msg_type, factory, push_buttons=None, **k):
    assert len(numbers) == 1
    return [ [ factory(_one_dimensional_name(name, column, row), channel, identifier, msg_type, push_button=push_buttons[column], **k) for column, identifier in enumerate(identifiers) ] for row, identifiers in enumerate(numbers)
           ]


class MidiMap(dict):
    """ Dict of controls adapted from Framework version. """

    def __init__(self, *a, **k):
        super(MidiMap, self).__init__(*a, **k)

    def add_button(self, name, number, channel=0, msg_type=MIDI_NOTE_TYPE, is_mty=True, factory=make_button, **k):
        """ Adds a button to the map. """
        assert name not in self.keys()
        self[name] = factory(name, channel, number, msg_type, is_mty, **k)

    def add_modifier_button(self, name, number, channel=0, msg_type=MIDI_NOTE_TYPE, factory=make_button, **k):
        """ Adds a modifier button to the map. """
        assert name not in self.keys()
        self[name] = factory(name, channel, number, msg_type, True, resource_type=PrioritizedResource, **k)

    def add_encoder(self, name, number, map_mode, channel=0, msg_type=MIDI_CC_TYPE, feed_delay=1, takeover=False, factory=make_encoder, **k):
        """ Adds an encoder to the map. """
        assert name not in self.keys()
        self[name] = factory(name, channel, number, msg_type, map_mode, feed_delay, takeover, **k)

    def add_button_matrix(self, name, numbers, channel=0, msg_type=MIDI_NOTE_TYPE, is_mty=True, factory=make_button, **k):
        """ Adds a button matrix to the map. """
        self._add_matrix(name, numbers, channel, msg_type, factory, is_mty=is_mty, **k)

    def add_multi_channel_button_matrix(self, name, numbers, channel_start=0, msg_type=MIDI_NOTE_TYPE, is_mty=True, factory=make_button, **k):
        """ Adds a multi-channel button matrix (where each column uses ascending
        MIDI channels) to the map. """
        self._add_matrix(name, numbers, channel_start, msg_type, factory, is_mty=is_mty, element_factory=_multi_channel_matrix_element_factory, **k)

    def add_encoder_matrix(self, name, numbers, map_mode, channel=0, msg_type=MIDI_CC_TYPE, feed_delay=1, takeover=False, factory=make_encoder, **k):
        """ Adds an encoder matrix to the map. """
        self._add_matrix(name, numbers, channel, msg_type, factory, map_mode=map_mode, feed_delay=feed_delay, takeover=takeover, **k)

    def add_multi_channel_encoder_matrix(self, name, numbers, map_mode, channel_start=0, msg_type=MIDI_CC_TYPE, feed_delay=1, takeover=False, factory=make_encoder, **k):
        """ Adds a multi-channel encoder matrix (where each column uses ascending MIDI
        channels) to the map. """
        self._add_matrix(name, numbers, channel_start, msg_type, factory, map_mode=map_mode, feed_delay=feed_delay, takeover=takeover, element_factory=_multi_channel_matrix_element_factory, **k)

    def add_push_encoder_matrix(self, name, numbers, map_mode, channel=0, msg_type=MIDI_CC_TYPE, feed_delay=1, takeover=False, push_buttons=None, **k):
        """ Adds a push encoder matrix to the map. This can currently only be 1D. """
        self._add_matrix(name, numbers, channel, msg_type, make_push_encoder, map_mode=map_mode, feed_delay=feed_delay, takeover=takeover, element_factory=_push_encoder_matrix_element_factory, push_buttons=push_buttons, **k)

    def _add_matrix(self, name, numbers, channel, msg_type, factory, element_factory=_default_matrix_element_factory, **k):
        """ Adds either a button or encoder matrix to the map. """
        assert name not in self.keys()
        elements = element_factory(name, numbers, channel, msg_type, factory, **k)
        self['%s_raw' % name] = elements
        self[name] = ButtonMatrixElement(name=name, rows=elements)

    def with_modifier(self, modifier_name, control, **k):
        """ Returns a modifier + control ComboElement. """
        assert modifier_name in self.keys()
        return SpecialComboElement(control, modifiers=[self[modifier_name]], **k)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/MidiMap.pyc
