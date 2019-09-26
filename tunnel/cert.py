#!/usr/bin/env python
# coding: utf-8
# yc@2019/09/25

if __name__ == '__main__':
    print(
        'Using the following command to generate a self-signed cert and key file:\n\n'
        '  openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days '
        '3650 -nodes -subj "/CN=ssl.what3g.com"\n\n'
        'Customize CN ("ssl.what3g.com" in this example), required by local.py'
    )
