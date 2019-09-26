# tunnel
Network tunneling tools

## Scenario

Suppose *Client* wants to access *Server*, but the network can't be trust. It needs to 
encrypt the traffic, make sure only *Server* can see the data. *Server* also wants to 
verify the data seems from *Client* trully is.

```txt
                      + Untrusted network
                      |
                      |
                      |
+---------+           |             +--------+
| Client  +------------------------>+ Server |
+---------+           |             +--------+
                      +
```

Here comes tunnel. *tunnel.local* for encrypting the traffic, and *tunel.remote* decrypting 
the traffic.

```txt
                                      + Untrusted network
                                      |
                                      |
                                      |
+---------+    +------------+         |           +------------+   +--------+
| Client  +--->+tunnel.local+-------------------->+tunel.remote+-->+ Server |
+---------+    +------------+         |           +------------+   +--------+
                                      +
```

*Client* and *tunnel.local* can be same device, and *tunel.remote* can also be running on *Server*.


## Install

Requires Python3.7.3+

```
python3.7 -m pip install --user tunnel-0.1.0-py3-none-any.whl
```


## Usage

Because tunnel use a bi-verified SSL cert, generate a pair of cert and key using (change "ssl.what5g.com" to other domain):

```sh
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 3650 -nodes -subj "/CN=ssl.what5g.com"
```

Copy `key.pem` and `cert.pem` to both servers of *tunnel.local* and *tunnel.remote*.

Suppose *Client* wants to access port 1080 of *Server*. Start *tunnel.local* as:

```sh
python3.7 -m tunnel.local -l 0.0.0.0:1080 -f tunnel.remote:10800 -k key.pem -c cert.pem -d ssl.what5g.com
```

Start *tunnel.remote* as:

```sh
python3.7 -m tunnel.remote -l 0.0.0.0:10800 -f server:1080 -k key.pem -c cert.pem
```

Finally, let *Client* access port 1080 of *tunnel.local*, resulting accessing port 1080 of *Server*, with traffic encrypted.


## Use Case

- tunneling socks5/http proxy traffic
- tunneling Shadowsocks traffic
