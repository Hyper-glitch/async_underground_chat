import argparse
import asyncio
import datetime
import time

import aiofiles

RECONNECTION_WAIT_TIME = 180


def create_parser() -> argparse.Namespace:
    """Create arg parser and add arguments.
    Returns:
        namespace: values or arguments, that parsed.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-H', '--host', help='TCP/IP hostname to serve on (default: %(default)r)', default='localhost',
    )
    parser.add_argument(
        '-P', '--port', help='TCP/IP port to serve on (default: %(default)r)', type=int, default='8080',
    )
    parser.add_argument(
        '-p', '--path', help='path to write chat history', type=str, default='minechat.history',
    )
    return parser.parse_args()


async def write_chat_msg(data):
    async with aiofiles.open('chat_history', mode='a') as file:
        await file.write(data)


async def listen_chat():
    host = 'minechat.dvmn.org'
    port = 5000

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
        await write_chat_msg(data=formatted_message)
        print(formatted_message)


if __name__ == '__main__':
    asyncio.run(listen_chat())
