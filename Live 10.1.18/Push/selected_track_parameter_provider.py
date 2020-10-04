# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\selected_track_parameter_provider.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import ParameterInfo
from pushbase.selected_track_parameter_provider import SelectedTrackParameterProvider as SelectedTrackParameterProviderBase
from .parameter_mapping_sensitivities import parameter_mapping_sensitivity, fine_grain_parameter_mapping_sensitivity

class SelectedTrackParameterProvider(SelectedTrackParameterProviderBase):

    def _create_parameter_info(self, parameter, name):
        assert name is not None
        return ParameterInfo(name=name, parameter=parameter, default_encoder_sensitivity=parameter_mapping_sensitivity(parameter), fine_grain_encoder_sensitivity=fine_grain_parameter_mapping_sensitivity(parameter))
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push/selected_track_parameter_provider.pyc
