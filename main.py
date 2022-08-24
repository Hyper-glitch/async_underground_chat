import asyncio

import aiofiles

import gui
from chat_utils import create_parser
from reader import read_msgs
from settings import CHAT_HOST, READ_CHAT_PORT, CHAT_HISTORY_PATH


async def show_history(messages_queue):
    async with aiofiles.open(CHAT_HISTORY_PATH, mode='r') as file:
        lines = await file.readlines()
    for line in lines:
        messages_queue.put_nowait(line)


async def main():
    parser = create_parser()
    args = parser.parse_args()

    host = args.host or CHAT_HOST
    read_port = args.read_port or READ_CHAT_PORT
    path = args.path or CHAT_HISTORY_PATH

    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()

    reader_args = [messages_queue, host, read_port, path]

    await asyncio.gather(
        read_msgs(*reader_args),
        show_history(messages_queue),
        gui.draw(messages_queue, sending_queue, status_updates_queue),
    )


if __name__ == '__main__':
    asyncio.run(main())
