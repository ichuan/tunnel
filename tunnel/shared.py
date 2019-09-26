#!/usr/bin/env python
# coding: utf-8
# yc@2019/09/25

import asyncio
import logging
import argparse
import ipaddress

from tunnel.consts import BUFFER_SIZE


logger = logging.getLogger('tunnel')


class StreamClosedException(Exception):
    pass


async def pipe_stream(reader, writer):
    while True:
        data = await reader.read(BUFFER_SIZE)
        if not data:
            raise StreamClosedException()
        writer.write(data)
        await writer.drain()


async def close_stream(s):
    s.close()
    await s.wait_closed()


def parse_args(desc):
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        '-l', '--listen',
        default='127.0.0.1:8443',
        help='Listen address and port. (Default: 127.0.0.1:8443)'
    )
    parser.add_argument(
        '-f', '--forward',
        required=True,
        help='Forwarding address and port. (e.g.: 127.0.0.1:465)'
    )
    parser.add_argument(
        '-k', '--key',
        required=True,
        help='Key file, used to wrap socket in SSL/TLS'
    )
    parser.add_argument(
        '-c', '--cert',
        required=True,
        help='Cert file, used to wrap socket in SSL/TLS'
    )
    parser.add_argument(
        '-d', '--domain',
        help='Common name in cert file, used by local.py'
    )
    args = parser.parse_args()
    ip, _, port = args.listen.rpartition(':')
    assert ipaddress.ip_address(ip) and 0 < int(port) < 65535
    args.listen = (ip, port)
    ip, _, port = args.forward.rpartition(':')
    assert ipaddress.ip_address(ip) and 0 < int(port) < 65535
    args.forward = (ip, port)
    return args


def handle_connection(args):
    async def _handle_connection(reader, writer):
        peername = writer.get_extra_info('peername')
        logger.info(f'New connection from {peername}')
        try:
            t_reader, t_writer = await asyncio.open_connection(**args)
        except Exception as e:
            logger.error(f'Closing {peername}: {e}')
            await close_stream(writer)
            return
        try:
            await asyncio.gather(
                pipe_stream(reader, t_writer),
                pipe_stream(t_reader, writer),
            )
        except StreamClosedException:
            pass
        except Exception as e:
            logger.error(f'Error forwarding: {e}')
        finally:
            peername2 = t_writer.get_extra_info('peername')
            logger.info(f'Closing {peername} and {peername2}')
            await close_stream(writer)
            await close_stream(t_writer)
    return _handle_connection
