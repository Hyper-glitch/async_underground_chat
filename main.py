import argparse
import asyncio
import logging

from reader import read_messages
from sender import registrate
from settings import READ_CHAT_PORT, CHAT_HOST, CHAT_HISTORY_PATH, SEND_CHAT_PORT, AUTH_TOKEN

logger = logging.getLogger(__name__)


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
    return parser.parse_args()


async def main():
    """Run the main logic for chat."""
    args = create_parser()

    logging.basicConfig(
        format=u'%(levelname)s %(filename)s %(message)s', level=logging.DEBUG,
    )

    host = CHAT_HOST if not args.host else args.host
    read_port = READ_CHAT_PORT if not args.read_port else args.read_port
    send_port = SEND_CHAT_PORT if not args.send_port else args.send_port
    path = CHAT_HISTORY_PATH if not args.path else args.path
    token = AUTH_TOKEN
    nickname = 'jepka'

    tasks = [
        asyncio.create_task(read_messages(host=host, port=read_port, path=path)),
        asyncio.create_task(registrate(host=host, port=send_port, nickname=nickname)),
    ]

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
