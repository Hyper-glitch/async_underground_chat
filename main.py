import asyncio

import gui
from chat_utils import create_parser
from reader import read_msgs
from settings import CHAT_HOST, READ_CHAT_PORT, CHAT_HISTORY_PATH


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
        gui.draw(messages_queue, sending_queue, status_updates_queue),
        read_msgs(*reader_args),
    )


if __name__ == '__main__':
    asyncio.run(main())
