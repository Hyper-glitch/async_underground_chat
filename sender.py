import json
import logging
import os
from asyncio import StreamReader, StreamWriter

import aiofiles

from chat_utils import create_parser, read_line, write_data, open_connection
from exceptions import FailedAuthError
from settings import CHAT_HOST, SEND_CHAT_PORT, AUTH_TOKEN, FAILED_AUTH_MESSAGE, EMPTY_LINE, NICKNAME

logger = logging.getLogger(__name__)


async def authorise(reader, writer, token: str):
    logger.debug(await read_line(reader))
    await write_data(writer=writer, data=f'{token}{EMPTY_LINE}')

    user_info = json.loads(await read_line(reader))
    logger.debug(user_info)

    if not user_info:
        raise FailedAuthError(FAILED_AUTH_MESSAGE)


async def registrate(reader, writer, username, path):
    sanitized_nickname = username.replace('\n', '')

    logger.debug(await read_line(reader))
    await write_data(writer=writer, data=EMPTY_LINE)

    logger.debug(await read_line(reader))
    await write_data(writer=writer, data=f'{sanitized_nickname}{EMPTY_LINE}')

    raw_reg_info = await read_line(reader)
    reg_info = json.loads(raw_reg_info)

    file_path = os.path.join(path, f'{reg_info["account_hash"]}.json')
    async with aiofiles.open(file_path, mode='w') as file:
        await file.write(raw_reg_info)
    logger.debug(reg_info)

    return reg_info


async def send_message(reader: StreamReader, writer: StreamWriter, message: str):
    sanitized_msg = message.replace('\n', '')
    await write_data(writer, data=f'{sanitized_msg}{EMPTY_LINE * 2}')
    logger.debug(await read_line(reader))


async def run_sender():
    parser = create_parser()
    args = parser.parse_args()

    host = args.host or CHAT_HOST
    send_port = args.send_port or SEND_CHAT_PORT
    token = args.token or AUTH_TOKEN
    username = args.nickname or NICKNAME
    message = ' '.join(args.message)
    accounts_path = 'users_info'

    os.makedirs(accounts_path, exist_ok=True)

    if not token:
        async with open_connection(host, send_port) as conn:
            reader, writer = conn
            reg_info = await registrate(reader, writer, username, accounts_path)
        token = reg_info['account_hash']

    async with open_connection(host, send_port) as conn:
        reader, writer = conn
        await authorise(reader, writer, token=token)
        await send_message(reader, writer, message=message)
