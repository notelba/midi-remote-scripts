# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\channel_eq.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData
from .visualisation_settings import VisualisationGuides

class ChannelEqDeviceComponent(DeviceComponentWithTrackColorViewData):
    VISUALISATION_POSITION = ButtonRange(1, 6)
    FILTER_PARAMETERS = [b'Highpass On', b'Low', b'Mid', b'Mid Freq', b'High']

    def _parameter_touched(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    def _parameter_released(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    @property
    def _adjustment_view_data(self):
        adjusting_filter = False
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed
                             ]
        for parameter in touched_parameters:
            if parameter.name in self.FILTER_PARAMETERS:
                adjusting_filter = True
                break

        return {b'AdjustingFilter': adjusting_filter}

    @property
    def _visualisation_visible(self):
        return True

    @property
    def _shrink_parameters(self):

        def is_shrunk(parameter_index):
            return self.VISUALISATION_POSITION.left_index <= parameter_index <= self.VISUALISATION_POSITION.right_index

        return [ is_shrunk(parameter_index) for parameter_index in range(8) ]

    @property
    def _get_current_view_data(self):
        position = self.VISUALISATION_POSITION
        start_position_in_px = VisualisationGuides.light_left_x(position.left_index)
        end_position_in_px = VisualisationGuides.light_right_x(position.right_index)
        return {b'VisualisationStart': start_position_in_px, 
           b'VisualisationWidth': end_position_in_px - start_position_in_px, 
           b'AdjustingFilter': False}

    def _initial_visualisation_view_data(self):
        view_data = super(ChannelEqDeviceComponent, self)._initial_visualisation_view_data()
        view_data.update(self._get_current_view_data)
        view_data.update(self._adjustment_view_data)
        return view_data
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push2/channel_eq.pyc
