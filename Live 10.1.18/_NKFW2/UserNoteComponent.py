# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\UserNoteComponent.py
# Compiled at: 2017-09-30 15:26:23
from AbstractInstrumentComponent import AbstractInstrumentComponent
from ControlUtils import reset_group_buttons, reset_button, assign_button_to_note
from Utils import parse_int

class UserNoteComponent(AbstractInstrumentComponent):
    """ UserNoteComponent allows arbitrary notes defined in a file to be assigned to a
    matrix.  The settings in the file should take the following form:

    ROW_x_BTN_x = color, channel, note_number """

    def __init__(self, color_class, scroll_button_color='Navigation.OctavesEnabled', handle_modifier_leds=True, target_clip_comp=None, quantize_comp=None, name='User_Note_Control', *a, **k):
        super(UserNoteComponent, self).__init__(scroll_button_color=scroll_button_color, handle_modifier_leds=handle_modifier_leds, target_clip_comp=target_clip_comp, quantize_comp=quantize_comp, name=name, *a, **k)
        self._color_dict = color_class.__dict__.keys() if color_class else None
        self._color_class_name = str(color_class).split('.')[(-1)] if color_class else ''
        self._matrix = None
        self._note_settings = {}
        return

    def disconnect(self):
        super(UserNoteComponent, self).disconnect()
        self._color_dict = None
        self._color_class_name = None
        self._matrix = None
        self._note_settings = None
        return

    def set_matrix(self, matrix):
        """ Sets the matrix to use for playing notes. """
        self._unused_pads = []
        self._used_pads = []
        matrix_to_reset = matrix if matrix else self._matrix
        reset_group_buttons(matrix_to_reset)
        self._matrix = matrix
        if matrix:
            self._assign_notes_to_matrix()

    def can_scroll_up(self):
        return False

    def can_scroll_down(self):
        return False

    def _can_scroll_octave(self, _):
        return False

    def reset(self):
        pass

    def should_enable_scroller(self):
        return False

    def parse_settings(self, settings):
        """ Parses the given dict of settings for button assignments. """
        parsed_settings = []
        self._note_settings = {}
        if settings:
            for k, v in settings.iteritems():
                coord = self._parse_button_coordinate(k)
                d = v.split(',')
                if coord != -1 and len(d) == 3:
                    color = self._parse_color_name(d[0])
                    channel = parse_int(d[1], default_value=9, min_value=9, max_value=16) - 1
                    note = parse_int(d[2], default_value=36, min_value=0, max_value=127)
                    if (
                     channel, note) not in parsed_settings:
                        parsed_settings.append((channel, note))
                        self._note_settings[coord] = {'color': color, 'channel': channel, 'note': note}

        self._assign_notes_to_matrix()

    def _parse_button_coordinate(self, setting_key):
        """ Parses the given key for the coordinate of the button that the settings
        relate to. """
        try:
            row = int(setting_key[4:5]) - 1
            column = int(setting_key[10:]) - 1
            return (row, column)
        except ValueError:
            self.canonical_parent.log_message('ValueError when parsing ' + 'UserNoteComponent settings.')
            return -1

    def _parse_color_name(self, color):
        """ Returns the full color name for the given color or a default color name if
        invalid color name. """
        color = color.upper().strip()
        if color in self._color_dict:
            return '%s.%s' % (self._color_class_name, color)
        return 'DefaultButton.On'

    def update(self):
        super(UserNoteComponent, self).update()
        self._assign_notes_to_matrix()

    def _assign_notes_to_matrix(self):
        if self.is_enabled() and self._matrix:
            self._used_pads = []
            self._unused_pads = []
            if self._note_settings:
                for btn, (column, row) in self._matrix.iterbuttons():
                    setting = self._note_settings.get((row, column), None)
                    if setting:
                        assign_button_to_note(btn, setting['note'], channel=setting['channel'], color=setting['color'])
                        self._used_pads.append(btn)
                    else:
                        reset_button(btn)
                        self._unused_pads.append(btn)

            else:
                reset_group_buttons(self._matrix)
                self._unused_pads = self._matrix
            self.handle_unused_pads()
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/UserNoteComponent.pyc
