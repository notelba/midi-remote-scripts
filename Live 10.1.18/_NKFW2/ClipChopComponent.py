# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ClipChopComponent.py
# Compiled at: 2017-03-07 13:28:52
from ClipPositionComponent import ClipPositionComponent
from LaunchQuantizeComponent import LaunchQuantizeComponent

class ClipChopComponent(ClipPositionComponent):
    """ ClipChopComponent utilizes a group of buttons to chop a clip by moving
    its start marker. """

    def __init__(self, qntz_component, playhead_color='Clip.Playhead.Even', target_clip_comp=None, name='Clip_Matrix_Chop_Control', *a, **k):
        assert isinstance(qntz_component, LaunchQuantizeComponent)
        super(ClipChopComponent, self).__init__(playhead_color=playhead_color, target_clip_comp=target_clip_comp, off_method=self.perform_off_action, name=name, *a, **k)
        self._quantize_component = qntz_component

    def disconnect(self):
        super(ClipChopComponent, self).disconnect()
        self._quantize_component = None
        return

    def perform_position_action(self, position):
        last_qntz = int(self.song().clip_trigger_quantization)
        self.song().clip_trigger_quantization = self._quantize_component.quantization
        if self._clip.looping:
            self._clip.start_marker = position
        else:
            self._clip.loop_start = position
        self._clip.set_fire_button_state(1)
        self.song().clip_trigger_quantization = last_qntz

    def perform_off_action(self):
        self._clip.set_fire_button_state(0)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ClipChopComponent.pyc
