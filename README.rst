|Docs| |Downloads| |License|

urwid_timed_progress
====================

**urwid_timed_progress** is an Urwid progress widget that displays enhanced
progress with custom units, rate of progress, and estimated time remaining.

Example screenshot showing two progress bars:

.. image::  https://raw.githubusercontent.com/mgk/urwid_timed_progress/master/screenshot.png
    :alt: Timed Progress Bars
    :target: https://raw.githubusercontent.com/mgk/urwid_timed_progress/master/examples/current_file_and_overall_progress.py
    :width: 600
    :height: 248
    :align: center

Installation
============

.. code::

    pip install urwid_timed_progress

Usage
=====

Create timed progress bar, much like a regular ProgressBar::

	file_size_mb = 1234
	progress = TimedProgressBar('normal', 'complete', label='Current File',
	                            units='MB', done=file_size_mb)

As the file operation proceeds update the progress bar::

	progress.add_progress(1)  # each time 1 unit of progress has been made

``add_progress()`` updates the progress bar rate and estimated time remaining.

To update the timer without adding progress do::

	progress.add_progress(0)

See `example code`_.

.. _example code: https://github.com/mgk/urwid_timed_progress/blob/master/examples/

.. |Docs| image:: https://readthedocs.org/projects/urwid-timed-progress/badge/?version=latest&style=flat
    :alt: Documentation Status
    :scale: 100%
    :target: http://urwid-timed-progress.rtfd.org/

.. |Downloads| image:: https://img.shields.io/pypi/dm/urwid_timed_progress.svg
    :target: https://pypi.python.org/pypi/urwid_timed_progress

.. |License| image:: http://img.shields.io/badge/license-MIT-blue.svg?style=flat
    :target: https://github.com/mgk/urwid_timed_progress/blob/master/LICENSE
