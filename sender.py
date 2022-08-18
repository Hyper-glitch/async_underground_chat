import asyncio
import json
import logging

from settings import CHAT_HOST, SEND_CHAT_PORT, AUTH_TOKEN

logger = logging.getLogger(__name__)


async def read_line(reader) -> str:
    chat_line = await reader.readline()
    return chat_line.decode('utf-8').strip()


async def write_data(writer, data):
    writer.write(data.encode())
    await writer.drain()


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
    asyncio.run(send_messages(host=host, port=send_port, token=token, message='blablabla'))
