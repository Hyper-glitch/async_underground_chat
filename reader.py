import datetime
import logging
import time
from asyncio.exceptions import TimeoutError

import aiofiles
from anyio import TASK_STATUS_IGNORED
from anyio.abc import TaskStatus
from async_timeout import timeout

import gui
from async_chat_utils import open_connection
from chat_utils import create_parser
from settings import CHAT_HOST, READ_CHAT_PORT, CHAT_HISTORY_PATH, READ_MSG_TEXT, TIMEOUT_ERROR_TEXT, \
    TIMEOUT_EXPIRED_SEC

watchdog_logger = logging.getLogger('watchdog_logger')


async def read_msgs(messages_queue, status_updates_queue, watchdog_queue,
                    task_status: TaskStatus = TASK_STATUS_IGNORED):
    """Write messages from chat line by line to a file.

    Raises:
        Exception: if connection between server and client lost.
    """
    task_status.started()
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
                try:
                    async with timeout(TIMEOUT_EXPIRED_SEC):
                        message = await reader.readline()
                except TimeoutError:
                    text = TIMEOUT_ERROR_TEXT
                else:
                    text = READ_MSG_TEXT

                watchdog_queue.put_nowait(f'[{int(time.time())}] {text}')
                now = datetime.datetime.now()
                formatted_date = now.strftime("%Y.%m.%d %H:%M:%S")
                formatted_message = f'[{formatted_date}] {message.decode()}'

                messages_queue.put_nowait(formatted_message)
                await file.write(formatted_message)
