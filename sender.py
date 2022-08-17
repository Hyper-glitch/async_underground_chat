import asyncio
import json

from settings import CHAT_HOST, SEND_CHAT_PORT


async def read_line(reader) -> str:
    chat_line = (await asyncio.wait_for(reader.readline(), timeout=10))
    return chat_line.decode("utf-8").strip()


async def write_data(writer, data):
    writer.write(data.encode())
    await writer.drain()


async def send_messages(host: str, port: int, token):
    test_message = 'Something else\n\n'
    reader, writer = await asyncio.open_connection(host=host, port=port)

    await write_data(writer, data=token)
    account_info = json.loads(await read_line(reader))

    await write_data(writer, data=test_message)
    writer.close()


if __name__ == '__main__':
    host = CHAT_HOST
    send_port = SEND_CHAT_PORT
    token = '66b440d2-1e24-11ed-8c47-0242ac110002\n'

    asyncio.run(send_messages(host=host, port=send_port, token=token))
