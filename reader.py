import datetime
import logging

import aiofiles

from chat_utils import create_parser, open_connection
from settings import CHAT_HOST, READ_CHAT_PORT, CHAT_HISTORY_PATH

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

    async with aiofiles.open(path, mode='a') as file:
        async with open_connection(host, read_port) as conn:
            reader, _ = conn

            while True:
                message = await reader.readline()
                now = datetime.datetime.now()
                formatted_date = now.strftime("%Y.%m.%d %H:%M:%S")

                formatted_message = f'[{formatted_date}] {message.decode()}'
                print(formatted_message)
                await file.write(formatted_message)
