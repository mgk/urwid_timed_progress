#!/usr/bin/env python

from time import sleep
import urwid as uw
from urwid_timed_progress import TimedProgressBar

# Demo of bar adjusting to reasonable units
# The demo simulates progress at different rates to show
# the progress bar changing units as needed.
if __name__ == '__main__':

    palette = [
        ('normal',   'white', 'black', 'standout'),
        ('complete', 'white', 'dark magenta'),
    ]

    # Using SI units: https://en.wikipedia.org/wiki/Kilobyte
    units = [
        ('bytes', 1),
        ('kB', 1000),
        ('MB', 1000000)
    ]

    bar = TimedProgressBar('normal', 'complete', done=5e7, units=units)
    status = uw.Text('simulation that demonstrates auto selecting best units')
    footer = uw.Text('q to exit, r to run simulation')
    progress = uw.Frame(uw.ListBox([bar, uw.Divider(bottom=5), status]),
                        footer=footer)

    def run():
        bar.reset()

        # start with slow rate of progress
        status.set_text('starting out, running slowly')
        for i in range(5):
            bar.add_progress(1)
            loop.draw_screen()
            sleep(.5)
        for i in range(50):
            bar.add_progress(200)
            loop.draw_screen()
            sleep(.1)

        # run fast until done
        status.set_text('running fast until done')
        while bar.current < bar.done:
            bar.add_progress(100000)
            loop.draw_screen()
            sleep(.01)

        status.set_text('done')
        loop.draw_screen()

    def keypress(key):
        if key == 'q':
            raise uw.ExitMainLoop()
        elif key == 'r':
            run()

    loop = uw.MainLoop(progress, palette, unhandled_input=keypress)
    loop.run()
