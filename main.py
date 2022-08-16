import asyncio


async def get_chat_msg():
    pass


async def tcp_client():
    host = 'minechat.dvmn.org'
    port = 5000

    while True:
        reader, writer = await asyncio.open_connection(host=host, port=port)

        data = await reader.readline()
        print(data.decode())


if __name__ == '__main__':
    asyncio.run(tcp_client())
