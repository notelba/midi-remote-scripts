# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\RingedEncoderMixin.py
# Compiled at: 2017-10-19 12:46:57
from ControlUtils import parameter_is_quantized, parameter_value_to_midi_value
from Utils import live_object_is_valid

class MappingType(object):
    """ The various types of parameter mappings that correspond to ring modes. """
    NONE = 0
    MANUAL = 1
    NORMAL = 2
    BIPOLAR = 3
    QUANTIZED = 4


class RingedEncoderMixin(object):
    """ RingedEncoderMixin is a mixin for an encoder/slider that includes LEDs that can
    operate in several modes (such as single, full, bipolar, etc). """

    def release_parameter(self):
        """ Extends standard to update ring mode. """
        super(RingedEncoderMixin, self).release_parameter()
        self._update_ring_mode()

    def install_connections(self, *a, **k):
        """ Extends standard to update ring mode. """
        super(RingedEncoderMixin, self).install_connections(*a, **k)
        self._update_ring_mode()

    def connect_to(self, p):
        """ Extends standard to update ring mode. """
        super(RingedEncoderMixin, self).connect_to(p)
        self._update_ring_mode()

    def set_property_to_map_to(self, prop):
        """ Extends standard to update ring mode. """
        super(RingedEncoderMixin, self).set_property_to_map_to(prop)
        self._update_ring_mode()

    def set_ring_mode(self, mode):
        """ Called to set the ring mode based on the passed mode. To be overridden. """
        raise NotImplementedError

    def send_value_on_ring_mode_change(self, value):
        """ Sends a value to the ring mode button upon the ring mode being changed.  This
        is broken out for specializations. """
        self.send_value(value, True)

    def _update_ring_mode(self):
        value_to_send = 0
        param = self.mapped_parameter()
        if self._property_to_map_to:
            param = self._property_to_map_to
        if self.is_mapped_manually():
            self.set_ring_mode(MappingType.MANUAL)
        elif live_object_is_valid(param):
            p_range = param.max - param.min
            if p_range > 0:
                value = parameter_value_to_midi_value(param.value, param.min, param.max)
                if param.min == -1 * param.max:
                    self.set_ring_mode(MappingType.BIPOLAR)
                elif parameter_is_quantized(param):
                    self.set_ring_mode(MappingType.QUANTIZED)
                else:
                    self.set_ring_mode(MappingType.NORMAL)
                value_to_send = int(value)
            else:
                self.set_ring_mode(MappingType.NONE)
        else:
            self.set_ring_mode(MappingType.NONE)
        self.send_value_on_ring_mode_change(value_to_send)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/RingedEncoderMixin.pyc
