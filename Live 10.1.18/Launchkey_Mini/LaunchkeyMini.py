# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_Mini\LaunchkeyMini.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from Launchkey.Launchkey import Launchkey, LaunchkeyControlFactory, make_button

class LaunchkeyMiniControlFactory(LaunchkeyControlFactory):

    def create_next_track_button(self):
        return make_button(107, b'Next_Track_Button')

    def create_prev_track_button(self):
        return make_button(106, b'Prev_Track_Button')


class LaunchkeyMini(Launchkey):
    """ Script for Novation's Launchkey Mini keyboard """

    def __init__(self, c_instance):
        super(LaunchkeyMini, self).__init__(c_instance, control_factory=LaunchkeyMiniControlFactory(), identity_response=(240,
                                                                                                                          126,
                                                                                                                          127,
                                                                                                                          6,
                                                                                                                          2,
                                                                                                                          0,
                                                                                                                          32,
                                                                                                                          41,
                                                                                                                          53,
                                                                                                                          0,
                                                                                                                          0))
        self._suggested_input_port = b'LK Mini InControl'
        self._suggested_output_port = b'LK Mini InControl'

    def _setup_navigation(self):
        super(LaunchkeyMini, self)._setup_navigation()
        self._next_scene_button = make_button(105, b'Next_Scene_Button')
        self._prev_scene_button = make_button(104, b'Prev_Scene_Button')
        self._session_navigation.set_next_scene_button(self._next_scene_button)
        self._session_navigation.set_prev_scene_button(self._prev_scene_button)

    def _setup_transport(self):
        pass
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchkey_Mini/LaunchkeyMini.pyc
