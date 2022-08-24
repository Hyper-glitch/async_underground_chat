import asyncio

import aiofiles

import gui
from reader import read_msgs
from sender import send_msgs
from settings import CHAT_HISTORY_PATH


async def show_history(messages_queue):
    async with aiofiles.open(CHAT_HISTORY_PATH, mode='r') as file:
        lines = await file.readlines()
    for line in lines:
        messages_queue.put_nowait(line)


async def main():
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()

    await asyncio.gather(
        gui.draw(messages_queue, sending_queue, status_updates_queue),
        read_msgs(messages_queue),
        show_history(messages_queue),
        send_msgs(sending_queue),
    )


if __name__ == '__main__':
    asyncio.run(main())
