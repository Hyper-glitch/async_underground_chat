import datetime
import logging
import time

import aiofiles

import gui
from chat_utils import open_connection, create_parser
from settings import CHAT_HOST, READ_CHAT_PORT, CHAT_HISTORY_PATH, READ_MSG_TEXT

watchdog_logger = logging.getLogger('watchdog_logger')


async def read_msgs(messages_queue, status_updates_queue, watchdog_queue):
    """Write messages from chat line by line to a file.

    Raises:
        Exception: if connection between server and client lost.
    """
    status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.INITIATED)

    parser = create_parser()
    args = parser.parse_args()

    host = args.host or CHAT_HOST
    read_port = args.read_port or READ_CHAT_PORT
    path = args.path or CHAT_HISTORY_PATH

    async with aiofiles.open(path, mode='a') as file:
        async with open_connection(host, read_port) as conn:
            reader, _ = conn
            status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.ESTABLISHED)
            while True:
                message = await reader.readline()
                watchdog_queue.put_nowait(f'[{int(time.time())}] {READ_MSG_TEXT}')

                now = datetime.datetime.now()
                formatted_date = now.strftime("%Y.%m.%d %H:%M:%S")
                formatted_message = f'[{formatted_date}] {message.decode()}'

                messages_queue.put_nowait(formatted_message)
                await file.write(formatted_message)
