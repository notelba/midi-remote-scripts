# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ButtonSliderManager.py
# Compiled at: 2017-09-30 15:26:22
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
from _Framework.ModesComponent import AddLayerMode
from _Framework.Layer import Layer
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from SpecialButtonSliderElement import SpecialButtonSliderElement

class ButtonSliderManager(ControlSurfaceComponent):
    """ ButtonSliderManager manages a group of SpecialButtonSliderElements created from
    the given matrix. """

    def __init__(self, matrix, should_invert_buttons=True, default_smoothing_speed=2, velocity_sensitive=False, *a, **k):
        super(ButtonSliderManager, self).__init__(name='Button_Slider_Manager', *a, **k)
        self.is_private = True
        self._layers = []
        slider = SpecialButtonSliderElement
        w_range = xrange(matrix.width())
        self._default_colors = [ 'ButtonSlider.Slider' for _ in w_range ]
        slider_elements = [
         [ slider(should_invert_buttons=should_invert_buttons, default_smoothing_speed=default_smoothing_speed, velocity_sensitive=velocity_sensitive, name='Button_Sliders_%s' % i, inc_dec_colors=('ButtonSlider.IncDecOff',
                                                                                                                                                                                            'ButtonSlider.IncDecOn'), off_on_colors=('ButtonSlider.OffOnOff',
                                                                                                                                                                                                                                     'ButtonSlider.OffOnOn'), automat_clear_colors=('ButtonSlider.ClearOff',
                                                                                                                                                                                                                                                                                    'ButtonSlider.ClearOn'), slider_color='ButtonSlider.Slider', bipolar_color='ButtonSlider.Bipolar') for i in w_range
         ]]
        self._slider_elements = slider_elements[0]
        for index, element in enumerate(self._slider_elements):
            layer = Layer(buttons=matrix.submatrix[index:index + 1, :])
            self._layers.append(AddLayerMode(element, layer))

        self._slider_matrix = ButtonMatrixElement(rows=slider_elements, name='Button_Sliders')

    def disconnect(self):
        super(ButtonSliderManager, self).disconnect()
        self._layers = None
        self._default_colors = None
        self._slider_matrix = None
        return

    def get_layers(self):
        """ Returns the layers needed to set buttons of the matrix to the sliders. """
        return self._layers

    def get_matrix(self):
        """ Returns the matrix of sliders. """
        return self._slider_matrix

    def get_sliders(self):
        """ Returns the sliders as a list. """
        return self._slider_elements

    def set_shift_button(self, button):
        """ Sets the button to use for switching to/from fine tuning. """
        self._on_shift_button_value.subject = button

    def enable_fine_tune_and_reset(self, enable):
        """ Sets the enabled state of fine tuning for all sliders. """
        for slider in self._slider_elements:
            slider.enable_fine_tune_and_reset(enable)

    def _set_color(self, color):
        for slider in self._slider_elements:
            slider.set_slider_color(color)

    def _get_color(self):
        return 'ButtonSlider.Slider'

    color = property(_get_color, _set_color)

    def _set_colors(self, colors):
        for index, slider in enumerate(self._slider_elements):
            slider.set_slider_color(colors[index])

    def _get_colors(self):
        return self._default_colors

    colors = property(_get_colors, _set_colors)

    @subject_slot('value')
    def _on_shift_button_value(self, value):
        self.enable_fine_tune_and_reset(value is not 0)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ButtonSliderManager.pyc
