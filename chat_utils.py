import argparse
import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def open_connection(host, port):
    reader, writer = await asyncio.open_connection(host=host, port=port)
    try:
        yield reader, writer
    finally:
        writer.close()


async def read_line(reader) -> str:
    chat_line = await reader.readline()
    return chat_line.decode('utf-8').strip()


async def write_data(writer, data: str):
    writer.write(data.encode())
    await writer.drain()


def create_parser() -> argparse.Namespace:
    """Create arg parser and add arguments.

    Returns:
        namespace: values or arguments, that parsed.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-H', '--host', help='TCP/IP hostname to listen chat (default: %(default)r)',
    )
    parser.add_argument(
        '-R', '--read_port', help='TCP/IP port for reading messages from the chat (default: %(default)r)', type=int,
    )
    parser.add_argument(
        '-S', '--send_port', help='TCP/IP port for sending messages to the chat (default: %(default)r)', type=int,
    )
    parser.add_argument(
        '-P', '--path', help='a path to write chat history', type=str,
    )
    parser.add_argument(
        '-T', '--token', help='token that authorize user in chat', type=str,
    )
    parser.add_argument(
        '-N', '--nickname', help='your alias in chat', type=str,
    )
    parser.add_argument(
        '-M', '--message', help='message that sends to the chat', type=str, nargs='+', required=True,
    )
    return parser.parse_args()
