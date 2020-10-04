# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\device_parameter_icons.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
IMAGE_ID_TO_FILENAME = {b'amp_bass': ('amp_bass.svg', ''), 
   b'amp_blues': ('amp_blues.svg', ''), 
   b'amp_boost': ('amp_boost.svg', ''), 
   b'amp_clean': ('amp_clean.svg', ''), 
   b'amp_heavy': ('amp_heavy.svg', ''), 
   b'amp_lead': ('amp_lead.svg', ''), 
   b'amp_rock': ('amp_rock.svg', ''), 
   b'armed': ('armed.svg', ''), 
   b'cabinet_1x12': ('cabinet_1x12.svg', ''), 
   b'cabinet_2x12': ('cabinet_2x12.svg', ''), 
   b'cabinet_4x10': ('cabinet_4x10.svg', ''), 
   b'cabinet_4x10bass': ('cabinet_4x10bass.svg', ''), 
   b'cabinet_4x12': ('cabinet_4x12.svg', ''), 
   b'cancel_x': ('cancel_x.svg', ''), 
   b'circuit_clean': ('circuit_clean.svg', ''), 
   b'circuit_ms2': ('circuit_ms2.svg', ''), 
   b'circuit_osr': ('circuit_osr.svg', ''), 
   b'circuit_prd': ('circuit_prd.svg', ''), 
   b'circuit_smp': ('circuit_smp.svg', ''), 
   b'co_beam': ('co_beam.svg', ''), 
   b'co_marimba': ('co_marimba.svg', ''), 
   b'co_membrane': ('co_membrane.svg', ''), 
   b'co_pipe': ('co_pipe.svg', ''), 
   b'co_plate': ('co_plate.svg', ''), 
   b'co_string': ('co_string.svg', ''), 
   b'co_tube': ('co_tube.svg', ''), 
   b'compressor_expand': ('compressor_expand.svg', ''), 
   b'compressor_peak': ('compressor_peak.svg', ''), 
   b'compressor_rms': ('compressor_rms.svg', ''), 
   b'control_off': ('control_off.svg', ''), 
   b'control_on': ('control_on.svg', ''), 
   b'delay_16th_1': ('delay_16th_1.svg', ''), 
   b'delay_16th_2': ('delay_16th_2.svg', ''), 
   b'delay_16th_3': ('delay_16th_3.svg', ''), 
   b'delay_16th_4': ('delay_16th_4.svg', ''), 
   b'delay_16th_5': ('delay_16th_5.svg', ''), 
   b'delay_16th_6': ('delay_16th_6.svg', ''), 
   b'delay_16th_8': ('delay_16th_8.svg', ''), 
   b'delay_16th_16': ('delay_16th_16.svg', ''), 
   b'delay_pingping_on': ('delay_pingping_on.svg', ''), 
   b'delay_pingping_off': ('delay_pingping_off.svg', ''), 
   b'device_pad': ('device_pad.svg', ''), 
   b'device_rack_drum': ('device_rack_drum.svg', ''), 
   b'device_rack_effect': ('device_rack_effect.svg', ''), 
   b'device_rack_instrument': ('device_rack_instrument.svg', ''), 
   b'drumbuss_soft': ('drumbuss_soft.svg', ''), 
   b'drumbuss_medium': ('drumbuss_medium.svg', ''), 
   b'drumbuss_hard': ('drumbuss_hard.svg', ''), 
   b'echo_16th': ('echo_16th.svg', ''), 
   b'echo_dotted': ('echo_dotted.svg', ''), 
   b'echo_note': ('echo_note.svg', ''), 
   b'echo_triplet': ('echo_triplet.svg', ''), 
   b'eq8_band1': ('eq8_band1.svg', ''), 
   b'eq8_band2': ('eq8_band2.svg', ''), 
   b'eq8_band3': ('eq8_band3.svg', ''), 
   b'eq8_band4': ('eq8_band4.svg', ''), 
   b'eq8_band5': ('eq8_band5.svg', ''), 
   b'eq8_band6': ('eq8_band6.svg', ''), 
   b'eq8_band7': ('eq8_band7.svg', ''), 
   b'eq8_band8': ('eq8_band8.svg', ''), 
   b'filter_band_12': ('filter_band_12.svg', '12BandPass_small.svg'), 
   b'filter_band_24': ('filter_band_24.svg', '24BandPass_small.svg'), 
   b'filter_band_6': ('filter_band_6.svg', ''), 
   b'filter_band_ladr': ('filter_band_ladr.svg', ''), 
   b'filter_band_ms2': ('filter_band_ms2.svg', ''), 
   b'filter_band_osr': ('filter_band_osr.svg', ''), 
   b'filter_band_prd': ('filter_band_prd.svg', ''), 
   b'filter_band_svf': ('filter_band_svf.svg', ''), 
   b'filter_bell': ('filter_bell.svg', 'Bell_small.svg'), 
   b'filter_formant_12': ('filter_formant_12.svg', ''), 
   b'filter_formant_6': ('filter_formant_6.svg', ''), 
   b'filter_high_12': ('filter_high_12.svg', '12HighPass_small.svg'), 
   b'filter_high_24': ('filter_high_24.svg', '24HighPass_small.svg'), 
   b'filter_high_48': ('filter_high_48.svg', '24HighPass_small.svg'), 
   b'filter_high_ladr': ('filter_high_ladr.svg', ''), 
   b'filter_high_ms2': ('filter_high_ms2.svg', ''), 
   b'filter_high_osr': ('filter_high_osr.svg', ''), 
   b'filter_high_prd': ('filter_high_prd.svg', ''), 
   b'filter_high_shelf': ('filter_high_shelf.svg', 'HighShelf_small.svg'), 
   b'filter_high_svf': ('filter_high_svf.svg', ''), 
   b'filter_low_12': ('filter_low_12.svg', '12LowPass_small.svg'), 
   b'filter_low_24': ('filter_low_24.svg', '24LowPass_small.svg'), 
   b'filter_low_48': ('filter_low_24.svg', '24LowPass_small.svg'), 
   b'filter_low_ladr': ('filter_low_ladr.svg', ''), 
   b'filter_low_ms2': ('filter_low_ms2.svg', ''), 
   b'filter_low_osr': ('filter_low_osr.svg', ''), 
   b'filter_low_prd': ('filter_low_prd.svg', ''), 
   b'filter_low_shelf': ('filter_low_shelf.svg', 'LowShelf_small.svg'), 
   b'filter_low_svf': ('filter_low_svf.svg', ''), 
   b'filter_morph_12': ('filter_morph_12.svg', '12Morph_small.svg'), 
   b'filter_morph_24': ('filter_morph_24.svg', '24Morph_small.svg'), 
   b'filter_notch_12': ('filter_notch_12.svg', '12Notch_small.svg'), 
   b'filter_notch_24': ('filter_notch_24.svg', '24Notch_small.svg'), 
   b'icon_horizontal1': ('icon_horizontal1.svg', ''), 
   b'icon_horizontal15': ('icon_horizontal15.svg', ''), 
   b'lfo_free': ('lfo_free.svg', ''), 
   b'lfo_phase': ('lfo_phase.svg', ''), 
   b'lfo_spin': ('lfo_spin.svg', ''), 
   b'lfo_sync': ('lfo_sync.svg', ''), 
   b'lfo_sine_small': ('', 'lfo_sine_small.svg'), 
   b'lfo_triangle_small': ('', 'lfo_triangle_small.svg'), 
   b'lfo_saw_up_small': ('', 'lfo_saw_up_small.svg'), 
   b'lfo_saw_down_small': ('', 'lfo_saw_down_small.svg'), 
   b'lfo_square_small': ('', 'lfo_square_small.svg'), 
   b'lfo_random_small': ('', 'lfo_random_small.svg'), 
   b'mic_condenser': ('mic_condenser.svg', ''), 
   b'mic_dynamic': ('mic_dynamic.svg', ''), 
   b'mic_far': ('mic_far.svg', ''), 
   b'mic_nearoff': ('mic_nearoff.svg', ''), 
   b'mic_nearon': ('mic_nearon.svg', ''), 
   b'osc_a': ('osc_a.svg', ''), 
   b'osc_alg_1': ('osc_alg_1.svg', ''), 
   b'osc_alg_10': ('osc_alg_10.svg', ''), 
   b'osc_alg_11': ('osc_alg_11.svg', ''), 
   b'osc_alg_2': ('osc_alg_2.svg', ''), 
   b'osc_alg_3': ('osc_alg_3.svg', ''), 
   b'osc_alg_4': ('osc_alg_4.svg', ''), 
   b'osc_alg_5': ('osc_alg_5.svg', ''), 
   b'osc_alg_6': ('osc_alg_6.svg', ''), 
   b'osc_alg_7': ('osc_alg_7.svg', ''), 
   b'osc_alg_8': ('osc_alg_8.svg', ''), 
   b'osc_alg_9': ('osc_alg_9.svg', ''), 
   b'osc_b': ('osc_b.svg', ''), 
   b'osc_c': ('osc_c.svg', ''), 
   b'osc_d': ('osc_d.svg', ''), 
   b'pedal_distortion': ('pedal_distortion.svg', ''), 
   b'pedal_fuzz': ('pedal_fuzz.svg', ''), 
   b'pedal_overdrive': ('pedal_overdrive.svg', ''), 
   b'phase_inverted': ('phase_inverted.svg', ''), 
   b'phase_normal': ('phase_normal.svg', ''), 
   b'route_in': ('route_in.svg', ''), 
   b'route_out': ('route_out.svg', ''), 
   b'simpler_1shot': ('simpler_1shot.svg', ''), 
   b'simpler_adsr': ('simpler_adsr.svg', ''), 
   b'simpler_slice': ('simpler_slice.svg', ''), 
   b'tension_bow': ('tension_bow.svg', ''), 
   b'tension_hammer': ('tension_hammer.svg', ''), 
   b'tension_hammerbounce': ('tension_hammerbounce.svg', ''), 
   b'tension_plectrum': ('tension_plectrum.svg', ''), 
   b'tension_plectum': ('tension_plectum.svg', ''), 
   b'track_group': ('track_group.svg', ''), 
   b'tube_a': ('tube_a.svg', ''), 
   b'utility_left': ('utility_left.svg', ''), 
   b'utility_right': ('utility_right.svg', ''), 
   b'utility_stereo': ('utility_stereo.svg', ''), 
   b'utility_swap': ('utility_swap.svg', ''), 
   b'tube_b': ('tube_b.svg', ''), 
   b'tube_c': ('tube_c.svg', ''), 
   b'voices_2': ('voices_2.svg', ''), 
   b'voices_3': ('voices_3.svg', ''), 
   b'voices_4': ('voices_4.svg', ''), 
   b'voices_5': ('voices_5.svg', ''), 
   b'voices_6': ('voices_6.svg', ''), 
   b'voices_7': ('voices_7.svg', ''), 
   b'voices_8': ('voices_8.svg', ''), 
   b'wave_noise_loop': ('wave_noise_loop.svg', ''), 
   b'wave_noise_white': ('wave_noise_white.svg', ''), 
   b'wave_saw_16': ('wave_saw_16.svg', ''), 
   b'wave_saw_3': ('wave_saw_3.svg', ''), 
   b'wave_saw_32': ('wave_saw_32.svg', ''), 
   b'wave_saw_4': ('wave_saw_4.svg', ''), 
   b'wave_saw_6': ('wave_saw_6.svg', ''), 
   b'wave_saw_64': ('wave_saw_64.svg', ''), 
   b'wave_saw_8': ('wave_saw_8.svg', ''), 
   b'wave_saw_down': ('wave_saw_down.svg', ''), 
   b'wave_saw_up': ('wave_saw_up.svg', ''), 
   b'wave_sh_mono': ('wave_sh_mono.svg', ''), 
   b'wave_sh_stereo': ('wave_sh_stereo.svg', ''), 
   b'wave_sine': ('wave_sine.svg', ''), 
   b'wave_sine_4bit': ('wave_sine_4bit.svg', ''), 
   b'wave_sine_8bit': ('wave_sine_8bit.svg', ''), 
   b'wave_square': ('wave_square.svg', ''), 
   b'wave_square_16': ('wave_square_16.svg', ''), 
   b'wave_square_3': ('wave_square_3.svg', ''), 
   b'wave_square_32': ('wave_square_32.svg', ''), 
   b'wave_square_4': ('wave_square_4.svg', ''), 
   b'wave_square_6': ('wave_square_6.svg', ''), 
   b'wave_square_64': ('wave_square_64.svg', ''), 
   b'wave_square_8': ('wave_square_8.svg', ''), 
   b'wave_triangle': ('wave_triangle.svg', ''), 
   b'wave_user': ('wave_user.svg', ''), 
   b'wavetable_effect_classic': ('wavetable_effect_classic.svg', ''), 
   b'wavetable_effect_fm': ('wavetable_effect_fm.svg', ''), 
   b'wavetable_effect_modern': ('wavetable_effect_modern.svg', ''), 
   b'wavetable_effect_none': ('wavetable_effect_none.svg', ''), 
   b'wavetable_env_loop': ('wavetable_env_loop.svg', ''), 
   b'wavetable_env_loop_none': ('wavetable_env_loop_none.svg', ''), 
   b'wavetable_env_loop_trigger': ('wavetable_env_loop_trigger.svg', ''), 
   b'wavetable_env_slope': ('wavetable_env_slope.svg', ''), 
   b'wavetable_env_time': ('wavetable_env_time.svg', ''), 
   b'wavetable_env_value': ('wavetable_env_value.svg', ''), 
   b'wavetable_filter_1': ('', 'wavetable_filter_1_small.svg'), 
   b'wavetable_filter_2': ('', 'wavetable_filter_2_small.svg'), 
   b'wavetable_filter_3': ('', 'wavetable_filter_3_small.svg'), 
   b'wavetable_filter_4': ('', 'wavetable_filter_4_small.svg'), 
   b'wavetable_filter_5': ('', 'wavetable_filter_5_small.svg'), 
   b'wavetable_filter_switch_1': ('wavetable_filter_switch_1.svg', ''), 
   b'wavetable_filter_switch_2': ('wavetable_filter_switch_2.svg', ''), 
   b'wavetable_octave_0': ('wavetable_octave_0.svg', ''), 
   b'wavetable_octave_minus_1': ('wavetable_octave_minus_1.svg', ''), 
   b'wavetable_octave_minus_2': ('wavetable_octave_minus_2.svg', ''), 
   b'wavetable_osc_1': ('wavetable_osc_1.svg', ''), 
   b'wavetable_osc_2': ('wavetable_osc_2.svg', ''), 
   b'wavetable_osc_mix': ('wavetable_osc_mix.svg', ''), 
   b'wavetable_osc_sub': ('wavetable_osc_sub.svg', ''), 
   b'wavetable_routing_parallel': ('wavetable_routing_parallel.svg', ''), 
   b'wavetable_routing_serial': ('wavetable_routing_serial.svg', ''), 
   b'wavetable_routing_split': ('wavetable_routing_split.svg', ''), 
   b'wavetable_unison_classic': ('wavetable_unison_classic.svg', ''), 
   b'wavetable_unison_shimmer': ('wavetable_unison_shimmer.svg', ''), 
   b'wavetable_unison_noise': ('wavetable_unison_noise.svg', ''), 
   b'wavetable_unison_none': ('wavetable_unison_none.svg', ''), 
   b'wavetable_unison_phase_sync': ('wavetable_unison_phase_sync.svg', ''), 
   b'wavetable_unison_position_spread': ('wavetable_unison_position_spread.svg', ''), 
   b'wavetable_unison_random': ('wavetable_unison_random.svg', ''), 
   b'workflow_clip': ('workflow_clip.svg', ''), 
   b'workflow_scene': ('workflow_scene.svg', '')}
OPERATOR_OSCILLATORS = ('wave_sine', 'wave_sine_4bit', 'wave_sine_8bit', 'wave_saw_3',
                        'wave_saw_4', 'wave_saw_6', 'wave_saw_8', 'wave_saw_16',
                        'wave_saw_32', 'wave_saw_64', 'wave_saw_down', 'wave_square_3',
                        'wave_square_4', 'wave_square_6', 'wave_square_8', 'wave_square_16',
                        'wave_square_32', 'wave_square_64', 'wave_square', 'wave_triangle',
                        'wave_noise_loop', 'wave_noise_white', 'wave_user')
ACTIVATE = ('control_off', 'control_on')
ANALOG_OSCILLATORS = ('wave_sine', 'wave_saw_down', 'wave_square', 'wave_noise_white')
ANALOG_L_F_O = ('wave_sine', 'wave_triangle', 'wave_square', 'wave_noise_white', 'wave_noise_white')
ANALOG_FILTERS = ('filter_low_12', 'filter_low_24', 'filter_band_6', 'filter_band_12',
                  'filter_notch_12', 'filter_notch_24', 'filter_high_12', 'filter_high_24',
                  'filter_formant_6', 'filter_formant_12')
RESONANCE_TYPES = ('co_beam', 'co_marimba', 'co_string', 'co_membrane', 'co_plate',
                   'co_pipe', 'co_tube')
COLLISION_FILTERS = ('filter_low_12', 'filter_high_12', 'filter_band_12', 'filter_band_6')
COLLISION_L_F_O = ('wave_sine', 'wave_square', 'wave_triangle', 'wave_saw_up', 'wave_saw_down',
                   'wave_sh_mono', 'wave_noise_white')
IMPULSE_FILTERS = ('filter_low_12', 'filter_low_24', 'filter_band_12', 'filter_band_24',
                   'filter_high_12', 'filter_high_24', 'filter_notch_12')
SAMPLER_OSCILLATORS = ('wave_sine', 'wave_square', 'wave_triangle', 'wave_saw_up',
                       'wave_saw_down', 'wave_sh_mono')
LFO_WAVEFORMS = ('wave_sine', 'wave_square', 'wave_triangle', 'wave_saw_up', 'wave_saw_down',
                 'wave_sh_stereo', 'wave_sh_mono')
STEREO_MODE = ('lfo_phase', 'lfo_spin')
SYNC = ('lfo_free', 'lfo_sync')
EQ8_FILTER_TYPES = ('filter_high_48', 'filter_high_12', 'filter_low_shelf', 'filter_bell',
                    'filter_notch_24', 'filter_high_shelf', 'filter_low_12', 'filter_low_48')
CYTOMIC_FILTER_TYPES = ('filter_low_48', 'filter_high_48', 'filter_band_24', 'filter_notch_24',
                        'filter_morph_24')
FILTER_CIRCUIT_TYPES = ('circuit_clean', 'circuit_osr', 'circuit_ms2', 'circuit_smp',
                        'circuit_prd')
COMPRESSOR_MODES = ('compressor_peak', 'compressor_rms', 'compressor_expand')
WAVETABLE_LOOP_MODE = ('wavetable_env_loop_none', 'wavetable_env_loop_trigger', 'wavetable_env_loop')
WAVETABLE_OSCILLATOR_SWITCH = ('wavetable_osc_1', 'wavetable_osc_2', 'wavetable_osc_sub',
                               'wavetable_osc_mix')
WAVETABLE_OSCILLATOR_EFFECT_TYPES = ('wavetable_effect_none', 'wavetable_effect_fm',
                                     'wavetable_effect_classic', 'wavetable_effect_modern')
WAVETABLE_FILTER_TYPES = ('wavetable_filter_1', 'wavetable_filter_2', 'wavetable_filter_3',
                          'wavetable_filter_4', 'wavetable_filter_5')
WAVETABLE_LFO_TYPES = ('lfo_sine_small', 'lfo_triangle_small', 'lfo_saw_down_small',
                       'lfo_square_small', 'lfo_random_small')
WAVETABLE_VOICES = ('voices_2', 'voices_3', 'voices_4', 'voices_5', 'voices_6', 'voices_7',
                    'voices_8')
GENERIC_PARAMETER_IMAGES = {b'LFO Waveform': LFO_WAVEFORMS, 
   b'Waveform': ('wave_sine', 'wave_triangle', 'wave_saw_down', 'wave_sh_stereo'), 
   b'Filter Type': ('filter_low_48', 'filter_high_48', 'filter_band_24', 'filter_notch_24'), 
   b'Ext. In On': ACTIVATE, 
   b'LFO Sync': SYNC, 
   b'Sync': SYNC, 
   b'Adaptive Q': ACTIVATE, 
   b'LFO Stereo Mode': STEREO_MODE, 
   b'Side Listen': ACTIVATE, 
   b'EQ On': ACTIVATE, 
   b'EQ Mode': ('filter_low_shelf', 'filter_bell', 'filter_high_shelf', 'filter_low_48', 'filter_band_24',
 'filter_high_48')}
DEVICE_PARAMETER_IMAGES = {b'UltraAnalog': {b'OSC1 On/Off': ACTIVATE, 
                    b'OSC2 On/Off': ACTIVATE, 
                    b'F1 On/Off': ACTIVATE, 
                    b'F2 On/Off': ACTIVATE, 
                    b'AMP1 On/Off': ACTIVATE, 
                    b'AMP2 On/Off': ACTIVATE, 
                    b'Noise On/Off': ACTIVATE, 
                    b'Unison On/Off': ACTIVATE, 
                    b'Glide On/Off': ACTIVATE, 
                    b'Glide Legato': ACTIVATE, 
                    b'LFO1 On/Off': ACTIVATE, 
                    b'LFO1 Sync': SYNC, 
                    b'LFO2 On/Off': ACTIVATE, 
                    b'LFO2 Sync': SYNC, 
                    b'F1 On/Off': ACTIVATE, 
                    b'F2 On/Off': ACTIVATE, 
                    b'Vib On/Off': ACTIVATE, 
                    b'OSC1 Shape': ANALOG_OSCILLATORS, 
                    b'OSC2 Shape': ANALOG_OSCILLATORS, 
                    b'F1 Type': ANALOG_FILTERS, 
                    b'F2 Type': ANALOG_FILTERS, 
                    b'LFO1 Shape': ANALOG_L_F_O, 
                    b'LFO2 Shape': ANALOG_L_F_O}, 
   b'ChannelEq': {b'Highpass On': ACTIVATE}, b'Collision': {b'Res 1 Type': RESONANCE_TYPES, 
                  b'Res 2 Type': RESONANCE_TYPES, 
                  b'Mallet On/Off': ACTIVATE, 
                  b'Noise On/Off': ACTIVATE, 
                  b'Res 1 On/Off': ACTIVATE, 
                  b'Res 2 On/Off': ACTIVATE, 
                  b'LFO 1 On/Off': ACTIVATE, 
                  b'LFO 2 On/Off': ACTIVATE, 
                  b'Mallet On/Off': ACTIVATE, 
                  b'Noise Filter Type': COLLISION_FILTERS, 
                  b'LFO 1 Shape': COLLISION_L_F_O, 
                  b'LFO 2 Shape': COLLISION_L_F_O, 
                  b'LFO 1 Sync': SYNC, 
                  b'LFO 2 Sync': SYNC}, 
   b'InstrumentImpulse': {b'1 Filter Type': IMPULSE_FILTERS, 
                          b'2 Filter Type': IMPULSE_FILTERS, 
                          b'3 Filter Type': IMPULSE_FILTERS, 
                          b'4 Filter Type': IMPULSE_FILTERS, 
                          b'5 Filter Type': IMPULSE_FILTERS, 
                          b'6 Filter Type': IMPULSE_FILTERS, 
                          b'7 Filter Type': IMPULSE_FILTERS, 
                          b'8 Filter Type': IMPULSE_FILTERS}, 
   b'StringStudio': {b'Excitator Type': ('tension_bow', 'tension_hammer', 'tension_hammerbounce', 'tension_plectrum'), 
                     b'Filter Type': ('filter_low_12', 'filter_low_24', 'filter_band_6', 'filter_band_12', 'filter_notch_12',
 'filter_notch_24', 'filter_high_12', 'filter_high_24', 'filter_formant_6', 'filter_formant_12'), 
                     b'Exc On/Off': ACTIVATE, 
                     b'E Pos Abs': ACTIVATE, 
                     b'Pickup On/Off': ACTIVATE, 
                     b'Damper On': ACTIVATE, 
                     b'Damper Gated': ACTIVATE, 
                     b'D Pos Abs': ACTIVATE, 
                     b'Term On/Off': ACTIVATE, 
                     b'Body On/Off': ACTIVATE, 
                     b'Filter On/Off': ACTIVATE, 
                     b'LFO On/Off': ACTIVATE, 
                     b'Vibrato On/Off': ACTIVATE, 
                     b'Unison On/Off': ACTIVATE, 
                     b'Porta On/Off': ACTIVATE, 
                     b'Porta Legato': ACTIVATE, 
                     b'Porta Prop': ACTIVATE, 
                     b'FEG On/Off': ACTIVATE, 
                     b'Damper Gated': ACTIVATE, 
                     b'LFO Sync On': SYNC, 
                     b'LFO Shape': ('wave_sine', 'wave_triangle', 'wave_square', 'wave_sh_mono', 'wave_noise_white')}, 
   b'Operator': {b'Oscillator': ('osc_a', 'osc_b', 'osc_c', 'osc_d'), 
                 b'Algorithm': ('osc_alg_1', 'osc_alg_2', 'osc_alg_3', 'osc_alg_4', 'osc_alg_5', 'osc_alg_6', 'osc_alg_7',
 'osc_alg_8', 'osc_alg_9', 'osc_alg_10', 'osc_alg_11'), 
                 b'Filter Type': CYTOMIC_FILTER_TYPES, 
                 b'Filter Circuit - LP/HP': FILTER_CIRCUIT_TYPES, 
                 b'Filter Circuit - BP/NO/Morph': FILTER_CIRCUIT_TYPES, 
                 b'LFO Type': ('wave_sine', 'wave_square', 'wave_triangle', 'wave_saw_up', 'wave_saw_down', 'wave_sh_mono',
 'wave_noise_white'), 
                 b'Osc-A Wave': OPERATOR_OSCILLATORS, 
                 b'Osc-B Wave': OPERATOR_OSCILLATORS, 
                 b'Osc-C Wave': OPERATOR_OSCILLATORS, 
                 b'Osc-D Wave': OPERATOR_OSCILLATORS, 
                 b'Filter On': ACTIVATE, 
                 b'Osc-A On': ACTIVATE, 
                 b'A Quantize': ACTIVATE, 
                 b'B Quantize': ACTIVATE, 
                 b'C Quantize': ACTIVATE, 
                 b'D Quantize': ACTIVATE, 
                 b'Osc-A Retrig': ACTIVATE, 
                 b'A Fix On ': ACTIVATE, 
                 b'Osc-B On': ACTIVATE, 
                 b'Osc-B Quantize': ACTIVATE, 
                 b'Osc-B Retrig': ACTIVATE, 
                 b'B Fix On ': ACTIVATE, 
                 b'Osc-C On': ACTIVATE, 
                 b'Osc-C Quantize': ACTIVATE, 
                 b'Osc-C Retrig': ACTIVATE, 
                 b'C Fix On ': ACTIVATE, 
                 b'Osc-D On': ACTIVATE, 
                 b'Osc-D Quantize': ACTIVATE, 
                 b'Osc-D Retrig': ACTIVATE, 
                 b'D Fix On ': ACTIVATE, 
                 b'LFO On': ACTIVATE, 
                 b'LFO Retrigger': ACTIVATE, 
                 b'Glide On': ACTIVATE, 
                 b'Pe On': ACTIVATE, 
                 b'LFO < Pe': ACTIVATE, 
                 b'Osc-A < Pe': ACTIVATE, 
                 b'Osc-B < Pe': ACTIVATE, 
                 b'Osc-C < Pe': ACTIVATE, 
                 b'Osc-D < Pe': ACTIVATE, 
                 b'Filt < LFO': ACTIVATE, 
                 b'Osc-A < LFO': ACTIVATE, 
                 b'Osc-B < LFO': ACTIVATE, 
                 b'Osc-C < LFO': ACTIVATE, 
                 b'Osc-D < LFO': ACTIVATE}, 
   b'MultiSampler': {b'F On': ACTIVATE, 
                     b'Fe On': ACTIVATE, 
                     b'Shaper On': ACTIVATE, 
                     b'Osc On': ACTIVATE, 
                     b'O Fix On': ACTIVATE, 
                     b'O Type': OPERATOR_OSCILLATORS, 
                     b'Pe On': ACTIVATE, 
                     b'L 1 On': ACTIVATE, 
                     b'L 1 Sync': SYNC, 
                     b'L 1 Retrig': ACTIVATE, 
                     b'L 1 Wave': SAMPLER_OSCILLATORS, 
                     b'L 2 On': ACTIVATE, 
                     b'L 2 Sync': SYNC, 
                     b'L 2 St Mode': STEREO_MODE, 
                     b'L 2 Retrig': ACTIVATE, 
                     b'L 2 Wave': SAMPLER_OSCILLATORS, 
                     b'L 3 On': ACTIVATE, 
                     b'L 3 Sync': SYNC, 
                     b'L 3 St Mode': STEREO_MODE, 
                     b'L 3 Retrig': ACTIVATE, 
                     b'L 3 Wave': SAMPLER_OSCILLATORS, 
                     b'Ae On': ACTIVATE, 
                     b'Filter Type': CYTOMIC_FILTER_TYPES, 
                     b'Filter Circuit - LP/HP': FILTER_CIRCUIT_TYPES, 
                     b'Filter Circuit - BP/NO/Morph': FILTER_CIRCUIT_TYPES}, 
   b'OriginalSimpler': {b'F On': ACTIVATE, 
                        b'Fe On': ACTIVATE, 
                        b'L On': ACTIVATE, 
                        b'L Retrig': ACTIVATE, 
                        b'Pe On': ACTIVATE, 
                        b'L Wave': ('wave_sine', 'wave_square', 'wave_triangle', 'wave_saw_down', 'wave_saw_up', 'wave_sh_mono'), 
                        b'Filter Type': CYTOMIC_FILTER_TYPES, 
                        b'Filter Circuit - LP/HP': FILTER_CIRCUIT_TYPES, 
                        b'Filter Circuit - BP/NO/Morph': FILTER_CIRCUIT_TYPES}, 
   b'Amp': {b'Amp Type': ('amp_clean', 'amp_boost', 'amp_blues', 'amp_rock', 'amp_lead', 'amp_heavy', 'amp_bass'), 
            b'Dual Mono': ACTIVATE}, 
   b'AutoFilter': {b'LFO Quantize On': ACTIVATE, 
                   b'Filter Type': CYTOMIC_FILTER_TYPES, 
                   b'Filter Circuit - LP/HP': FILTER_CIRCUIT_TYPES, 
                   b'Filter Circuit - BP/NO/Morph': FILTER_CIRCUIT_TYPES}, 
   b'AutoPan': {b'Invert': ('phase_normal', 'phase_inverted'), 
                b'LFO Type': SYNC, 
                b'Stereo Mode': STEREO_MODE}, 
   b'BeatRepeat': {b'Filter On': ACTIVATE, b'Repeat': ACTIVATE, b'Block Triplets': ACTIVATE}, b'Cabinet': {b'Dual Mono': ACTIVATE, 
                b'Cabinet Type': ('cabinet_1x12', 'cabinet_2x12', 'cabinet_4x12', 'cabinet_4x10', 'cabinet_4x10bass'), 
                b'Microphone Type': ('mic_condenser', 'mic_dynamic'), 
                b'Microphone Position': ('mic_nearon', 'mic_nearoff', 'mic_far')}, 
   b'Chorus': {b'LFO Extend On': ACTIVATE, b'Link On': ACTIVATE}, b'Compressor2': {b'Auto Release On/Off': ACTIVATE, 
                    b'Makeup': ACTIVATE, 
                    b'Model': COMPRESSOR_MODES}, 
   b'Corpus': {b'Resonance Type': RESONANCE_TYPES, 
               b'LFO On/Off': ACTIVATE, 
               b'LFO Shape': ('wave_sine', 'wave_square', 'wave_triangle', 'wave_saw_up', 'wave_saw_down', 'wave_sh_mono',
 'wave_noise_white'), 
               b'LFO Stereo Mode': STEREO_MODE, 
               b'MIDI Frequency': ACTIVATE, 
               b'Note Off': ACTIVATE, 
               b'Filter On/Off': ACTIVATE}, 
   b'Delay': {b'L 16th': ('delay_16th_1', 'delay_16th_2', 'delay_16th_3', 'delay_16th_4', 'delay_16th_5', 'delay_16th_6',
 'delay_16th_8', 'delay_16th_16'), 
              b'R 16th': ('delay_16th_1', 'delay_16th_2', 'delay_16th_3', 'delay_16th_4', 'delay_16th_5', 'delay_16th_6',
 'delay_16th_8', 'delay_16th_16'), 
              b'Channel': ('utility_stereo', 'utility_left', 'utility_right'), 
              b'Link Switch': ('utility_stereo', 'utility_left'), 
              b'L Sync Enum': SYNC, 
              b'R Sync Enum': SYNC, 
              b'Ping Pong': ACTIVATE}, 
   b'DrumBuss': {b'Drive Type': ('drumbuss_soft', 'drumbuss_medium', 'drumbuss_hard')}, b'Tube': {b'Tube Type': ('tube_a', 'tube_b', 'tube_c')}, b'Echo': {b'L Sync Mode': ('echo_note', 'echo_triplet', 'echo_dotted', 'echo_16th'), 
             b'R Sync Mode': ('echo_note', 'echo_triplet', 'echo_dotted', 'echo_16th'), 
             b'Mod Wave': ('lfo_sine_small', 'lfo_triangle_small', 'lfo_saw_up_small', 'lfo_saw_down_small',
 'lfo_square_small', 'lfo_random_small'), 
             b'Link': ACTIVATE, 
             b'Ping Pong': ACTIVATE, 
             b'Repitch': ACTIVATE, 
             b'Filter On': ACTIVATE, 
             b'Mod Sync': ACTIVATE}, 
   b'Eq8': {b'Band': ('eq8_band1', 'eq8_band2', 'eq8_band3', 'eq8_band4', 'eq8_band5', 'eq8_band6', 'eq8_band7',
 'eq8_band8'), 
            b'1 Filter Type A': EQ8_FILTER_TYPES, 
            b'2 Filter Type A': EQ8_FILTER_TYPES, 
            b'3 Filter Type A': EQ8_FILTER_TYPES, 
            b'4 Filter Type A': EQ8_FILTER_TYPES, 
            b'5 Filter Type A': EQ8_FILTER_TYPES, 
            b'6 Filter Type A': EQ8_FILTER_TYPES, 
            b'7 Filter Type A': EQ8_FILTER_TYPES, 
            b'8 Filter Type A': EQ8_FILTER_TYPES, 
            b'1 Filter On A': ACTIVATE, 
            b'2 Filter On A': ACTIVATE, 
            b'3 Filter On A': ACTIVATE, 
            b'4 Filter On A': ACTIVATE, 
            b'5 Filter On A': ACTIVATE, 
            b'6 Filter On A': ACTIVATE, 
            b'7 Filter On A': ACTIVATE, 
            b'8 Filter On A': ACTIVATE}, 
   b'FilterEQ3': {b'LowOn': ACTIVATE, b'MidOn': ACTIVATE, b'HighOn': ACTIVATE}, b'FilterDelay': {b'1 Input On': ACTIVATE, 
                    b'2 Input On': ACTIVATE, 
                    b'3 Input On': ACTIVATE, 
                    b'1 Delay Mode': ACTIVATE, 
                    b'2 Delay Mode': ACTIVATE, 
                    b'3 Delay Mode': ACTIVATE}, 
   b'FrequencyShifter': {b'Wide': ACTIVATE, b'Drive On/Off': ACTIVATE}, b'GlueCompressor': {b'Peak Clip In': ACTIVATE}, b'GrainDelay': {b'Delay Mode': ACTIVATE}, b'InstrumentVector': {b'Oscillator': WAVETABLE_OSCILLATOR_SWITCH, 
                         b'Osc 1 Effect Type': WAVETABLE_OSCILLATOR_EFFECT_TYPES, 
                         b'Osc 2 Effect Type': WAVETABLE_OSCILLATOR_EFFECT_TYPES, 
                         b'Sub Transpose': ('wavetable_octave_0', 'wavetable_octave_minus_1', 'wavetable_octave_minus_2'), 
                         b'Filter': ('wavetable_filter_switch_1', 'wavetable_filter_switch_2'), 
                         b'Filter 1 Type': WAVETABLE_FILTER_TYPES, 
                         b'Filter 2 Type': WAVETABLE_FILTER_TYPES, 
                         b'Filter 1 On': ACTIVATE, 
                         b'Filter 2 On': ACTIVATE, 
                         b'Filter 1 LP/HP': FILTER_CIRCUIT_TYPES, 
                         b'Filter 2 LP/HP': FILTER_CIRCUIT_TYPES, 
                         b'Filter 1 BP/NO/Morph': FILTER_CIRCUIT_TYPES, 
                         b'Filter 2 BP/NO/Morph': FILTER_CIRCUIT_TYPES, 
                         b'Filter Routing': ('wavetable_routing_serial', 'wavetable_routing_parallel', 'wavetable_routing_split'), 
                         b'Amp Env View': ('wavetable_env_time', 'wavetable_env_slope'), 
                         b'Mod Env View': ('wavetable_env_time', 'wavetable_env_slope', 'wavetable_env_value'), 
                         b'Amp Loop Mode': WAVETABLE_LOOP_MODE, 
                         b'Env 2 Loop Mode': WAVETABLE_LOOP_MODE, 
                         b'Env 3 Loop Mode': WAVETABLE_LOOP_MODE, 
                         b'LFO 1 Shape': WAVETABLE_LFO_TYPES, 
                         b'LFO 2 Shape': WAVETABLE_LFO_TYPES, 
                         b'LFO 1 Retrigger': ACTIVATE, 
                         b'LFO 2 Retrigger': ACTIVATE, 
                         b'Mono On': ACTIVATE, 
                         b'Unison Mode': ('wavetable_unison_none', 'wavetable_unison_classic', 'wavetable_unison_shimmer', 'wavetable_unison_noise',
 'wavetable_unison_phase_sync', 'wavetable_unison_position_spread', 'wavetable_unison_random'), 
                         b'Unison Voices': WAVETABLE_VOICES, 
                         b'Poly Voices': WAVETABLE_VOICES}, 
   b'Limiter': {b'Auto': ACTIVATE, b'Link Channels': ACTIVATE}, b'Looper': {b'Reverse': ACTIVATE}, b'MultibandDynamics': {b'Band Activator (Low)': ACTIVATE, 
                          b'Band Activator (Mid)': ACTIVATE, 
                          b'Band Activator (High)': ACTIVATE, 
                          b'Soft Knee On/Off': ACTIVATE}, 
   b'Pedal': {b'Type': ('pedal_overdrive', 'pedal_distortion', 'pedal_fuzz'), 
              b'Sub': ACTIVATE}, 
   b'Redux': {b'Bit On': ACTIVATE}, b'Resonator': {b'Const': ACTIVATE, 
                  b'Filter On': ACTIVATE, 
                  b'I On': ACTIVATE, 
                  b'II On': ACTIVATE, 
                  b'III On': ACTIVATE, 
                  b'IV On': ACTIVATE, 
                  b'V On': ACTIVATE}, 
   b'Reverb': {b'In LowCut On': ACTIVATE, 
               b'In HighCut On': ACTIVATE, 
               b'ER Spin On': ACTIVATE, 
               b'HiShelf On': ACTIVATE, 
               b'LowShelf On': ACTIVATE, 
               b'Freeze On': ACTIVATE, 
               b'Flat On': ACTIVATE, 
               b'Cut On': ACTIVATE, 
               b'Chorus On': ACTIVATE}, 
   b'Saturator': {b'Color': ACTIVATE, b'Soft Clip': ACTIVATE}, b'StereoGain': {b'Mute': ACTIVATE, 
                   b'BlockDc': ACTIVATE, 
                   b'Channel Mode': ('utility_left', 'utility_stereo', 'utility_right', 'utility_swap'), 
                   b'Left Inv': ACTIVATE, 
                   b'Right Inv': ACTIVATE}, 
   b'Vinyl': {b'Tracing On': ACTIVATE, b'Pinch On': ACTIVATE}, b'Vocoder': {b'Precise/Retro': ACTIVATE, b'Enhance': ACTIVATE}, b'MidiArpeggiator': {b'Hold On': ACTIVATE, 
                        b'Sync On': ACTIVATE, 
                        b'Velocity On': ACTIVATE, 
                        b'Vel. Retrigger': ACTIVATE}, 
   b'MidiNoteLength': {b'Trigger Mode': ACTIVATE, b'Sync On': ACTIVATE}, b'MidiRandom': {b'Mode': ACTIVATE}, b'MidiScale': {b'Fold': ACTIVATE}}

def get_image_filenames_from_ids(image_ids, small_images=False, image_id_to_filename=IMAGE_ID_TO_FILENAME):
    image_index = 1 if small_images else 0
    return [ image_id_to_filename.get(image_id, ('', ''))[image_index] for image_id in image_ids
           ]


def get_image_filenames(parameter_name, device_type, small_images=False, device_parameter_images=DEVICE_PARAMETER_IMAGES, generic_parameter_images=GENERIC_PARAMETER_IMAGES, image_id_to_filename=IMAGE_ID_TO_FILENAME):
    image_ids = []
    if device_type in device_parameter_images and parameter_name in device_parameter_images[device_type]:
        image_ids = device_parameter_images[device_type][parameter_name]
    elif parameter_name in generic_parameter_images:
        image_ids = generic_parameter_images[parameter_name]
    return get_image_filenames_from_ids(image_ids, small_images=small_images, image_id_to_filename=image_id_to_filename)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push2/device_parameter_icons.pyc
