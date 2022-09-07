import asyncio
import json
import os
import time
from asyncio import StreamWriter
from asyncio.exceptions import TimeoutError
from tkinter import messagebox

import aiofiles
from anyio import TASK_STATUS_IGNORED, create_task_group
from anyio.abc import TaskStatus
from async_timeout import timeout

import gui
from async_chat_utils import read_line, write_data, open_connection
from exceptions import InvalidToken
from settings import (
    CHAT_HOST, SEND_CHAT_PORT, FAILED_AUTH_MESSAGE, EMPTY_LINE, SEND_MSG_TEXT, SUCCESS_AUTH_TEXT, READ_CHAT_PORT,
    WATCHDOG_BEFORE_AUTH_TEXT, TIMEOUT_ERROR_TEXT, SERVER_PING_FREQUENCY_SEC, PING_SERVER_TEXT,
    TIMEOUT_READ_EXPIRED_SEC,
)


async def ping_pong_server(watchdog_queue, task_status: TaskStatus = TASK_STATUS_IGNORED):
    task_status.started()

    async with create_task_group() as tg:
        await tg.start(ping, watchdog_queue)
        await tg.start(pong, watchdog_queue)


async def ping(watchdog_queue, task_status: TaskStatus = TASK_STATUS_IGNORED):
    task_status.started()

    async with open_connection(CHAT_HOST, SEND_CHAT_PORT) as conn:
        _, writer = conn
        while True:
            await send_message(writer, message='')
            watchdog_queue.put_nowait(f'[{int(time.time())}] {PING_SERVER_TEXT}')
            await asyncio.sleep(SERVER_PING_FREQUENCY_SEC)


async def pong(watchdog_queue, task_status: TaskStatus = TASK_STATUS_IGNORED):
    task_status.started()

    async with open_connection(CHAT_HOST, READ_CHAT_PORT) as conn:
        reader, _ = conn

        while True:
            try:
                async with timeout(TIMEOUT_READ_EXPIRED_SEC) as cm:
                    await reader.readline()
            finally:
                if cm.expired:
                    watchdog_queue.put_nowait(f'[{int(time.time())}] {TIMEOUT_READ_EXPIRED_SEC}s {TIMEOUT_ERROR_TEXT}')
                    raise TimeoutError


async def authorise(reader, writer, token: str) -> dict:
    await read_line(reader)
    await write_data(writer=writer, data=f'{token}{EMPTY_LINE}')

    user_info = json.loads(await read_line(reader))

    if not user_info:
        messagebox.showinfo(title='Неизвестный токен', message=FAILED_AUTH_MESSAGE)
        raise InvalidToken(FAILED_AUTH_MESSAGE)

    return user_info


async def registrate(reader, writer, username, path):
    await read_line(reader)
    sanitized_nickname = username.replace('\n', '')

    await write_data(writer=writer, data=EMPTY_LINE)
    await read_line(reader)
    await write_data(writer=writer, data=f'{sanitized_nickname}{EMPTY_LINE}')

    raw_reg_info = await read_line(reader)
    reg_info = json.loads(raw_reg_info)

    file_path = os.path.join(path, f'{reg_info["account_hash"]}.json')
    async with aiofiles.open(file_path, mode='w') as file:
        await file.write(raw_reg_info)

    return reg_info


async def send_message(writer: StreamWriter, message: str):
    sanitized_msg = message.replace('\n', '')
    await write_data(writer, data=f'{sanitized_msg}{EMPTY_LINE * 2}')


async def send_msgs(
        token, host, send_port, sending_queue, status_updates_queue,
        watchdog_queue, task_status: TaskStatus = TASK_STATUS_IGNORED,
):
    task_status.started()
    status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.INITIATED)

    async with open_connection(host, send_port) as conn:
        status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.ESTABLISHED)
        reader, writer = conn

        watchdog_queue.put_nowait(f'[{int(time.time())}] {WATCHDOG_BEFORE_AUTH_TEXT}')
        auth_info = await authorise(reader, writer, token=token)
        watchdog_queue.put_nowait(f'[{int(time.time())}] {SUCCESS_AUTH_TEXT}')

        event = gui.NicknameReceived(auth_info['nickname'])
        status_updates_queue.put_nowait(event)

        while True:
            message = await sending_queue.get()
            await send_message(writer, message=message)
            watchdog_queue.put_nowait(f'[{int(time.time())}] {SEND_MSG_TEXT}')
