# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\EncoderSensitivityMixin.py
# Compiled at: 2017-04-24 12:52:35
from _NKFW2.ControlUtils import parameter_is_quantized
from _NKFW2.consts import PARAM_REL_STEP
DEF_SENSITIVITY = 2.0
QNTZD_SENSITIVITY = 1.0 / 15.0
FINE_SENSITIVITY = 0.01
PROP_FINE_SENSITIVITY = PARAM_REL_STEP / 20.0

class EncoderSensitivityMixin(object):
    """ EncoderSensitivityMixin handles dynamically setting the sensitivity for an
    encoder to use. """

    def set_is_fine_tuning(self, is_fine_tuning):
        """ Sets whether the encoder should provide fine tuning. """
        self._set_sensitivity(self.parameter, is_fine_tuning)

    def set_property_to_map_to(self, prop):
        """ Extends standard to set mapping sensitivity. """
        super(EncoderSensitivityMixin, self).set_property_to_map_to(prop)
        self._set_sensitivity(prop)

    def connect_to(self, param):
        """ Extends standard to set mapping sensitivity. """
        super(EncoderSensitivityMixin, self).connect_to(param)
        self._set_sensitivity(param)

    def _set_sensitivity(self, param, fine=False):
        is_qntzd = parameter_is_quantized(param)
        if is_qntzd:
            sense = QNTZD_SENSITIVITY
        else:
            sense = FINE_SENSITIVITY if fine else DEF_SENSITIVITY
        self.mapping_sensitivity = sense
        if self._property_to_map_to and not is_qntzd:
            param.set_relative_step(PROP_FINE_SENSITIVITY if fine else PARAM_REL_STEP)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/EncoderSensitivityMixin.pyc
