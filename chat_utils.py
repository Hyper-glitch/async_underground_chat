import json
from typing import Union

import aiofiles


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
