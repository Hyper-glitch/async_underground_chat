import aiofiles


async def write_chat_msg(data: str, path: str):
    """Write messages from chat line by line to a file.

    Args:
        data: message from chat for writing in a file.
        path: filepath for chat history.
    """
    async with aiofiles.open(path, mode='a') as file:
        await file.write(data)
