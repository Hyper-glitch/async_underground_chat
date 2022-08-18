import asyncio
import logging

from chat_utils import create_parser
from reader import read_messages
from settings import READ_CHAT_PORT, CHAT_HOST, CHAT_HISTORY_PATH

logger = logging.getLogger(__name__)


async def main():
    """Run the main logic for chat."""
    args = create_parser()

    logging.basicConfig(
        format=u'%(levelname)s %(filename)s %(message)s', level=logging.DEBUG,
    )

    host = CHAT_HOST if not args.host else args.host
    read_port = READ_CHAT_PORT if not args.read_port else args.read_port
    path = CHAT_HISTORY_PATH if not args.path else args.path

    tasks = [
        asyncio.create_task(read_messages(host=host, port=read_port, path=path)),
    ]

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
