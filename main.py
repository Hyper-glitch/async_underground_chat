import asyncio
import logging

import aiofiles

import gui
from chat_utils import set_up_logger
from reader import read_msgs
from sender import send_msgs
from settings import CHAT_HISTORY_PATH

watchdog_logger = logging.getLogger('watchdog_logger')


async def show_history(messages_queue):
    async with aiofiles.open(CHAT_HISTORY_PATH, mode='r') as file:
        lines = await file.readlines()
    for line in lines:
        messages_queue.put_nowait(line)


async def watch_for_connection(watchdog_queue):
    while True:
        log = await watchdog_queue.get()
        watchdog_logger.info(log)


async def main():
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    watchdog_queue = asyncio.Queue()

    set_up_logger()

    await asyncio.gather(
        gui.draw(messages_queue, sending_queue, status_updates_queue),
        read_msgs(messages_queue, status_updates_queue, watchdog_queue),
        show_history(messages_queue),
        send_msgs(sending_queue, status_updates_queue, watchdog_queue),
        watch_for_connection(watchdog_queue),
    )


if __name__ == '__main__':
    asyncio.run(main())
