"""Module with functions that helps run chat."""
import argparse
import logging


def create_parser() -> argparse.ArgumentParser:
    """Create arg parser and add arguments.

    Returns:
        namespace: values or arguments, that parsed.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-H', '--host', help='TCP/IP hostname to listen chat (default: %(default)r)',
    )
    parser.add_argument(
        '-R', '--read_port', help='TCP/IP port for reading messages from the chat (default: %(default)r)', type=int,
    )
    parser.add_argument(
        '-S', '--send_port', help='TCP/IP port for sending messages to the chat (default: %(default)r)', type=int,
    )
    parser.add_argument(
        '-P', '--path', help='a path to write chat history', type=str,
    )
    parser.add_argument(
        '-T', '--token', help='token that authorize user in chat', type=str,
    )
    parser.add_argument(
        '-N', '--nickname', help='your alias in chat', type=str,
    )
    return parser


def set_up_logger(logger):
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(u'%(message)s'))
    logger.addHandler(handler)
