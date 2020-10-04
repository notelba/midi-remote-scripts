# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ControlSurfaceBase.py
# Compiled at: 2018-06-18 14:25:00
"""
# Copyright (C) 2015-2018 Stray <stray411@hotmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For questions regarding this module contact
# Stray <stray411@hotmail.com>
"""
from __future__ import with_statement
import Live, sys, logging
logger = logging.getLogger(__name__)
from _Framework.ControlSurface import OptimizedControlSurface
from _Framework.SubjectSlot import subject_slot
from Utils import parse_file, date_has_passed
LIVE_MAJOR_VERSION = Live.Application.get_application().get_major_version()
if LIVE_MAJOR_VERSION == 9:
    from _Framework.M4LInterfaceComponent import M4LInterfaceComponent
VERSION = 'v1.1.5'
SYSEX_ID_REQ = (240, 126, 127, 6, 1, 247)
MAX_REQUESTS = 10

class ControlSurfaceBase(OptimizedControlSurface):
    """ ControlSurfaceBase is the base class for a control surface that contains some of
    the basic plumbing that all scripts need.

    If the connects_to arg is used, the class must implement a method named
    handle_script_connections that takes a dict of scripts arg.  Alternatively, the class
    can override connect_script_instances in which case handle_script_connections will
    never be called. """

    def __init__(self, c_instance, name, connects_to=(), expiry=(), *a, **k):
        self._script_name = name
        self._connects_to = connects_to
        self._request_count = 0
        super(ControlSurfaceBase, self).__init__(c_instance, *a, **k)
        self._has_been_identified = not self.needs_identification()
        self._suppress_send_midi = not self._has_been_identified
        if expiry and date_has_passed(expiry):
            self.log_message('%s beta has expired!' % name)
            self.show_message('%s beta has expired!' % name)
            self.disconnect()
            return
        if self.has_control_track():
            self.set_feedback_channels(self.feedback_channels())

    def disconnect(self):
        super(ControlSurfaceBase, self).disconnect()
        self._connects_to = None
        return

    def set_targets_component(self, targets_comp):
        """ Sets the target component to use for updating device selection. """
        self._on_target_track_changed.subject = targets_comp
        self._on_target_track_changed(targets_comp.target_track)

    def notify_startup(self, script_version):
        """ Prints the script-related info to Live's log and status bar and sets up
        the script's M4L interface.  This should be called once the script is completely
        set up. """
        script_default = '%s: %s for Live' % (self._script_name, script_version)
        live = Live.Application.get_application()
        self.log_message('NK LOG ------- ' + '%s -- NKFW2: %s ------- Live: %d.%d.%d ------- END LOG' % (
         script_default, VERSION, LIVE_MAJOR_VERSION,
         live.get_minor_version(), live.get_bugfix_version()))
        self.show_message(script_default)
        with self.component_guard():
            self._create_m4l_interface()

    def connect_script_instances(self, instantiated_scripts):
        """ Overrides standard to connect to any scripts that were passed to __init__.
        Will call handle_script_connections with a dict of located scripts. """
        if self._connects_to:
            instances = {}
            for script in instantiated_scripts:
                name = script.__class__.__name__
                if name in self._connects_to:
                    instances[name] = script

            self.handle_script_connections(instances)

    def handle_sysex(self, midi_bytes):
        """ Overrides standard to handle controller identification if applicable. """
        if not self._has_been_identified:
            if self.is_identity_response(midi_bytes):
                self._has_been_identified = True
                self._suppress_send_midi = False
                self.on_identified()
                self.schedule_message(1, self.refresh_state)

    def port_settings_changed(self):
        """ Called when port settings change to request_identification if applicable
        or just refresh state. """
        self._request_count = 0
        if self.needs_identification():
            self._has_been_identified = False
            self._suppress_send_midi = True
            self.request_identification()
        else:
            self.schedule_message(1, self.refresh_state)

    def request_identification(self):
        """ Sends ID request and schedules message to call this method again and do
        so repeatedly until handshake succeeds or MAX_REQUESTS have been sent. """
        if not self._has_been_identified and self._request_count < MAX_REQUESTS:
            self._send_midi(SYSEX_ID_REQ)
            self.schedule_message(2, self.request_identification)
            self._request_count += 1

    def needs_identification(self):
        """ Returns whether the controller needs identification.  If this is overridden,
        the class must implement a method named on_identified that will be called once
        the controller has been identified and before a refresh has been scheduled.
        Alternatively, the class can override handle_sysex in which case on_identified
        will never be called. """
        return False

    def is_identity_response(self, midi_bytes):
        """ Returns whether the given MIDI bytes are likely an identity response.
        This can be overridden to provide specialized handling. """
        return midi_bytes[3:5] == (6, 2)

    def has_control_track(self):
        """ Returns whether the controller can control and provide
        feedback from tracks. """
        return False

    def feedback_channels(self):
        """ The list of feedback channels that should be used. """
        return []

    @staticmethod
    def script_path():
        """ Returns the absolute path to MRS directory containing this script. """
        mrs_path = ''
        for path in sys.path:
            if 'MIDI Remote Scripts' in path:
                mrs_path = path
                break

        return '%s/' % mrs_path

    def parse_file(self, file_name, parent_path=None, script_name=None, to_upper=True):
        """ Convenience method that calculates file paths automatically. For more
        advanced parsing, use Utils.parse_file. """
        if parent_path:
            f_path = parent_path
        else:
            f_path = self.script_path() + '/' + (script_name or self._script_name)
        return parse_file(file_name, f_path, logger=self.log_message, to_upper=to_upper)

    def log_message(self, *message):
        """ Overrides standard to use logger instead of c_instance. """
        try:
            message = '(%s) %s' % (self.__class__.__name__,
             (' ').join(map(str, message)))
            logger.info(message)
        except:
            logger.info('Logging encountered illegal character(s)!')

    @staticmethod
    def get_logger():
        """ Returns this script's logger object. """
        return logger

    def _send_midi(self, midi_event_bytes, optimized=True):
        """ Extends standard to not do anything if suppressing unless the event is
        SysEx. """
        if not self._suppress_send_midi or midi_event_bytes == SYSEX_ID_REQ:
            super(ControlSurfaceBase, self)._send_midi(midi_event_bytes, optimized)

    @subject_slot('target_track')
    def _on_target_track_changed(self, track):
        if self.has_control_track():
            self.release_controlled_track()
            self.set_controlled_track(track)

    def _create_m4l_interface(self):
        """ Creates and sets up the M4L interface for easy interaction
        from M4L devices. """
        if LIVE_MAJOR_VERSION > 9:
            return
        self._m4l_interface = M4LInterfaceComponent(controls=self.controls, component_guard=self.component_guard, priority=1)
        self._m4l_interface.name = 'M4L_Interface'
        self._m4l_interface.is_private = True
        self.get_control_names = self._m4l_interface.get_control_names
        self.get_control = self._m4l_interface.get_control
        self.grab_control = self._m4l_interface.grab_control
        self.release_control = self._m4l_interface.release_control
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ControlSurfaceBase.pyc
