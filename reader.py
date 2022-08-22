import asyncio
import datetime

import aiofiles

from chat_utils import create_parser, open_connection
from settings import CHAT_HOST, READ_CHAT_PORT, CHAT_HISTORY_PATH


async def run_reader():
    """Write messages from chat line by line to a file.

    Raises:
        Exception: if connection between server and client lost.
    """
    parser = create_parser()
    args = parser.parse_args()

    host = args.host or CHAT_HOST
    read_port = args.read_port or READ_CHAT_PORT
    path = args.path or CHAT_HISTORY_PATH

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


if __name__ == '__main__':
    asyncio.run(run_reader())
