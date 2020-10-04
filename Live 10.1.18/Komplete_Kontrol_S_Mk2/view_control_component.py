# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk2\view_control_component.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import BasicTrackScroller, BasicSceneScroller
from ableton.v2.control_surface.control import SendValueEncoderControl

class ViewControlComponent(Component):
    track_encoder = SendValueEncoderControl()
    scene_encoder = SendValueEncoderControl()

    def __init__(self, *a, **k):
        super(ViewControlComponent, self).__init__(*a, **k)
        self._track_scroller = BasicTrackScroller()
        self._scene_scroller = BasicSceneScroller()
        song = self.song
        view = song.view
        self.register_slot(song, self._update_track_encoder, b'visible_tracks')
        self.register_slot(song, self._update_track_encoder, b'return_tracks')
        self.register_slot(view, self._update_track_encoder, b'selected_track')
        self.register_slot(song, self._update_scene_encoder, b'scenes')
        self.register_slot(view, self._update_scene_encoder, b'selected_scene')

    @track_encoder.value
    def track_encoder(self, value, _):
        self._do_scroll(value, self._track_scroller)

    @scene_encoder.value
    def scene_encoder(self, value, _):
        self._do_scroll(value, self._scene_scroller)

    def _do_scroll(self, value, scroller):
        if value < 0:
            scroller.scroll_up()
        else:
            scroller.scroll_down()

    def update(self):
        super(ViewControlComponent, self).update()
        self._update_track_encoder()
        self._update_scene_encoder()

    def _update_track_encoder(self):
        if self.is_enabled():
            self.track_encoder.value = int(self._track_scroller.can_scroll_up()) ^ int(self._track_scroller.can_scroll_down() << 1)

    def _update_scene_encoder(self):
        if self.is_enabled():
            self.scene_encoder.value = int(self._scene_scroller.can_scroll_up()) ^ int(self._scene_scroller.can_scroll_down() << 1)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Komplete_Kontrol_S_Mk2/view_control_component.pyc
