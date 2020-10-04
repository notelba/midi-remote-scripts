# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\browser_model_factory.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import Live
from .browser_model import filter_type_for_browser, EmptyBrowserModel, QueryingBrowserModel
from .browser_query import TagBrowserQuery, PathBrowserQuery, PlacesBrowserQuery, SourceBrowserQuery, ColorTagsBrowserQuery
FilterType = Live.Browser.FilterType
PLACES_LABEL = b'Places'

def make_plugins_query():
    return TagBrowserQuery(include=[
     b'Plug-Ins'], root_name=b'plugins', subfolder=b'Plug-Ins')


def make_midi_effect_browser_model(browser):
    midi_effects = TagBrowserQuery(include=[b'MIDI Effects'], root_name=b'midi_effects')
    max = TagBrowserQuery(include=[
     [
      b'Max for Live', b'Max MIDI Effect']], subfolder=b'Max for Live', root_name=b'max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[color_tags, midi_effects, max, plugins, places])


def make_audio_effect_browser_model(browser):
    audio_effects = TagBrowserQuery(include=[b'Audio Effects'], root_name=b'audio_effects')
    max = TagBrowserQuery(include=[
     [
      b'Max for Live', b'Max Audio Effect']], subfolder=b'Max for Live', root_name=b'max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[color_tags, audio_effects, max, plugins, places])


def make_instruments_browser_model(browser):
    instrument_rack = PathBrowserQuery(path=[
     b'Instruments', b'Instrument Rack'], root_name=b'instruments')
    drums = SourceBrowserQuery(include=[
     b'Drums'], exclude=[b'Drum Hits'], subfolder=b'Drum Rack', root_name=b'drums')
    instruments = TagBrowserQuery(include=[
     b'Instruments'], exclude=[
     b'Drum Rack', b'Instrument Rack'], root_name=b'instruments')
    drum_hits = TagBrowserQuery(include=[
     [
      b'Drums', b'Drum Hits']], subfolder=b'Drum Hits', root_name=b'drums')
    max = TagBrowserQuery(include=[
     [
      b'Max for Live', b'Max Instrument']], subfolder=b'Max for Live', root_name=b'max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[
     color_tags,
     instrument_rack,
     drums,
     instruments,
     max,
     drum_hits,
     plugins,
     places])


def make_drum_pad_browser_model(browser):
    drums = TagBrowserQuery(include=[[b'Drums', b'Drum Hits']], root_name=b'drums')
    samples = SourceBrowserQuery(include=[
     b'Samples'], subfolder=b'Samples', root_name=b'samples')
    instruments = TagBrowserQuery(include=[b'Instruments'], root_name=b'instruments')
    max = TagBrowserQuery(include=[
     [
      b'Max for Live', b'Max Instrument']], subfolder=b'Max for Live', root_name=b'max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[
     color_tags, drums, samples, instruments, max, plugins, places])


def make_fallback_browser_model(browser):
    return EmptyBrowserModel(browser=browser)


def make_browser_model(browser, filter_type=None):
    """
    Factory that returns an appropriate browser model depending on the
    browser filter type and hotswap target.
    """
    factories = {FilterType.instrument_hotswap: make_instruments_browser_model, 
       FilterType.drum_pad_hotswap: make_drum_pad_browser_model, 
       FilterType.audio_effect_hotswap: make_audio_effect_browser_model, 
       FilterType.midi_effect_hotswap: make_midi_effect_browser_model}
    if filter_type == None:
        filter_type = filter_type_for_browser(browser)
    return factories.get(filter_type, make_fallback_browser_model)(browser)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push/browser_model_factory.pyc
