import datetime

import aiofiles

from chat_utils import open_connection


async def read_msgs(messages_queue, host, read_port, path):
    """Write messages from chat line by line to a file.

    Raises:
        Exception: if connection between server and client lost.
    """
    async with aiofiles.open(path, mode='a') as file:
        async with open_connection(host, read_port) as conn:
            reader, _ = conn

            while True:
                message = await reader.readline()
                now = datetime.datetime.now()
                formatted_date = now.strftime("%Y.%m.%d %H:%M:%S")
                formatted_message = f'[{formatted_date}] {message.decode()}'

                messages_queue.put_nowait(formatted_message)
                await file.write(formatted_message)
