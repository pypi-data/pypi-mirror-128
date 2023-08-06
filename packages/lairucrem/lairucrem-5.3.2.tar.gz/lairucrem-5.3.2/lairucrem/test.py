import collections
import os
from typing import Optional

import trio
import urwid
from outcome import Error


def urwid_with_trio(urwid_loop: urwid.MainLoop, trio_func):
    _func_queue = collections.deque()

    def _wakeup(*_data):
        while _func_queue:
            _func = _func_queue.popleft()()
        return True
    _wakeup_fd = urwid_loop.watch_pipe(_wakeup)

    def run_sync_soon_threadsafe(func):
        _func_queue.append(func)
        os.write(_wakeup_fd, b'\n')

    def run_sync_soon_not_threadsafe(func):
        urwid_loop.set_alarm_in(0, lambda *args: func())

    outcome = None

    def done_callback(_outcome):
        nonlocal outcome
        outcome = _outcome
        urwid_loop.remove_watch_pipe(_wakeup_fd)
        raise urwid.ExitMainLoop()

    scope: Optional[trio.CancelScope] = None

    async def trio_scope():
        nonlocal scope
        with trio.CancelScope() as scope:
            return await trio_func()

    trio.lowlevel.start_guest_run(
        trio_scope,
        run_sync_soon_threadsafe=run_sync_soon_threadsafe,
        run_sync_soon_not_threadsafe=run_sync_soon_not_threadsafe,
        done_callback=done_callback,
        # host_uses_signal_set_wakeup_fd=True,
    )
    try:
        urwid_loop.run()
    finally:
        os.close(_wakeup_fd)
        if outcome is None:
            outcome = Error(RuntimeError('Loop stopped before trio was done!'))
            if scope is not None:
                scope.cancel()
        return outcome.unwrap()


async def job():
    for n in range(100):
        await trio.sleep(1)
        pb.set_completion(n)
    await trio.sleep(0.0)
    return "OK!"


pb = urwid.ProgressBar("color1", "color3", satt='color2', done=99)
fill = urwid.Filler(pb, 'top')
loop = urwid.MainLoop(fill, palette=[
    ('color1', 'white', 'dark gray'),
    ('color2', 'light gray', 'dark gray'),
    ('color3', 'black', 'white'),
])

print(urwid_with_trio(loop, job))
