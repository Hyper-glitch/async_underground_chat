import argparse
import json
from typing import Union

import aiofiles


async def read_line(reader) -> str:
    chat_line = await reader.readline()
    return chat_line.decode('utf-8').strip()


async def write_data(writer, data: str):
    writer.write(data.encode())
    await writer.drain()


async def write_to_file(data: Union[str, dict], path: str):
    """Write messages from chat line by line to a file.

    Args:
        data: message from chat for writing in a file.
        path: filepath for chat history.
    """
    if isinstance(data, dict):
        data = json.dumps(data)

    async with aiofiles.open(path, mode='a') as file:
        await file.write(data)


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
        '-R', '--read_port', help='TCP/IP port to serve on (default: %(default)r)', type=int,
    )
    parser.add_argument(
        '-S', '--send_port', help='TCP/IP port to serve on (default: %(default)r)', type=int,
    )
    parser.add_argument(
        '-P', '--path', help='path to write chat history', type=str,
    )
    parser.add_argument(
        '-T', '--token', help='token that authorize user in chat', type=str,
    )
    parser.add_argument(
        '-U', '--username', help='your alias in chat', type=str,
    )
    parser.add_argument(
        '-M', '--message', help='message that sends to the chat', type=str, nargs='+', required=True,
    )
    return parser.parse_args()
