import asyncio
import json
import logging
from asyncio import StreamReader, StreamWriter

from chat_utils import write_to_file, create_parser, read_line, write_data
from settings import CHAT_HOST, SEND_CHAT_PORT, AUTH_TOKEN, FAILED_AUTH_MESSAGE, EMPTY_LINE, NICKNAME

logger = logging.getLogger(__name__)


async def authorise(reader, writer, token: str):
    logger.debug(await read_line(reader))
    await write_data(writer=writer, data=f'{token}{EMPTY_LINE}')

    user_info = json.loads(await read_line(reader))
    logger.debug(user_info)

    assert user_info is not None, FAILED_AUTH_MESSAGE


async def registrate(reader, writer, username):
    sanitized_nickname = username.replace('\n', '')

    logger.debug(await read_line(reader))
    await write_data(writer=writer, data=EMPTY_LINE)

    logger.debug(await read_line(reader))
    await write_data(writer=writer, data=f'{sanitized_nickname}{EMPTY_LINE}')

    reg_info = json.loads(await read_line(reader))
    logger.debug(reg_info)

    await write_to_file(data=reg_info, path=f'users_info/{reg_info["account_hash"]}.json')
    return reg_info


async def send_message(reader: StreamReader, writer: StreamWriter, message: str):
    sanitized_msg = message.replace('\n', '')
    await write_data(writer, data=f'{sanitized_msg}{EMPTY_LINE * 2}')
    logger.debug(await read_line(reader))


async def run_sender():
    args = create_parser()

    host = CHAT_HOST if not args.host else args.host
    send_port = SEND_CHAT_PORT if not args.send_port else args.send_port
    token = AUTH_TOKEN if not args.token else args.token
    username = NICKNAME if not args.nickname else args.nickname
    message = 'Teeeeeeest meeeesssssagegeee!' if not args.message else ' '.join(args.message)

    if not token:
        reader, writer = await asyncio.open_connection(host=host, port=send_port)
        reg_info = await registrate(reader, writer, username)
        token = reg_info['account_hash']
        writer.close()

    reader, writer = await asyncio.open_connection(host=host, port=send_port)
    await authorise(reader, writer, token=token)
    await send_message(reader, writer, message=message)
