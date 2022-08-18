import asyncio
import datetime
import logging
import time

from chat_utils import write_to_file, create_parser
from settings import RECONNECTION_WAIT_TIME, CHAT_HOST, READ_CHAT_PORT, CHAT_HISTORY_PATH

logger = logging.getLogger(__name__)


async def run_reader():
    """Write messages from chat line by line to a file.

    Raises:
        Exception: if connection between server and client lost.
    """
    args = create_parser()

    host = CHAT_HOST if not args.host else args.host
    read_port = READ_CHAT_PORT if not args.read_port else args.read_port
    path = CHAT_HISTORY_PATH if not args.path else args.path

    while True:
        try:
            reader, writer = await asyncio.open_connection(host=host, port=read_port)
        except Exception:
            time.sleep(RECONNECTION_WAIT_TIME)
            continue

        message = await reader.readline()

        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y.%m.%d %H:%M:%S")

        formatted_message = f'[{formatted_date}] {message.decode()}'
        print(formatted_message)
        await write_to_file(data=formatted_message, path=path)
        writer.close()
