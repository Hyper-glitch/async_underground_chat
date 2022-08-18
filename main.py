import asyncio
import logging

from reader import run_reader
from sender import run_sender

logger = logging.getLogger(__name__)


async def main():
    """Run the main logic for chat."""
    logging.basicConfig(
        format=u'%(levelname)s %(filename)s %(message)s', level=logging.DEBUG,
    )
    tasks = [
        asyncio.create_task(run_reader()),
        asyncio.create_task(run_sender()),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
