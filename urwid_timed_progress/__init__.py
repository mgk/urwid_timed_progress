#!/usr/bin/env python

import urwid as uw
import time
import datetime
from operator import itemgetter
from decimal import Decimal

__version__ = '1.0.2'


class FancyProgressBar(uw.ProgressBar):
    """ProgressBar with extended inline text"""
    def __init__(self, normal, complete, done=100, satt=None,
                 units='KB'):
        super(FancyProgressBar, self).__init__(normal, complete, 0, done, satt)
        self.units = units

    def get_text(self):
        """Return extended progress bar text"""
        done_units = to_reasonable_unit(self.done, self.units)
        current = round(self.current / done_units['multiplier'], 2)
        percent = int(self.current * 100 / self.done)
        return '{0:.2f} of {1:.2f} {2} ({3}%)'.format(current,
                                                      done_units['val'],
                                                      done_units['label'],
                                                      percent)


class TimedProgressBar(uw.Columns):
    """Progress bar with label, progress rate, and time remaining displays

    TimedProgressBar keeps track of when progress started and computes
    the :attr:`rate` of progress and estimated :attr:`remaining_time`
    as :attr:`current` progress is updated with the :meth:`add_progress`
    method.

    A timed progress bar starts with a current value of 0.

    :param normal: display attribute for incomplete part of progress bar
    :param complete: display attribute for complete part of progress bar
    :param done: progress amount at 100%
    :param satt: display attribute for smoothed part of bar where the
        foreground of satt corresponds to the normal part and the
        background corresponds to the complete part.  If satt  is ``None``
        then no smoothing will be done.
    :param units: units to use. If a string, the units value is taken as a
        label and is used as is. `units` can also be a list of tuples such
        as::

            [
                ('KB', 1000),
                ('MB', 1000000),
                ('GB', 1000000000)
            ]

        With a list of tuples, the timed progress bar selects the most
        reasonable unit to use for current, done, and rate. 3 KB is more
        reasonable than .003 MB and 3MB is more reasonable than 3000KB.

        Values greater than 1 and less than 1000 are preferred over fractions.
        So 400 KB is considered more reasonable than .4 MB.

    :type units: str or list of tuples
    :param label: label shown to the left of the progress bar
    :param label_width: fixed width of `label`. Can be used to align
        stacked progress bars. Set `label_width` to 0 and `label` to the
        empty string to omit the label.
    """
    def __init__(self, normal, complete, done=100, satt=None,
                 units='', label='Progress', label_width=15):
        super(TimedProgressBar, self).__init__([], dividechars=1)
        if isinstance(units, str):
            units = [(units, 1)]
        self.units = units
        self.bar = FancyProgressBar(normal, complete, done, satt, units)

        self.rate_display = uw.Text('', align='left')
        self.remaining_time_display = uw.Text('', align='right')

        info = uw.Columns([self.rate_display, self.remaining_time_display])

        self.contents = [
            (uw.Text(label), self.options('given', label_width)),
            (uw.Pile([self.bar, info]), self.options('weight', 1))
            ]

        self.reset()

    def add_progress(self, delta):
        """Add to the current progress amount

        Add `delta` to the current progress amount. This also updates
        :attr:`rate` and :attr:`remaining_time`.

        The :attr:`current` progress is never less than 0 or greater
        than :attr:`done`.

        :param delta: amount to add, may be negative
        """
        self.bar.current = max(min(self.done, self.current + delta), 0)
        self.rate_display.set_text(self.rate_text)
        self.remaining_time_display.set_text(self.remaining_time_text)
        return self.current == self.done

    def reset(self):
        """Set :attr:`current` and restart the progress bar timer."""
        self.bar.current = 0
        self.start_time = time.time()
        self.add_progress(0)

    @property
    def current(self):
        """current progress amount"""
        return self.bar.current

    @property
    def done(self):
        """progress amount when complete"""
        return self.bar.done

    @done.setter
    def done(self, value):
        self.bar.done = value

    @property
    def elapsed(self):
        """time in seconds since the progress bar timer was last started"""
        return time.time() - self.start_time

    @property
    def rate(self):
        """progress rate"""
        if self.elapsed == 0:
            return 0
        else:
            return self.current / self.elapsed

    @property
    def rate_text(self):
        rate_units = to_reasonable_unit(self.rate, self.units)
        return '{0:.2f} {1}/s'.format(rate_units['val'], rate_units['label'])

    @property
    def remaining_time(self):
        """remaining time (as a timedelta) until complete at current rate"""
        if self.rate == 0:
            return None
        else:
            remaining_progress = self.done - self.current
            if self.rate == 0:
                if self.done == 0:
                    return 0
                else:
                    return None

            return remaining_progress / self.rate

    @property
    def remaining_time_text(self):
        try:
            return str(datetime.timedelta(seconds=round(self.remaining_time)))
        except:
            return ''


def to_reasonable_unit(value, units, round_digits=2):
    """Convert a value to the most reasonable unit.

    The most reasonable unit is roughly the one with the smallest exponent
    absolute value when written in scientific notation. For example
    `1.5` is more reasonable that `.0015` and `22` is more reasonable
    than `22000`. There is a bias towards numbers > 1, so `3.2` is
    considered more reasonable that `.32`.
    """
    def to_unit(unit):
        return float(value) / unit[1]
    exponents = [abs(Decimal(to_unit(u)).adjusted() - 1) for u in units]
    best = min(enumerate(exponents), key=itemgetter(1))[0]
    return dict(val=round(to_unit(units[best]), round_digits),
                label=units[best][0],
                multiplier=units[best][1])
