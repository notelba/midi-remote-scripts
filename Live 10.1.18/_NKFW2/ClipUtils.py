# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ClipUtils.py
# Compiled at: 2017-05-29 15:43:11
import Live
from Utils import format_absolute_time, get_name
from consts import MIDI_RANGE, NOTE_PITCH, NOTE_TIME, NOTE_LENGTH, NOTE_VELO, NOTE_MUTED, NOTE_TUPLE_RANGE, COMPOUND_NOTE_NAMES, MIN_CLIP_LOOP_LENGTH, DEF_SEQ_CLIP_LENGTH, SHARP_NOTES

def delete_clip(slot, show_message=None):
    """ Deletes the clip in the given slot. """
    if slot and slot.has_clip:
        name = get_name(slot.clip)
        slot.delete_clip()
        if show_message:
            show_message('Clip Deleted', name)


def duplicate_clip(song, clip, callback=None, show_message=None):
    """ Duplicates the clip, selects the duplicate and fires it if the clip that was
    duplicated was playing. This can also call a callback to announce that the clip has
    been duplicated. """
    try:
        track = clip.canonical_parent.canonical_parent
        current_slot_index = list(track.clip_slots).index(clip.canonical_parent)
        should_fire = clip.is_playing
        track.duplicate_clip_slot(current_slot_index)
        if callback:
            callback()
        duped_clip_slot = track.clip_slots[(current_slot_index + 1)]
        song.view.detail_clip = duped_clip_slot.clip
        if track.is_visible:
            song.view.highlighted_clip_slot = duped_clip_slot
        if should_fire:
            duped_clip_slot.fire(force_legato=True, launch_quantization=Live.Song.Quantization.q_no_q)
        if show_message:
            show_message('Clip Duplicated', get_name(clip))
    except:
        pass


def get_clip_long_name(song, clip):
    """ Returns the name of the clip if it isn't None or the empty_clip_name. """
    assert clip is None or isinstance(clip, Live.Clip.Clip)
    if clip:
        clip_name = '[unnamed]'
        if clip.name:
            clip_name = clip.name
    else:
        clip_name = get_empty_clip_name(song)
    return clip_name


def get_empty_clip_name(song):
    """ Returns the name of the selected scene for use in conjunction with
    get_clip_long_name. """
    if not isinstance(song, Live.Song.Song):
        raise AssertionError
        scene = song.view.selected_scene
        scene_name = scene.name
        scene_name = scene_name or str(list(song.scenes).index(scene) + 1)
    return '[none] - Sc: ' + scene_name


def get_end(clip):
    """ Returns the position of either the clip's end marker or its loop end,
    whichever is greater. """
    assert isinstance(clip, Live.Clip.Clip)
    return max(clip.end_marker, clip.loop_end)


def _move_loop(clip, start, end):
    """ Moves loop position in the correct order. """
    if start < clip.loop_end:
        clip.loop_start = start
        clip.loop_end = end
        clip.loop_start = start
    else:
        clip.loop_end = end
        clip.loop_start = start


def _move_markers(clip, start, end, move_start, move_end):
    """ Moves start/end markers (if elected) in the correct order. """
    if move_start or move_end:
        if start < clip.end_marker:
            if move_start:
                clip.start_marker = start
            if move_end:
                clip.end_marker = end
        else:
            if move_end:
                clip.end_marker = end
            if move_start:
                clip.start_marker = start


def apply_loop_settings(clip, loop_settings, move_start, move_end, zoom_loop):
    """ Ensures that loop settings (start, end) are possible and applies in correct order.
    Also moves start marker, end marker and shows loop if specified. This can also be
    used for moving start/end markers for non-looping clips. """
    assert isinstance(clip, Live.Clip.Clip)
    assert len(loop_settings) == 2
    move_start = bool(move_start)
    move_end = bool(move_end)
    zoom_loop = bool(zoom_loop)
    start = loop_settings[0]
    end = loop_settings[1]
    if not move_end and end > clip.end_marker:
        end = clip.end_marker
    if start < end:
        diff = end - start
        if diff < MIN_CLIP_LOOP_LENGTH:
            offset = MIN_CLIP_LOOP_LENGTH - diff
            if start > MIN_CLIP_LOOP_LENGTH:
                start -= offset
            else:
                end += offset
        _move_loop(clip, start, end)
        _move_markers(clip, start, end, move_start, move_end)
        if zoom_loop:
            clip.view.show_loop()
            clip.view.show_loop()


def can_clear_parameter_envelope(param):
    """ Returns whether or not automation can be cleared for the parameter. """
    if param:
        return param.automation_state != Live.DeviceParameter.AutomationState.none
    return False


def clear_parameter_envelope(clip, param):
    """ Clears envelope for the given parameter from the given clip. """
    assert isinstance(clip, Live.Clip.Clip)
    assert param is None or isinstance(param, Live.DeviceParameter.DeviceParameter)
    if param:
        clip.clear_envelope(param)
    return


def get_playing_clip(song, track=None):
    """ Returns the clip playing on the selected or specified track or none. """
    assert isinstance(song, Live.Song.Song)
    assert track is None or isinstance(track, Live.Track.Track)
    if track is None:
        track = song.view.selected_track
    if track in song.tracks:
        slot_index = track.playing_slot_index
        if slot_index >= 0:
            return track.clip_slots[slot_index].clip
    return


def create_sequence_clip(app, track=None):
    """ Creates and returns a new clip in the selected slot on the selected or specified
    track to use for step-sequencing.  This will also launch the clip, display detail
    view and autoname the clip."""
    if not isinstance(app, Live.Application.Application):
        raise AssertionError
        assert track is None or isinstance(track, Live.Track.Track)
        song = app.get_document()
        if track is None:
            track = song.view.selected_track
        if track.has_midi_input:
            scene_index = list(song.scenes).index(song.view.selected_scene)
            slot = track.clip_slots[scene_index]
            song.view.highlighted_clip_slot = slot.has_clip or slot
            app.view.show_view('Detail/Clip')
            slot.create_clip(DEF_SEQ_CLIP_LENGTH)
            song.view.detail_clip = slot.clip
            slot.clip.name = '%s %s' % (scene_index + 1, track.name)
            slot.fire()
        return slot.clip
    else:
        return


def double_clip(clip, show_message=None):
    """ Doubles the given clip (for MIDI clips only). """
    try:
        c_len = clip.length * 2
        clip.duplicate_loop()
        if show_message:
            show_message('New Loop Length', format_absolute_time(clip, c_len, base_is_one=False))
    except:
        pass


def get_all_notes(clip):
    """ Returns all the notes in the given clip. This uses unrealistic time range to
    account for notes that fall outside of 1.1.1/the clip's end. """
    assert clip is None or clip.is_midi_clip
    all_notes = []
    if clip:
        all_notes = clip.get_notes(-100000000.0, 0, 999999999.0, 128)
    return all_notes


def get_note_lane(clip, pitch):
    """ Returns an entire note lane for editing. This uses unrealistic time range to
    account for notes that fall outside of 1.1.1/the clip's end. """
    assert clip is None or clip.is_midi_clip
    assert pitch in MIDI_RANGE
    lane = []
    if clip:
        lane = clip.get_notes(-100000000.0, pitch, 999999999.0, 1)
    return lane


def get_pitch_list(clip):
    """ Returns a sorted list of unique pitches in the clip. """
    assert clip is None or clip.is_midi_clip
    all_notes = []
    if clip:
        notes = clip.get_notes(-100000000.0, 0, 999999999.0, 128)
        all_notes = list(set([ n[NOTE_PITCH] for n in notes ]))
        all_notes.sort()
    return all_notes


def pitch_is_sharp(pitch):
    """ Returns whether the given pitch is sharp/flat. """
    return pitch % 12 in SHARP_NOTES


def mute_note_lane(clip, pitch, status=None):
    """ Mutes/unmutes all the notes in the given lane. If status is passed, will
    explicitly set mute state. """
    assert clip.is_midi_clip
    assert pitch in MIDI_RANGE
    lane = get_note_lane(clip, pitch)
    if status is not None:
        status_to_set = bool(status)
    else:
        status_to_set = not note_lane_is_muted(lane, pitch)
    for note in lane:
        clip.set_notes((
         (note[NOTE_PITCH], note[NOTE_TIME], note[NOTE_LENGTH],
          note[NOTE_VELO], status_to_set),))

    return


def solo_note_lane(clip, pitch):
    """ Solos/unsolo the given pitch by muting/unmuting all others. """
    assert clip.is_midi_clip
    assert pitch in MIDI_RANGE
    all_notes = get_all_notes(clip)
    should_solo = not note_lane_is_soloed(all_notes, pitch)
    for note in all_notes:
        clip.set_notes((
         (note[NOTE_PITCH], note[NOTE_TIME], note[NOTE_LENGTH],
          note[NOTE_VELO], note[NOTE_PITCH] != pitch and should_solo),))


def delete_note_lane(clip, pitch):
    """ Deletes the given pitch from the clip. """
    assert clip.is_midi_clip
    assert pitch in MIDI_RANGE
    clip.remove_notes(-100000000.0, pitch, 999999999.0, 1)


def delete_all_notes(clip):
    """ Deletes all of the notes from the clip. """
    assert clip.is_midi_clip
    clip.remove_notes(-100000000.0, 0, 999999999.0, 128)


def select_notes(clip, notes_to_select, _=None):
    """ Selects the given notes in the clip by deselecting all other notes, but only if
    the notes are not already selected. Args is needed for compatibility with tasks. """
    if not clip.is_midi_clip:
        raise AssertionError
        assert isinstance(notes_to_select, (tuple, list))
        current_selection = clip.get_selected_notes()
        selection_equal = len(current_selection) == len(notes_to_select)
        if selection_equal:
            for note in notes_to_select:
                if note not in current_selection:
                    selection_equal = False
                    break

        all_notes = selection_equal or get_all_notes(clip)
        unselected_notes = []
        for note in all_notes:
            if note not in notes_to_select:
                unselected_notes.append(note)

        clip.select_all_notes()
        clip.replace_selected_notes(tuple(unselected_notes))
        clip.deselect_all_notes()
        clip.set_notes(tuple(notes_to_select))


def notes_are_equal(note_a, note_b):
    """ Returns whether or not the given notes are equal to each other. For time and
    length, it's not possible to check equality as they're float values, so we just check
    that they're close. """
    assert isinstance(note_a, tuple)
    assert isinstance(note_b, tuple)
    for index in NOTE_TUPLE_RANGE:
        if index == NOTE_TIME or index == NOTE_LENGTH:
            diff = abs(note_a[index] - note_b[index])
            if diff > 1e-10:
                return False
        elif note_a[index] != note_b[index]:
            return False

    return True


def position_has_pitch(notes, pitch, start_pos, end_pos, notes_to_exclude=None):
    """ Returns whether or not a pitch exists in the given position range in the given
    list/tuple of notes. A list/tuple of notes to exclude can also be specified so that
    they aren't considered in comparisons. """
    assert isinstance(notes, (tuple, list))
    assert pitch in MIDI_RANGE
    assert isinstance(start_pos, float)
    assert isinstance(end_pos, float)
    assert notes_to_exclude is None or isinstance(notes_to_exclude, (tuple, list))
    for note in notes:
        if notes_to_exclude is None or note not in notes_to_exclude:
            if note[NOTE_PITCH] == pitch:
                if start_pos <= note[NOTE_TIME] < end_pos:
                    return True
                note_end = note[NOTE_TIME] + note[NOTE_LENGTH]
                if start_pos < note_end <= end_pos:
                    return True

    return False


def get_index_of_note_event(notes, note_event):
    """ Returns the index of the given note event in the the given list/tuple of notes.
        Returns 0 if not found. """
    assert isinstance(notes, (tuple, list))
    assert note_event is None or isinstance(note_event, tuple)
    if note_event:
        for index, note in enumerate(notes):
            if notes_are_equal(note, note_event):
                return index

    return 0


def get_notes_at_position(notes, position, resolution):
    """ Returns the list of notes at the given position within the given resolution value.
        Returns an empty list if none found. """
    assert notes is None or isinstance(notes, (tuple, list))
    assert isinstance(position, float)
    assert isinstance(resolution, float)
    notes_at_pos = []
    if notes:
        offset = resolution * 0.25
        start = min(position, position - offset)
        pos_range = position + resolution - offset
        for note in notes:
            if start <= note[NOTE_TIME] < pos_range:
                notes_at_pos.append(note)

    return notes_at_pos


def note_lane_is_muted(notes, pitch):
    """ Returns whether or not the lane has any muted notes in it. """
    assert notes is None or isinstance(notes, (tuple, list))
    assert pitch in MIDI_RANGE
    for note in notes:
        if note[NOTE_PITCH] == pitch:
            if note[NOTE_MUTED]:
                return True

    return False


def note_lane_is_soloed(notes, pitch):
    """ Returns whether or not the lane is soloed. This is determined by whether the lane
    has any muted notes and whether other lanes have any unmuted notes. """
    assert notes is None or isinstance(notes, (tuple, list))
    assert pitch in MIDI_RANGE
    for note in notes:
        if note[NOTE_PITCH] == pitch:
            if note[NOTE_MUTED]:
                return False
        elif not note[NOTE_MUTED]:
            return False

    return True


def get_pitch_range_as_string(pitches):
    """ Returns a string that lists the lowest and highest pitch names in the given
    pitches (which is expected to be a unique list). This will return an empty string if
    there aren't at least two valid pitches. """
    valid_pitches = [ p for p in pitches if p in MIDI_RANGE ]
    valid_pitches.sort()
    if len(valid_pitches) > 1:
        return '%s - %s' % (convert_to_note_name(valid_pitches[0]),
         convert_to_note_name(valid_pitches[(-1)]))
    return ''


def convert_to_note_name(note_num, note_names_to_use=COMPOUND_NOTE_NAMES):
    """ Returns a string representing the note name of the given note number.
    By default, this will use the COMPOUND_NOTE_NAMES defined in consts with accidentals
    represented as flats and sharps, but alternate tuples/lists can be passed in. """
    assert note_num in MIDI_RANGE
    assert len(note_names_to_use) == 12
    return note_names_to_use[(note_num % 12)] + str(note_num / 12 - 2)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ClipUtils.pyc
