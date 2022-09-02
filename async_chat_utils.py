"""Module with async functions that chat main logic."""
import asyncio
from contextlib import asynccontextmanager

import aiofiles
from aiofiles import os
from anyio import TASK_STATUS_IGNORED
from anyio.abc import TaskStatus

from settings import CHAT_HISTORY_PATH


async def read_line(reader) -> str:
    chat_line = await reader.readline()
    return chat_line.decode('utf-8').strip()


async def write_data(writer, data: str):
    writer.write(data.encode())
    await writer.drain()


@asynccontextmanager
async def open_connection(host, port):
    reader, writer = await asyncio.open_connection(host=host, port=port)
    try:
        yield reader, writer
    finally:
        writer.close()


async def show_history(messages_queue, task_status: TaskStatus = TASK_STATUS_IGNORED):
    task_status.started()

    if await aiofiles.os.path.exists(CHAT_HISTORY_PATH):
        async with aiofiles.open(CHAT_HISTORY_PATH, mode='r') as file:
            lines = await file.readlines()
        for line in lines:
            messages_queue.put_nowait(line)
