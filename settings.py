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
TIMEOUT_WRITE_EXPIRED_SEC = env.int('TIMEOUT_WRITE_EXPIRED_SEC', 1)
TIMEOUT_READ_EXPIRED_SEC = env.int('TIMEOUT_READ_EXPIRED_SEC', 3)
SERVER_PING_FREQUENCY_SEC = env.int('SERVER_PING_FREQUENCY', 1)

GUI_TITTLE = 'Чат Майнкрафтера'
SEND_GUI_BUTTON = 'Отправить'
FAILED_AUTH_MESSAGE = 'Неизвестный токен. Проверьте его или зарегистрируйтесь заново.'
ALIVE_CONN_TEXT = 'Connection is alive.'
DEAD_CONN_TEXT = 'Connection is dead.'
TIMEOUT_ERROR_TEXT = 'Timeout is elapsed'
RECONNECTION_TEXT = 'Try to reconnection'
PING_SERVER_TEXT = f'{ALIVE_CONN_TEXT} Ping server'
WATCHDOG_BEFORE_AUTH_TEXT = f'{ALIVE_CONN_TEXT} Prompt before auth'
SEND_MSG_TEXT = f'{ALIVE_CONN_TEXT} Message sent'
READ_MSG_TEXT = f'{ALIVE_CONN_TEXT} New message in chat'
SUCCESS_AUTH_TEXT = f'{ALIVE_CONN_TEXT} Authorization done'

LONG_WAIT_RECONNECTION_SEC = 60
SHORT_WAIT_RECONNECTION_SEC = 5
LAST_GUI_DRAW_QUEUE = 3
MAX_ATTEMPTS_TO_RECONNECTION = 10

EMPTY_LINE = '\n'
