import asyncio
import logging
from _socket import gaierror

from anyio import create_task_group, TASK_STATUS_IGNORED, run
from anyio.abc import TaskStatus

import gui
from async_chat_utils import show_history
from chat_utils import set_up_logger
from reader import read_msgs
from sender import send_msgs, ping_server
from settings import LAST_GUI_DRAW_QUEUE, TIMEOUT_ERROR_TEXT

watchdog_logger = logging.getLogger('watchdog_logger')


async def start_task_group(messages_queue, status_updates_queue, watchdog_queue, sending_queue):
    async with create_task_group() as tg:
        await tg.start(ping_server, watchdog_queue)
        await tg.start(read_msgs, messages_queue, status_updates_queue, watchdog_queue)
        await tg.start(send_msgs, sending_queue, status_updates_queue, watchdog_queue)
        await tg.start(watch_for_connection, watchdog_queue)


async def watch_for_connection(watchdog_queue, task_status: TaskStatus = TASK_STATUS_IGNORED):
    task_status.started()

    while True:
        log = await watchdog_queue.get()
        if TIMEOUT_ERROR_TEXT in log:
            raise gaierror

        watchdog_logger.info(log)


async def handle_connection(messages_queue, sending_queue, status_updates_queue, watchdog_queue):
    while True:
        try:
            await start_task_group(messages_queue, status_updates_queue, watchdog_queue, sending_queue)
        except (ConnectionError, gaierror):
            status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.CLOSED)
            status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.CLOSED)
        finally:
            status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.INITIATED)
            status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.INITIATED)
            continue


async def main():
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    watchdog_queue = asyncio.Queue()
    queues = [messages_queue, sending_queue, status_updates_queue, watchdog_queue]

    set_up_logger()

    await asyncio.gather(
        gui.draw(*queues[:LAST_GUI_DRAW_QUEUE]),
        show_history(messages_queue),
        handle_connection(*queues),
    )


if __name__ == '__main__':
    run(main)
