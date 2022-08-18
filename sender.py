import asyncio
import json
import logging

from chat_utils import write_to_file
from settings import CHAT_HOST, SEND_CHAT_PORT, AUTH_TOKEN, FAILED_AUTH_MESSAGE, EMPTY_LINE

logger = logging.getLogger(__name__)


async def read_line(reader) -> str:
    chat_line = await reader.readline()
    return chat_line.decode('utf-8').strip()


async def write_data(writer, data: str):
    writer.write(data.encode())
    await writer.drain()


async def authorise(host, port, token: str):
    reader, writer = await asyncio.open_connection(host=host, port=port)

    logger.debug(await read_line(reader))
    await write_data(writer=writer, data=f'{token}{EMPTY_LINE}')

    user_info = json.loads(await read_line(reader))
    logger.debug(user_info)

    assert user_info is not None, FAILED_AUTH_MESSAGE
    writer.close()

    return user_info


async def registrate(host, port, nickname):
    reader, writer = await asyncio.open_connection(host=host, port=port)

    logger.debug(await read_line(reader))
    await write_data(writer=writer, data=EMPTY_LINE)

    logger.debug(await read_line(reader))
    await write_data(writer=writer, data=f'{nickname}{EMPTY_LINE}')

    user_info = json.loads(await read_line(reader))
    logger.debug(user_info)

    await write_to_file(data=user_info, path=f'users_info/{user_info["account_hash"]}.json')

    writer.close()


async def send_messages(host: str, port: int, token: str, message: str):
    reader, writer = await asyncio.open_connection(host=host, port=port)
    logger.debug(await read_line(reader))

    await write_data(writer, data=f'{token}\n')
    logger.debug(await read_line(reader))

    await write_data(writer, data=f'{message}\n\n')
    logger.debug(await read_line(reader))

    writer.close()


if __name__ == '__main__':
    host = CHAT_HOST
    send_port = SEND_CHAT_PORT
    token = AUTH_TOKEN
    nickname = 'jepka'

    asyncio.run(registrate(host=host, port=send_port, nickname=nickname))
