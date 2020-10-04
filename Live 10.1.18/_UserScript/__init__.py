# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_UserScript\__init__.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from ConfigParser import ConfigParser
from _Generic.GenericScript import GenericScript
import Live
HIDE_SCRIPT = True

def interpret_map_mode(map_mode_name):
    result = Live.MidiMap.MapMode.absolute
    if map_mode_name == b'Absolute14Bit':
        result = Live.MidiMap.MapMode.absolute_14_bit
    elif map_mode_name == b'AccelSignedBit':
        result = Live.MidiMap.MapMode.relative_signed_bit
    elif map_mode_name == b'LinearSignedBit':
        result = Live.MidiMap.MapMode.relative_smooth_signed_bit
    elif map_mode_name == b'AccelSignedBit2':
        result = Live.MidiMap.MapMode.relative_signed_bit2
    elif map_mode_name == b'LinearSignedBit2':
        result = Live.MidiMap.MapMode.relative_smooth_signed_bit2
    elif map_mode_name == b'AccelBinaryOffset':
        result = Live.MidiMap.MapMode.relative_binary_offset
    elif map_mode_name == b'LinearBinaryOffset':
        result = Live.MidiMap.MapMode.relative_smooth_binary_offset
    elif map_mode_name == b'AccelTwoCompliment':
        result = Live.MidiMap.MapMode.relative_two_compliment
    elif map_mode_name == b'LinearTwoCompliment':
        result = Live.MidiMap.MapMode.relative_smooth_two_compliment
    return result


def create_instance(c_instance, user_path=b''):
    """ The generic script can be customised by using parameters.
        In this case, the user has written a text file with all necessary info.
        Here we read this file and fill the necessary data structures before
        instantiating the generic script.
    """
    device_map_mode = Live.MidiMap.MapMode.absolute
    volume_map_mode = Live.MidiMap.MapMode.absolute
    sends_map_mode = Live.MidiMap.MapMode.absolute
    if not user_path == b'':
        file_object = open(user_path)
        if file_object:
            file_data = None
            config_parser = ConfigParser()
            config_parser.readfp(file_object, user_path)
            device_controls = [
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1)]
            transport_controls = {b'STOP': -1, 
               b'PLAY': -1, 
               b'REC': -1, 
               b'LOOP': -1, 
               b'RWD': -1, 
               b'FFWD': -1}
            volume_controls = [
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1)]
            trackarm_controls = [
             -1, -1, -1, -1, -1, -1, -1, -1]
            bank_controls = {b'TOGGLELOCK': -1, 
               b'NEXTBANK': -1, 
               b'PREVBANK': -1, 
               b'BANK1': -1, 
               b'BANK2': -1, 
               b'BANK3': -1, 
               b'BANK4': -1, 
               b'BANK5': -1, 
               b'BANK6': -1, 
               b'BANK7': -1, 
               b'BANK8': -1}
            controller_descriptions = {b'INPUTPORT': b'', b'OUTPUTPORT': b'', b'CHANNEL': -1}
            mixer_options = {b'NUMSENDS': 2, 
               b'SEND1': [
                        -1, -1, -1, -1, -1, -1, -1, -1], 
               b'SEND2': [
                        -1, -1, -1, -1, -1, -1, -1, -1], 
               b'MASTERVOLUME': -1, 
               b'MASTERVOLUMECHANNEL': -1}
            for index in range(8):
                if config_parser.has_section(b'DeviceControls'):
                    encoder_tuple = [-1, -1]
                    option_name = b'Encoder' + str(index + 1)
                    if config_parser.has_option(b'DeviceControls', option_name):
                        option_value = config_parser.getint(b'DeviceControls', option_name)
                        if option_value in range(128):
                            encoder_tuple[0] = option_value
                    option_name = b'EncoderChannel' + str(index + 1)
                    if config_parser.has_option(b'DeviceControls', option_name):
                        option_value = config_parser.getint(b'DeviceControls', option_name)
                        if option_value in range(128):
                            encoder_tuple[1] = option_value
                    device_controls[index] = tuple(encoder_tuple)
                    option_name = b'Bank' + str(index + 1) + b'Button'
                    if config_parser.has_option(b'DeviceControls', option_name):
                        option_value = config_parser.getint(b'DeviceControls', option_name)
                        if option_value in range(128):
                            option_key = b'BANK' + str(index + 1)
                            bank_controls[option_key] = option_value
                if config_parser.has_section(b'MixerControls'):
                    volume_tuple = [-1, -1]
                    option_name = b'VolumeSlider' + str(index + 1)
                    if config_parser.has_option(b'MixerControls', option_name):
                        option_value = config_parser.getint(b'MixerControls', option_name)
                        if option_value in range(128):
                            volume_tuple[0] = option_value
                    option_name = b'Slider' + str(index + 1) + b'Channel'
                    if config_parser.has_option(b'MixerControls', option_name):
                        option_value = config_parser.getint(b'MixerControls', option_name)
                        if option_value in range(16):
                            volume_tuple[1] = option_value
                    volume_controls[index] = tuple(volume_tuple)
                    option_name = b'TrackArmButton' + str(index + 1)
                    if config_parser.has_option(b'MixerControls', option_name):
                        option_value = config_parser.getint(b'MixerControls', option_name)
                        if option_value in range(128):
                            trackarm_controls[index] = option_value
                    option_name = b'Send1Knob' + str(index + 1)
                    if config_parser.has_option(b'MixerControls', option_name):
                        option_value = config_parser.getint(b'MixerControls', option_name)
                        if option_value in range(128):
                            mixer_options[b'SEND1'][index] = option_value
                    option_name = b'Send2Knob' + str(index + 1)
                    if config_parser.has_option(b'MixerControls', option_name):
                        option_value = config_parser.getint(b'MixerControls', option_name)
                        if option_value in range(128):
                            mixer_options[b'SEND2'][index] = option_value
                if config_parser.has_section(b'Globals'):
                    if config_parser.has_option(b'Globals', b'GlobalChannel'):
                        option_value = config_parser.getint(b'Globals', b'GlobalChannel')
                        if option_value in range(16):
                            controller_descriptions[b'CHANNEL'] = option_value
                    if config_parser.has_option(b'Globals', b'InputName'):
                        controller_descriptions[b'INPUTPORT'] = config_parser.get(b'Globals', b'InputName')
                    if config_parser.has_option(b'Globals', b'OutputName'):
                        controller_descriptions[b'OUTPUTPORT'] = config_parser.get(b'Globals', b'OutputName')
                    pad_translation = []
                    for pad in range(16):
                        pad_info = []
                        note = -1
                        channel = -1
                        option_name = b'Pad' + str(pad + 1) + b'Note'
                        if config_parser.has_option(b'Globals', option_name):
                            note = config_parser.getint(b'Globals', option_name)
                            if note in range(128):
                                option_name = b'Pad' + str(pad + 1) + b'Channel'
                                if config_parser.has_option(b'Globals', option_name):
                                    channel = config_parser.getint(b'Globals', option_name)
                                if channel is -1 and controller_descriptions[b'CHANNEL'] is not -1:
                                    channel = controller_descriptions[b'CHANNEL']
                                if channel in range(16):
                                    pad_info.append(pad % 4)
                                    pad_info.append(int(pad / 4))
                                    pad_info.append(note)
                                    pad_info.append(channel)
                                    pad_translation.append(tuple(pad_info))

                    if len(pad_translation) > 0:
                        controller_descriptions[b'PAD_TRANSLATION'] = tuple(pad_translation)
                if config_parser.has_section(b'DeviceControls'):
                    if config_parser.has_option(b'DeviceControls', b'NextBankButton'):
                        option_value = config_parser.getint(b'DeviceControls', b'NextBankButton')
                        if option_value in range(128):
                            bank_controls[b'NEXTBANK'] = option_value
                    if config_parser.has_option(b'DeviceControls', b'PrevBankButton'):
                        option_value = config_parser.getint(b'DeviceControls', b'PrevBankButton')
                        if option_value in range(128):
                            bank_controls[b'PREVBANK'] = option_value
                    if config_parser.has_option(b'DeviceControls', b'LockButton'):
                        option_value = config_parser.getint(b'DeviceControls', b'LockButton')
                        if option_value in range(128):
                            bank_controls[b'TOGGLELOCK'] = option_value
                    if config_parser.has_option(b'DeviceControls', b'EncoderMapMode'):
                        device_map_mode = interpret_map_mode(config_parser.get(b'DeviceControls', b'EncoderMapMode'))
                if config_parser.has_section(b'MixerControls'):
                    if config_parser.has_option(b'MixerControls', b'MasterVolumeSlider'):
                        option_value = config_parser.getint(b'MixerControls', b'MasterVolumeSlider')
                        if option_value in range(128):
                            mixer_options[b'MASTERVOLUME'] = option_value
                    if config_parser.has_option(b'MixerControls', b'MasterSliderChannel'):
                        option_value = config_parser.getint(b'MixerControls', b'MasterSliderChannel')
                        if option_value in range(16):
                            mixer_options[b'MASTERVOLUMECHANNEL'] = option_value
                    if config_parser.has_option(b'MixerControls', b'VolumeMapMode'):
                        volume_map_mode = interpret_map_mode(config_parser.get(b'MixerControls', b'VolumeMapMode'))
                    if config_parser.has_option(b'MixerControls', b'SendsMapMode'):
                        sends_map_mode = interpret_map_mode(config_parser.get(b'MixerControls', b'SendsMapMode'))
                        mixer_options[b'SENDMAPMODE'] = sends_map_mode
                if config_parser.has_section(b'TransportControls'):
                    if config_parser.has_option(b'TransportControls', b'StopButton'):
                        option_value = config_parser.getint(b'TransportControls', b'StopButton')
                        if option_value in range(128):
                            transport_controls[b'STOP'] = option_value
                    if config_parser.has_option(b'TransportControls', b'PlayButton'):
                        option_value = config_parser.getint(b'TransportControls', b'PlayButton')
                        if option_value in range(128):
                            transport_controls[b'PLAY'] = option_value
                    if config_parser.has_option(b'TransportControls', b'RecButton'):
                        option_value = config_parser.getint(b'TransportControls', b'RecButton')
                        if option_value in range(128):
                            transport_controls[b'REC'] = option_value
                    if config_parser.has_option(b'TransportControls', b'LoopButton'):
                        option_value = config_parser.getint(b'TransportControls', b'LoopButton')
                        if option_value in range(128):
                            transport_controls[b'LOOP'] = option_value
                    if config_parser.has_option(b'TransportControls', b'RwdButton'):
                        option_value = config_parser.getint(b'TransportControls', b'RwdButton')
                        if option_value in range(128):
                            transport_controls[b'RWD'] = option_value
                    if config_parser.has_option(b'TransportControls', b'FfwdButton'):
                        option_value = config_parser.getint(b'TransportControls', b'FfwdButton')
                        if option_value in range(128):
                            transport_controls[b'FFWD'] = option_value

    return GenericScript(c_instance, device_map_mode, volume_map_mode, tuple(device_controls), transport_controls, tuple(volume_controls), tuple(trackarm_controls), bank_controls, controller_descriptions, mixer_options)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_UserScript/__init__.pyc
