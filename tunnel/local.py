#!/usr/bin/env python
# coding: utf-8
# yc@2019/09/25

import ssl
import asyncio
import logging
import logging.config

from tunnel.shared import parse_args, handle_connection


logger = logging.getLogger('tunnel')


async def start_forwarder(args):
    if not args.domain:
        print('--domain required. It is "Common Name" in cert file')
        return

    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=args.cert)
    ctx.load_cert_chain(certfile=args.cert, keyfile=args.key)

    server = await asyncio.start_server(
        handle_connection({
            'ssl': ctx,
            'server_hostname': args.domain,
            'host': args.forward[0],
            'port': args.forward[1],
        }),
        host=args.listen[0],
        port=args.listen[1],
        backlog=1024,
    )
    logger.info(f'Server listening at {args.listen}...')
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        level=logging.INFO,
    )
    args = parse_args('tunnel/local')
    asyncio.run(start_forwarder(args))
