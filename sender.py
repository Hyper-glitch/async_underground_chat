import json
import os
import time
from asyncio import StreamWriter
from tkinter import messagebox

import aiofiles
from anyio import TASK_STATUS_IGNORED
from anyio.abc import TaskStatus

import gui
from async_chat_utils import read_line, write_data, open_connection
from chat_utils import create_parser
from exceptions import InvalidToken
from settings import (
    CHAT_HOST, SEND_CHAT_PORT, AUTH_TOKEN, FAILED_AUTH_MESSAGE, EMPTY_LINE, NICKNAME, SEND_MSG_TEXT, SUCCESS_AUTH_TEXT,
    WATCHDOG_BEFORE_AUTH_TEXT,
)


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


async def send_message(watchdog_queue, writer: StreamWriter, message: str):
    sanitized_msg = message.replace('\n', '')
    await write_data(writer, data=f'{sanitized_msg}{EMPTY_LINE * 2}')
    watchdog_queue.put_nowait(f'[{int(time.time())}] {SEND_MSG_TEXT}')


async def send_msgs(sending_queue, status_updates_queue, watchdog_queue, task_status: TaskStatus = TASK_STATUS_IGNORED):
    task_status.started()
    status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.INITIATED)

    parser = create_parser()
    args = parser.parse_args()

    host = args.host or CHAT_HOST
    send_port = args.send_port or SEND_CHAT_PORT
    token = args.token or AUTH_TOKEN
    username = args.nickname or NICKNAME
    accounts_path = 'users_info'

    os.makedirs(accounts_path, exist_ok=True)

    if not token:
        async with open_connection(host, send_port) as conn:
            status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.ESTABLISHED)
            reader, writer = conn
            reg_info = await registrate(reader, writer, username, accounts_path)
        token = reg_info['account_hash']

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
            await send_message(watchdog_queue, writer, message=message)
