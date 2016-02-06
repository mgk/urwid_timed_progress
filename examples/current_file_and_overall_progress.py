#!/usr/bin/env python

import sys
import urwid as uw
from urwid_timed_progress import TimedProgressBar
from urwid.html_fragment import screenshot_init, screenshot_collect

# Demo of timed progress bar.

if __name__ == '__main__':

    palette = [
        ('normal',   'white', 'black', 'standout'),
        ('complete', 'white', 'dark magenta'),
    ]

    # capture as HTML screenshot if first arg is "screenshot"
    take_screenshot = len(sys.argv) > 1 and sys.argv[1] == 'screenshot'
    if take_screenshot:
        screenshot_init([(70, 15)], [['x'] * 7, ['q']])

    # Create two timed progress bars with labels and custom units.
    # Using the same label_width allows the bars to line up.
    bar1 = TimedProgressBar('normal', 'complete', label='Current File',
                            label_width=15, units='MB', done=10)
    bar2 = TimedProgressBar('normal', 'complete', label='Overall',
                            label_width=15, units='MB', done=100)

    # Advance the second bar
    bar2.add_progress(40)

    footer = uw.Text('q to exit, any other key adds to progress')
    progress = uw.Frame(uw.ListBox([bar1, uw.Divider(), bar2]), footer=footer)

    # Pressing a key other that 'q' advances the progress bars by 1
    # Calling add_progress() also updates the displayed rate and time
    # remaining.
    def keypress(key):
        if key in ('q', 'Q'):
            raise uw.ExitMainLoop()
        else:
            bar2.add_progress(1)
            if bar1.add_progress(1) and bar2.current < bar2.done:
                bar1.reset()

    loop = uw.MainLoop(progress, palette, unhandled_input=keypress)
    loop.run()

    if take_screenshot:
        for i, s in enumerate(screenshot_collect()):
            with open('screenshot-{}.html'.format(i), 'w') as f:
                f.write(s)
