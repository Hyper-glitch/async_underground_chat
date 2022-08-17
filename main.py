import argparse
import asyncio
import datetime
import time

import aiofiles

from settings import RECONNECTION_WAIT_TIME, CHAT_PORT, CHAT_HOST, CHAT_HISTORY_PATH


def create_parser() -> argparse.Namespace:
    """Create arg parser and add arguments.
    Returns:
        namespace: values or arguments, that parsed.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-H', '--host', help='TCP/IP hostname to serve on (default: %(default)r)',
    )
    parser.add_argument(
        '-P', '--port', help='TCP/IP port to serve on (default: %(default)r)', type=int,
    )
    parser.add_argument(
        '-p', '--path', help='path to write chat history', type=str,
    )
    return parser.parse_args()


async def write_chat_msg(data, path):
    async with aiofiles.open(path, mode='a') as file:
        await file.write(data)


async def listen_chat(host, port, path):
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


def main():
    args = create_parser()

    host = CHAT_HOST if not args.host else args.host
    port = CHAT_PORT if not args.port else args.port
    path = CHAT_HISTORY_PATH if not args.path else args.path

    asyncio.run(listen_chat(host=host, port=port, path=path))


if __name__ == '__main__':
    main()
