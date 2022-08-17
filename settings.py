"""Module for setting vars."""
from environs import Env

env = Env()
env.read_env()

CHAT_HOST = env.str('HOST', 'minechat.dvmn.org')
READ_CHAT_PORT = env.int('PORT', 5000)
SEND_CHAT_PORT = env.int('PORT', 5050)
CHAT_HISTORY_PATH = env.str('HISTORY_PATH', 'minechat.history')

RECONNECTION_WAIT_TIME = 180
