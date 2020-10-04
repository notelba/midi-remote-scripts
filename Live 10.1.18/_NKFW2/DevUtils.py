# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\DevUtils.py
# Compiled at: 2017-03-07 13:28:52
from collections import Iterable
import inspect, time, logging
logger = logging.getLogger(__name__)

def log(message):
    """ Writes the given message to Live's log file. """
    logger.info(message)


def get_logger():
    """ Returns the logger (for testing purposes). """
    return logger


def print_io(func):
    """ Decator that prints the caller, passed args and return from the given
    function. """

    def inner(*args, **kwargs):
        py_mod = inspect.stack()[1][1]
        line_num = inspect.stack()[1][2]
        caller = inspect.stack()[1][3]
        log('\n**** printing io for %s' % func.func_name)
        log('>>> Called by %s in %s at line number %s' % (caller, py_mod, line_num))
        if args:
            log('>>> Args: %s' % (', ').join([ str(a) for a in args ]))
        if kwargs:
            log('>>> Kwargs: %s' % kwargs)
        r = func(*args, **kwargs)
        if isinstance(r, Iterable) and not isinstance(r, (dict, str)):
            log('<<< Returned: %s' % (', ').join([ str(a) for a in r ]))
        else:
            log('<<< Returned: %s' % r)
        return r

    return inner


def print_profile(func):
    """ Decator that prints the time it took the given function to complete. """

    def inner(*args, **kwargs):
        start = int(round(time.time() * 1000))
        r = func(*args, **kwargs)
        end = int(round(time.time() * 1000))
        log('**** %s took %s ms' % (func.func_name, end - start))
        return r

    return inner


def print_call_count(func):
    """ Decator that prints the number of times the given function has been called. """

    def inner(*args, **kwargs):
        inner.calls += 1
        log('**** %s called %s times' % (func.func_name, inner.calls))
        return func(*args, **kwargs)

    inner.calls = 0
    return inner
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/DevUtils.pyc
