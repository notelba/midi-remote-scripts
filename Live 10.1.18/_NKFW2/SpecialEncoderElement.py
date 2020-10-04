# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialEncoderElement.py
# Compiled at: 2017-10-19 12:46:57
import Live
MAP = Live.MidiMap.MapMode
from _Framework.EncoderElement import EncoderElement
from _Framework.SubjectSlot import SlotManager, subject_slot
from ControlUtils import reset_parameter
from Utils import live_object_is_valid
TWO_COMP = (
 MAP.relative_smooth_two_compliment, MAP.relative_two_compliment)
SIGNED_BIT = (MAP.relative_smooth_signed_bit, MAP.relative_signed_bit)

class SpecialEncoderElement(EncoderElement, SlotManager):
    """ SpecialEncoderElement that sends 0 value to clear LED when no parameter
    present.  Also includes property handling and a listener for the assigned parameter/
    property for use with M4L and displays.  A variant (PushEncoderElement) for encoders
    that include an integrated button is available in this module. """
    __subject_events__ = ('parameter', 'parameter_name', 'parameter_value')

    def __init__(self, *a, **k):
        self._last_received_value = -1
        self._thinner = 0
        self._property_to_map_to = None
        self._is_enabled = True
        super(SpecialEncoderElement, self).__init__(*a, **k)
        self._needs_takeover = False
        return

    @property
    def parameter(self):
        """ Returns the parameter or property this encoder is assigned to. """
        return self._parameter_to_map_to or self._property_to_map_to

    @property
    def parameter_name(self):
        """ (For use with M4L and displays): Returns the name of the parameter or property
        this encoder is assigned to. If not assigned, returns the CC# of the encoder if
        it's been translated. """
        param = self._parameter_to_map_to or self._property_to_map_to
        if param is None:
            if self.message_channel() != self.original_channel():
                header = 'Map#' if self.is_enabled() else 'CC#'
                return '%s %s' % (header, self.message_identifier())
            return ''
        return param.name

    @property
    def parameter_value(self):
        """ (For use with M4L and displays): Returns the unicode value of the parameter
        or property this encoder is assigned to. """
        param = self._parameter_to_map_to or self._property_to_map_to
        if param is not None:
            return unicode(param)
        else:
            return ''

    @subject_slot('value')
    def _on_parameter_value_changed(self):
        """ Notifies listeners of parameter_value upon changes. """
        self.notify_parameter_value(self.parameter_value)

    @subject_slot('name')
    def _on_parameter_name_changed(self):
        """ Notifies listeners of parameter_name upon changes. """
        self.notify_parameter_name(self.parameter_name)

    def release_parameter(self):
        """ Extends standard to send 0 value to clear LED if no parameter to map to
        and notify listener. """
        self._property_to_map_to = None
        super(SpecialEncoderElement, self).release_parameter()
        if not self.is_mapped_manually() and not self._parameter_to_map_to:
            self.send_value(0, force=True)
        self._update_assignment_and_notify()
        return

    def install_connections(self, install_translation=None, install_mapping=None, install_forwarding=None):
        """ Extends standard to notify listener. """
        super(SpecialEncoderElement, self).install_connections(install_translation, install_mapping, install_forwarding)
        self._update_assignment_and_notify()

    def set_property_to_map_to(self, prop):
        """ Sets the property to map to and notifies listeners. """
        notify = prop != self._property_to_map_to
        self._property_to_map_to = prop
        if notify:
            self._update_assignment_and_notify()

    def _update_assignment_and_notify(self):
        """ Updates/verifies this encoder's assignment, notifies listeners and sets up
        value and name listeners. """
        param = self.mapped_parameter()
        if self._property_to_map_to:
            param = self._property_to_map_to
        if self.is_mapped_manually() or not live_object_is_valid(param):
            param = None
        self.notify_parameter(param)
        self.notify_parameter_name(self.parameter_name)
        self.notify_parameter_value(self.parameter_value)
        self._on_parameter_value_changed.subject = param
        self._on_parameter_name_changed.subject = param
        return

    def is_enabled(self):
        """ Returns whether this control is enabled. """
        return self._is_enabled

    def is_mapped_manually(self):
        """ Returns whether the encoder has been MIDI mapped. """
        return not self._is_mapped and not self._is_being_forwarded

    def receive_value(self, value):
        """ Extends standard to store last received value. """
        super(SpecialEncoderElement, self).receive_value(value)
        self._last_received_value = value

    def get_adjustment_factor(self, value, threshold=10):
        """ Returns the adjustment factor to use for endless encoders. Applies thinning
        (using the given threshold if it isn't 0) to allow for more coarse adjustment. """
        if threshold:
            factor = -1
            if value <= 63:
                factor = 1
            if self._thinner is not 0:
                self._thinner += factor
                if abs(self._thinner) >= threshold:
                    self._thinner = 0
                    return factor
            else:
                self._thinner = factor
        else:
            factor = value
            if value > 63:
                if self.message_map_mode() in TWO_COMP:
                    factor = -(128 - value)
                elif self.message_map_mode() in SIGNED_BIT:
                    factor = 64 - value
            return factor
        return 0

    def set_enabled(self, enabled):
        """ Enables/disables the control. When disabled, it can be used for sending data
        to MIDI tracks. """
        if self._is_enabled != bool(enabled):
            self._is_enabled = bool(enabled)
            self._request_rebuild()

    def script_wants_forwarding(self):
        """ Returns whether or not the control should be used in the script or to send
        data to MIDI tracks. """
        return self._is_enabled

    def should_suppress_feedback_for_property_controls(self):
        """ For use with absolute encoders with LEDs, this determines if PropertyControl
        should send feedback to the control or should suppress the feedback after the
        control has been moved.  This will be True in most cases. """
        return True


class PushEncoderElement(SpecialEncoderElement):
    """ Specialized SpecialEncoderElement that includes a push button that can reset or
    toggle the assigned parameter/property. """

    def __init__(self, msg_type, channel, identifier, map_mode, encoder_sensitivity=None, push_button=None, *a, **k):
        super(PushEncoderElement, self).__init__(msg_type, channel, identifier, map_mode, encoder_sensitivity, *a, **k)
        self._on_push_button_value.subject = push_button

    @subject_slot('value')
    def _on_push_button_value(self, value):
        if value:
            if self._property_to_map_to:
                reset_parameter(self._property_to_map_to)
            else:
                reset_parameter(self._parameter_to_map_to)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialEncoderElement.pyc
