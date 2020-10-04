# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\DisplayLineElement.py
# Compiled at: 2017-04-24 12:52:35
from _Framework import Task
from _Framework.NotifyingControlElement import NotifyingControlElement
CHARS_TO_REMOVE = (' ', 'I', 'i', 'O', 'o', 'U', 'u', 'E', 'e', 'A', 'a')
TRANSLATED_MESSAGES = {'Track Volume': 'Volume', 'Track Panning': 'Pan', 
   'Chain Volume': 'Volume', 
   'Chain Panorama': 'Pan', 
   'Chain Send 0': 'Send A', 
   'Chain Send 1': 'Send B', 
   'Chain Send 2': 'Send C', 
   'Chain Send 3': 'Send D', 
   'Chain Send 4': 'Send E', 
   'Crossfade': 'XFader', 
   'Preview Volume': 'Cue'}

def format_string(string, num_chars, should_center):
    """ Returns a cropped and optionally center formatted version of string. """
    if len(string) > 75:
        string = string[0:num_chars]
    if len(string) > num_chars:
        for um in CHARS_TO_REMOVE:
            while len(string) > num_chars and string.rfind(um, 1) != -1:
                um_pos = string.rfind(um, 1)
                string = string[:um_pos] + string[um_pos + 1:]

        if len(string) > num_chars:
            string = string[0:num_chars]
    else:
        string = string.center(num_chars) if should_center else string.ljust(num_chars)
    return string


def chunk_message(msg, segment_size, max_segments=4):
    """ Splits a line of strings into an array of chunks that can fit in display
    segments and returns it. """
    if len(msg) > segment_size:
        m_split = msg.split()
        chunks = []
        c = ''
        for m in m_split:
            if len(c) + len(m) < segment_size:
                c = '%s %s' % (c, m)
            else:
                chunks.append(('{:<{width}}').format(c, width=segment_size))
                c = m

        if c:
            chunks.append(('{:<{width}}').format(c, width=segment_size))
        if len(chunks) > max_segments:
            t_len = max_segments - 1
            trunc = chunks[:t_len]
            trunc.append(('').join(chunks[t_len:]))
            return trunc
        return chunks
    return [
     msg]


def format_message(a, segment_size):
    """ Formats the given array of messages into an array of segments that can fit in
    display segments and returns it. """
    num_segments = len(a)
    if num_segments == 1 or num_segments == 2 and not a[1]:
        return chunk_message(a[0], segment_size)
    if num_segments == 2:
        return [a[0]] + chunk_message(a[1], segment_size, max_segments=3)
    return a


class DisplayLineElement(NotifyingControlElement):
    """ DisplayLineElement handles a line in a physical display. """
    segment = 8
    double_segment = 16
    segment_offsets = ()
    double_segment_offsets = ()
    blank_line = ()
    translated_chars = {}

    def __init__(self, header, *a, **k):
        super(DisplayLineElement, self).__init__(*a, **k)
        self._header = header
        self._current_line = list(self.blank_line)
        self._momentary_line = []
        self._last_sent_message = None
        self._show_message_is_priority = False
        self._send_message_task = self._tasks.add(Task.run(self._send_message))
        self._send_message_task.kill()
        self._auto_revert_task = self._tasks.add(Task.sequence(Task.delay(15), self.revert))
        self._auto_revert_task.kill()
        return

    def disconnect(self):
        super(DisplayLineElement, self).disconnect()
        self.clear()
        self._momentary_line = None
        self._header = None
        self._current_line = None
        self._last_sent_message = None
        self._send_message_task = None
        self._auto_revert_task = None
        return

    def write(self, length, offset, message, clear=False, center=False, _=False):
        """ Writes the given message at the given offset and crops to the given length.
        Can also center string if specified. """
        self._show_message_is_priority = False
        self._current_line = self._do_write(self._current_line, length, offset, message, clear, center)
        self._request_send_message()

    def write_line(self, list_of_strings, center=False):
        """ Convenience method that takes a variable list of strings to write to this
        display line. """
        self._show_message_is_priority = False
        self.reset()
        for i, s in enumerate(list_of_strings):
            self.write(self.segment, self.segment_offsets[i], s, center=center)

    def write_momentary(self, length, offset, message, clear=False, center=False, auto_revert=False, is_priority=False):
        """ Momentarily writes the given message at the given offset and crops to the
        given length.  Call revert to reset back to default or use auto_revert.  Can also
        clear rest of line and center string if specified. """
        self._show_message_is_priority = is_priority
        self._momentary_line = self._do_write(self._momentary_line, length, offset, message, clear, center)
        self._request_send_message()
        self._auto_revert_task.kill()
        if auto_revert:
            self._auto_revert_task.restart()

    def show_message(self, *a, **k):
        """ Convenience method for use with ShowMessageMixin that takes a variable list
        of strings to momentarily write to this display line. This can prioritize the
        message via is_priority=True so that reset will not clear it. This can not
        auto_revert if revert=False. """
        self._show_message_is_priority = k.get('is_priority', False)
        can_revert = k.get('revert', True)
        self._momentary_line = []
        formatted = format_message(a, self.double_segment)
        if len(formatted) == 1 and not formatted[0]:
            self.revert(None)
            return
        else:
            last = len(formatted) - 1
            for i, msg in enumerate(formatted):
                should_format = len(msg) > 2
                center = i % 2 != 0 and should_format
                revert = i == last and can_revert
                if not center and should_format:
                    msg = ('{:>{width}}').format(msg, width=self.double_segment)
                self.write_momentary(self.double_segment, self.double_segment_offsets[i], msg, clear=True, center=center, auto_revert=revert, is_priority=self._show_message_is_priority)

            return

    def _do_write(self, var, length, offset, message, clear, center):
        """ Performs the actual write and returns modified variable to caller. """
        message = TRANSLATED_MESSAGES.get(message, message)
        new_chars = self._get_chars(format_string(message, length, center))
        if clear:
            var = list(self._momentary_line) if self._momentary_line else list(self.blank_line)
        else:
            if var != self._current_line:
                var = list(self._current_line)
            for index in xrange(length):
                var[offset + index] = new_chars[index]

        return var

    def reset(self):
        """ Clears the display line. """
        has_revert_task = self._auto_revert_task and self._auto_revert_task.is_running
        if not self._show_message_is_priority:
            self._momentary_line = []
            if has_revert_task:
                self._auto_revert_task.kill()
        self._current_line = list(self.blank_line)
        self._last_sent_message = None
        self._request_send_message()
        return

    def revert(self, _=None):
        """ Reverts momentary display back to default. """
        self._momentary_line = []
        self._last_sent_message = None
        self._show_message_is_priority = False
        self._request_send_message()
        return

    def clear(self):
        """ Clears the line. """
        raise NotImplementedError

    def _request_send_message(self):
        """ Requests that a message be sent and schedules it via Task. """
        if self._send_message_task:
            self._send_message_task.restart()

    def _send_message(self):
        """ Determines which message should be sent. """
        if self._momentary_line:
            self.send_midi(tuple(self._header + self._momentary_line + [247]))
        else:
            self.send_midi(tuple(self._header + self._current_line + [247]))

    def send_midi(self, midi_bytes):
        """ Sends the given bytes out if they aren't equal to the last sent bytes. """
        if midi_bytes != self._last_sent_message:
            self._send_midi(midi_bytes)
            self._last_sent_message = midi_bytes

    def _get_chars(self, string):
        """ Returns a list of ASCII values derived from string. """
        ascii = []
        for c in string:
            new_char = self.translated_chars.get(c, ord(c))
            if new_char > 127:
                new_char = 63
            ascii.append(new_char)

        return ascii
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/DisplayLineElement.pyc
