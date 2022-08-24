"""Module for setting vars."""
from environs import Env

env = Env()
env.read_env()

CHAT_HOST = env.str('HOST', 'minechat.dvmn.org')
READ_CHAT_PORT = env.int('READ_PORT', 5000)
SEND_CHAT_PORT = env.int('SEND_PORT', 5050)
CHAT_HISTORY_PATH = env.str('HISTORY_PATH', 'minechat.history')
AUTH_TOKEN = env.str('AUTH_TOKEN', '')
NICKNAME = env.str('NICKNAME', 'anon')
GUI_TITTLE = 'Чат Майнкрафтера'
SEND_GUI_BUTTON = 'Отправить'

FAILED_AUTH_MESSAGE = 'Неизвестный токен. Проверьте его или зарегистрируйтесь заново.'
RECONNECTION_WAIT_TIME = 180
EMPTY_LINE = '\n'
ALIVE_CONN_TEXT = 'Connection is alive.'
WATCHDOG_BEFORE_AUTH_TEXT = f'{ALIVE_CONN_TEXT} Prompt before auth'
SEND_MSG_TEXT = f'{ALIVE_CONN_TEXT} Message sent'
READ_MSG_TEXT = f'{ALIVE_CONN_TEXT} New message in chat'
SUCCESS_AUTH_TEXT = f'{ALIVE_CONN_TEXT} Authorization done'
