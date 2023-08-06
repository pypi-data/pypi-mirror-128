"""lairucrem with Trio based event loop."""

import trio
import urwid

nursery = None

async def get_main_widget():
    """Build the main widget."""
    txt = urwid.Text("Hello World")
    return urwid.Filler(txt, 'top')


def unhandled_input(key):
    if key == 'q':
        nursery.cancel_scope.cancel()
        # raise ValueError


class LairucremEventlLoop(urwid.TrioEventLoop):

    async def watch_process(self, cmd, cofunc):
        """await cofunc when the given process has some data to read in stdout."""
        return self._start_trask(self._watch_process, process)

    async def _watch_process(self, scope, process):
        with scope:
            while not scope.cancel_called:
                await self._wait_process



async def run():
    """Do stuff."""
    global nursery
    widget = await get_main_widget()
    event_loop = urwid.TrioEventLoop()
    loop = urwid.MainLoop(widget, event_loop=event_loop, unhandled_input=unhandled_input)
    async with trio.open_nursery() as nursery:
        with loop.start():
            await event_loop.run_async()
            event_loop.run_async()
        nursery.cancel_scope.cancel()





def main():
    """Start the main loop."""
    trio.run(run)


if __name__ == '__main__':
    main()
