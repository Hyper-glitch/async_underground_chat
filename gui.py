import asyncio
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from aiofiles import os
from anyio import TASK_STATUS_IGNORED, create_task_group
from anyio.abc import TaskStatus

from async_chat_utils import open_connection
from chat_utils import create_parser
from enums import ReadConnectionStateChanged, SendingConnectionStateChanged
from exceptions import TkAppClosed
from sender import registrate
from settings import GUI_TITTLE, SEND_GUI_BUTTON, CHAT_HOST, SEND_CHAT_PORT


class NicknameReceived:
    def __init__(self, nickname):
        self.nickname = nickname


def process_new_message(input_field, sending_queue):
    text = input_field.get()
    sending_queue.put_nowait(text)
    input_field.delete(0, tk.END)


async def update_tk(root_frame, interval=1 / 120, task_status: TaskStatus = TASK_STATUS_IGNORED):
    task_status.started()

    while True:
        try:
            root_frame.update()
        except tk.TclError:
            # if application has been destroyed/closed
            raise TkAppClosed()
        await asyncio.sleep(interval)


async def update_conversation_history(panel, messages_queue, task_status: TaskStatus = TASK_STATUS_IGNORED):
    task_status.started()

    while True:
        msg = await messages_queue.get()

        panel['state'] = 'normal'
        if panel.index('end-1c') != '1.0':
            panel.insert('end', '\n')
        panel.insert('end', msg)
        # TODO сделать промотку умной, чтобы не мешала просматривать историю сообщений
        # ScrolledText.frame
        # ScrolledText.vbar
        panel.yview(tk.END)
        panel['state'] = 'disabled'


async def update_status_panel(status_labels, status_updates_queue, task_status: TaskStatus = TASK_STATUS_IGNORED):
    task_status.started()

    nickname_label, read_label, write_label = status_labels

    read_label['text'] = f'Чтение: нет соединения'
    write_label['text'] = f'Отправка: нет соединения'
    nickname_label['text'] = f'Имя пользователя: неизвестно'

    while True:
        msg = await status_updates_queue.get()
        if isinstance(msg, ReadConnectionStateChanged):
            read_label['text'] = f'Чтение: {msg}'

        if isinstance(msg, SendingConnectionStateChanged):
            write_label['text'] = f'Отправка: {msg}'

        if isinstance(msg, NicknameReceived):
            nickname_label['text'] = f'Имя пользователя: {msg.nickname}'


def create_status_panel(root_frame):
    status_frame = tk.Frame(root_frame)
    status_frame.pack(side='bottom', fill=tk.X)

    connections_frame = tk.Frame(status_frame)
    connections_frame.pack(side='left')
    label_kwargs = {'height': 1, 'fg': 'grey', 'font': 'arial 10', 'anchor': 'w'}

    nickname_label = tk.Label(connections_frame, **label_kwargs)
    nickname_label.pack(side='top', fill=tk.X)

    status_read_label = tk.Label(connections_frame, **label_kwargs)
    status_read_label.pack(side='top', fill=tk.X)

    status_write_label = tk.Label(connections_frame, **label_kwargs)
    status_write_label.pack(side='top', fill=tk.X)

    return nickname_label, status_read_label, status_write_label


async def draw(messages_queue, sending_queue, status_updates_queue, task_status: TaskStatus = TASK_STATUS_IGNORED):
    task_status.started()

    root = tk.Tk()

    root.title(GUI_TITTLE)

    root_frame = tk.Frame()
    root_frame.pack(fill='both', expand=True)

    status_labels = create_status_panel(root_frame)

    input_frame = tk.Frame(root_frame)
    input_frame.pack(side='bottom', fill=tk.X)

    input_field = tk.Entry(input_frame)
    input_field.pack(side='left', fill=tk.X, expand=True)

    input_field.bind('<Return>', lambda event: process_new_message(input_field, sending_queue))

    send_button = tk.Button(input_frame)
    send_button['text'] = SEND_GUI_BUTTON
    send_button['command'] = lambda: process_new_message(input_field, sending_queue)
    send_button.pack(side='left')

    conversation_panel = ScrolledText(root_frame, wrap='none')
    conversation_panel.pack(side='top', fill='both', expand=True)

    async with create_task_group() as tg:
        await tg.start(update_tk, root_frame)
        await tg.start(update_conversation_history, conversation_panel, messages_queue)
        await tg.start(update_status_panel, status_labels, status_updates_queue)


async def get_token(token_queue, root, host, send_port, task_status: TaskStatus = TASK_STATUS_IGNORED):
    task_status.started()

    accounts_path = 'users_info'
    await os.makedirs(accounts_path, exist_ok=True)

    username = await token_queue.get()

    async with open_connection(host, send_port) as conn:
        reader, writer = conn
        reg_info = await registrate(reader, writer, username, accounts_path)

    token = reg_info['account_hash']
    token_queue.put_nowait(token)
    messagebox.showinfo(message=f'Your token is in the path: {accounts_path}/{token}')
    root.destroy()
    raise asyncio.CancelledError


async def draw_registration(queue, host, send_port, task_status: TaskStatus = TASK_STATUS_IGNORED):
    task_status.started()

    root = tk.Tk()
    root.geometry('600x600+1000+400')
    root.title('MineChat')

    tk.Label(text='Welcome to MainChat!\nPlease Registrate a new account', width=400, height=5).pack()
    tk.Label(root, text='Enter your username, then push Enter', width=200, height=2).pack()

    input_field = tk.Entry(root)
    input_field.pack()
    input_field.bind('<Return>', lambda event: process_new_message(input_field, queue))

    async with create_task_group() as tg:
        await tg.start(update_tk, root)
        await tg.start(get_token, queue, root, host, send_port)
