import asyncio
import logging
import time
from _socket import gaierror

from anyio import create_task_group, TASK_STATUS_IGNORED, run
from anyio.abc import TaskStatus

import gui
from async_chat_utils import read_history
from chat_utils import set_up_logger, create_parser
from reader import read_msgs
from sender import send_msgs, ping_pong_server
from settings import (
    LAST_GUI_DRAW_QUEUE, AUTH_TOKEN, MAX_ATTEMPTS_TO_RECONNECTION, LONG_WAIT_RECONNECTION_SEC, CHAT_HOST,
    SEND_CHAT_PORT, CHAT_HISTORY_PATH, READ_CHAT_PORT, SHORT_WAIT_RECONNECTION_SEC, RECONNECTION_TEXT, DEAD_CONN_TEXT,
)

watchdog_logger = logging.getLogger('watchdog_logger')


async def watch_for_connection(watchdog_queue, task_status: TaskStatus = TASK_STATUS_IGNORED):
    task_status.started()

    while True:
        log = await watchdog_queue.get()
        watchdog_logger.info(log)


async def start_server_task_group(
        token, host, send_port, read_port, path, messages_queue,
        status_updates_queue, watchdog_queue, sending_queue,
):
    async with create_task_group() as tg:
        await tg.start(ping_pong_server, watchdog_queue)
        await tg.start(read_msgs, read_port, path, host, messages_queue, status_updates_queue, watchdog_queue)
        await tg.start(send_msgs, token, host, send_port, sending_queue, status_updates_queue, watchdog_queue)
        await tg.start(watch_for_connection, watchdog_queue)


async def handle_connection(
        messages_queue, sending_queue, status_updates_queue,
        watchdog_queue, token, host, send_port, read_port,
        path, task_status: TaskStatus = TASK_STATUS_IGNORED,
):
    task_status.started()
    attempts_to_reconnection = 0

    while True:
        try:
            await start_server_task_group(
                token, host, send_port, read_port, path, messages_queue,
                status_updates_queue, watchdog_queue, sending_queue,
            )
        except (ConnectionError, gaierror):
            watchdog_logger.info(f'[{int(time.time())}] {DEAD_CONN_TEXT}')
            status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.CLOSED)
            status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.CLOSED)
        finally:
            attempts_to_reconnection += 1
            watchdog_logger.info(f'[{int(time.time())}] {RECONNECTION_TEXT} in {SHORT_WAIT_RECONNECTION_SEC} sec')
            status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.INITIATED)
            status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.INITIATED)
            time.sleep(SHORT_WAIT_RECONNECTION_SEC)

            if attempts_to_reconnection > MAX_ATTEMPTS_TO_RECONNECTION:
                watchdog_logger.info(
                    f'[{int(time.time())}] {MAX_ATTEMPTS_TO_RECONNECTION} attempts are over. '
                    f'{RECONNECTION_TEXT} in {LONG_WAIT_RECONNECTION_SEC} sec'
                )
                attempts_to_reconnection = 0
                time.sleep(LONG_WAIT_RECONNECTION_SEC)

            continue


async def main():
    watchdog_logger = logging.getLogger('watchdog_logger')
    set_up_logger(watchdog_logger)

    parser = create_parser()
    args = parser.parse_args()

    token = args.token or AUTH_TOKEN
    path = args.path or CHAT_HISTORY_PATH
    host = args.host or CHAT_HOST
    read_port = args.read_port or READ_CHAT_PORT
    send_port = args.send_port or SEND_CHAT_PORT

    token_queue = asyncio.Queue()
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    watchdog_queue = asyncio.Queue()

    queues = [messages_queue, sending_queue, status_updates_queue, watchdog_queue]

    if not token:
        async with create_task_group() as reg_tg:
            await reg_tg.start(gui.draw_registration, token_queue, host, send_port)
        token = await token_queue.get()

    async with create_task_group() as tg:
        await tg.start(gui.draw, *queues[:LAST_GUI_DRAW_QUEUE])
        await tg.start(read_history, messages_queue)
        await tg.start(handle_connection, *queues, token, host, send_port, read_port, path)


if __name__ == '__main__':
    try:
        run(main)
    except KeyboardInterrupt:
        exit(0)
