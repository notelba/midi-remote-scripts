# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\base\__init__.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from .dependency import DependencyError, depends, inject
from .disconnectable import CompoundDisconnectable, Disconnectable, disconnectable
from .event import Event, EventError, EventObject, MultiSlot, ObservablePropertyAlias, SerializableListenableProperties, Slot, SlotGroup, has_event, listenable_property, listens, listens_group
from .gcutil import histogram, instances_by_name, refget
from .isclose import isclose
from .live_api_utils import duplicate_clip_loop, is_parameter_bipolar, liveobj_changed, liveobj_valid
from .proxy import Proxy, ProxyBase
from .signal import Signal
from .util import Bindable, BooleanContext, NamedTuple, OutermostOnlyContext, Slicer, aggregate_contexts, chunks, clamp, compose, const, dict_diff, find_if, first, flatten, forward_property, get_slice, group, in_range, index_if, infinite_context_manager, instance_decorator, is_contextmanager, is_iterable, is_matrix, lazy_attribute, linear, maybe, memoize, mixin, monkeypatch, monkeypatch_extend, negate, next, nop, overlaymap, print_message, product, recursive_map, remove_if, second, sign, slice_size, slicer, third, to_slice, trace_value, union
__all__ = (
 b'Bindable',
 b'BooleanContext',
 b'CompoundDisconnectable',
 b'DependencyError',
 b'Disconnectable',
 b'Event',
 b'EventError',
 b'EventObject',
 b'MultiSlot',
 b'NamedTuple',
 b'ObservablePropertyAlias',
 b'OutermostOnlyContext',
 b'Proxy',
 b'ProxyBase',
 b'SerializableListenableProperties',
 b'Signal',
 b'Slicer',
 b'Slot',
 b'SlotGroup',
 b'aggregate_contexts',
 b'chunks',
 b'clamp',
 b'compose',
 b'const',
 b'depends',
 b'dict_diff',
 b'disconnectable',
 b'duplicate_clip_loop',
 b'find_if',
 b'first',
 b'flatten',
 b'forward_property',
 b'get_slice',
 b'group',
 b'has_event',
 b'histogram',
 b'in_range',
 b'index_if',
 b'infinite_context_manager',
 b'inject',
 b'instance_decorator',
 b'instances_by_name',
 b'is_contextmanager',
 b'is_iterable',
 b'is_matrix',
 b'is_parameter_bipolar',
 b'isclose',
 b'lazy_attribute',
 b'linear',
 b'listenable_property',
 b'listens',
 b'listens_group',
 b'liveobj_changed',
 b'liveobj_valid',
 b'maybe',
 b'memoize',
 b'mixin',
 b'monkeypatch',
 b'monkeypatch_extend',
 b'negate',
 b'next',
 b'nop',
 b'overlaymap',
 b'print_message',
 b'product',
 b'recursive_map',
 b'refget',
 b'remove_if',
 b'second',
 b'sign',
 b'slice_size',
 b'slicer',
 b'third',
 b'to_slice',
 b'trace_value',
 b'union')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ableton/v2/base/__init__.pyc
