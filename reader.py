import asyncio
import datetime
import logging
import time

from chat_utils import write_chat_msg
from settings import RECONNECTION_WAIT_TIME, CHAT_HOST, READ_CHAT_PORT, CHAT_HISTORY_PATH

logger = logging.getLogger(__name__)


async def read_messages(host: str, port: int, path: str):
    """Write messages from chat line by line to a file.

    Args:
        host: TCP/IP hostname to open listen connection.
        port: TCP/IP port to open listen connection.
        path: filepath for chat history.

    Raises:
        Exception: if connection between server and client lost.
    """
    while True:
        try:
            reader, writer = await asyncio.open_connection(host=host, port=port)
        except Exception:
            time.sleep(RECONNECTION_WAIT_TIME)
            continue

        message = await reader.readline()

        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y.%m.%d %H:%M:%S")

        formatted_message = f'[{formatted_date}] {message.decode()}'
        print(formatted_message)
        await write_chat_msg(data=formatted_message, path=path)
        writer.close()


if __name__ == '__main__':
    host = CHAT_HOST
    read_port = READ_CHAT_PORT
    path = CHAT_HISTORY_PATH

    asyncio.run(read_messages(host=host, port=read_port, path=path))
