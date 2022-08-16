import asyncio
import datetime
import time

import aiofiles

RECONNECTION_WAIT_TIME = 180


async def write_chat_msg(data):
    async with aiofiles.open('chat_history', mode='a') as file:
        await file.write(data)


async def tcp_client():
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
    asyncio.run(tcp_client())
