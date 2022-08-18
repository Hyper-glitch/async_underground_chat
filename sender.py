import asyncio
import json
import logging

from settings import CHAT_HOST, SEND_CHAT_PORT, AUTH_TOKEN, FAILED_AUTH_MESSAGE

logger = logging.getLogger(__name__)


async def read_line(reader) -> str:
    chat_line = await reader.readline()
    return chat_line.decode('utf-8').strip()


async def write_data(writer, data: str):
    writer.write(data.encode())
    await writer.drain()


async def auth(host, port, token: str):
    reader, writer = await asyncio.open_connection(host=host, port=port)

    logger.debug(await read_line(reader))
    await write_data(writer=writer, data=f'{token}\n')

    account_info = json.loads(await read_line(reader))
    logger.debug(account_info)

    assert account_info is not None, FAILED_AUTH_MESSAGE
    return account_info


async def send_messages(host: str, port: int, token: str, message: str):
    reader, writer = await asyncio.open_connection(host=host, port=port)
    logger.debug(await read_line(reader))

    await write_data(writer, data=f'{token}\n')
    account_info = json.loads(await reader.readline())
    logger.debug(await read_line(reader))

    await write_data(writer, data=f'{message}\n\n')
    logger.debug(await read_line(reader))

    writer.close()


if __name__ == '__main__':
    host = CHAT_HOST
    send_port = SEND_CHAT_PORT
    token = AUTH_TOKEN

    asyncio.run(auth(token=token))
