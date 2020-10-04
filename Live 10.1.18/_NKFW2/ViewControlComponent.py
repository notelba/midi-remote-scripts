# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ViewControlComponent.py
# Compiled at: 2017-04-24 12:52:36
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _NKFW2.SpecialControl import SpecialButtonControl

class ViewControlComponent(ControlSurfaceComponent):
    """ ViewControlComponent provides controls for controlling views. """
    detail_button = SpecialButtonControl(color='View.DetailOff', on_color='View.DetailOn')
    clip_track_button = SpecialButtonControl(color='View.ClipOff', on_color='View.ClipOn')
    main_view_button = SpecialButtonControl(color='View.ArrangeOff', on_color='View.ArrangeOn')

    def __init__(self, name='View_Control', *a, **k):
        super(ViewControlComponent, self).__init__(name=name, *a, **k)
        app_view = self.application().view
        app_view.add_is_view_visible_listener('Detail', self._on_detail_view_changed)
        app_view.add_is_view_visible_listener('Detail/DeviceChain', self._on_device_view_changed)
        app_view.add_is_view_visible_listener('Detail/Clip', self._on_clip_view_changed)
        app_view.add_is_view_visible_listener('Arranger', self._on_main_view_changed)

    def disconnect(self):
        app_view = self.application().view
        if app_view.is_view_visible_has_listener('Detail', self._on_detail_view_changed):
            app_view.remove_is_view_visible_listener('Detail', self._on_detail_view_changed)
        if app_view.is_view_visible_has_listener('Detail/DeviceChain', self._on_device_view_changed):
            app_view.remove_is_view_visible_listener('Detail/DeviceChain', self._on_device_view_changed)
        if app_view.is_view_visible_has_listener('Detail/Clip', self._on_clip_view_changed):
            app_view.remove_is_view_visible_listener('Detail/Clip', self._on_clip_view_changed)
        if app_view.is_view_visible_has_listener('Arranger', self._on_main_view_changed):
            app_view.remove_is_view_visible_listener('Arranger', self._on_main_view_changed)
        super(ViewControlComponent, self).disconnect()

    @detail_button.pressed
    def detail_button(self, _):
        if self.application().view.is_view_visible('Detail'):
            self.application().view.hide_view('Detail')
        else:
            self.application().view.show_view('Detail')

    @clip_track_button.pressed
    def clip_track_button(self, _):
        self.application().view.show_view('Detail')
        if self.application().view.is_view_visible('Detail/DeviceChain'):
            self.application().view.show_view('Detail/Clip')
        else:
            self.application().view.show_view('Detail/DeviceChain')

    @main_view_button.pressed
    def main_view_button(self, _):
        if self.application().view.is_view_visible('Arranger'):
            self.application().view.show_view('Session')
        else:
            self.application().view.show_view('Arranger')

    def update(self):
        super(ViewControlComponent, self).update()
        self._on_detail_view_changed()
        self._on_clip_track_view_changed()
        self._on_main_view_changed()

    def _on_detail_view_changed(self):
        if self.is_enabled():
            self.detail_button.is_on = self.application().view.is_view_visible('Detail')

    def _on_clip_view_changed(self):
        self._on_clip_track_view_changed()

    def _on_device_view_changed(self):
        self._on_clip_track_view_changed()

    def _on_clip_track_view_changed(self):
        if self.is_enabled():
            self.clip_track_button.is_on = self.application().view.is_view_visible('Detail/Clip')

    def _on_main_view_changed(self):
        if self.is_enabled():
            self.main_view_button.is_on = self.application().view.is_view_visible('Arranger')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ViewControlComponent.pyc
