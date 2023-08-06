![logo](https://raw.githubusercontent.com/cybergarage/uecho-py/main/doc/img/logo.png?token=AAEPHD4KEMD7MIIGJNOQPX3BR7O4M)

[![pytest](https://github.com/cybergarage/uecho-py/actions/workflows/pytest.yml/badge.svg)](https://github.com/cybergarage/uecho-py/actions/workflows/pytest.yml)
![](https://img.shields.io/badge/python-3.6-blue.svg)
![](https://img.shields.io/badge/python-3.7-blue.svg)
![](https://img.shields.io/badge/python-3.8-blue.svg)
![](https://img.shields.io/badge/python-3.9-blue.svg)
![](https://img.shields.io/badge/python-3.10-blue.svg)

The `uecho-py` is a portable and cross platform development framework for creating controller applications and devices of [ECHONET Lite][enet] for Python developers. [ECHONET][enet] is an open standard specification for IoT devices in Japan, it specifies more than 100 IoT devices such as crime prevention sensor, air conditioner and refrigerator.

[enet]:http://echonet.jp/english/

## Installation

You can install `uecho-py` using `pip` as the following:

```
 $ pip install uecho
 ```
## Examples

## uechosearch

The [`uechosearch`](bin/uechosearch.py) is a sample controller to search all [ECHONET Lite][enet] nodes in the same local area network as the following usage.

```
Usage : uechosearch
```

The [`uechosearch`](bin/uechosearch.py) searches all [ECHONET Lite][enet] device and profile objects in the local area network, and prints all found objects with the IP address as the following:

```
$ uechosearch
192.168.aaa.bbb [0] 05FF01 
192.168.aaa.cc  [0] 0F2001 [1] 029101 
```

## uechopost

The [`uechopost`](bin/uechopost.py) is a sample controller to post a message to a [ECHONET Lite][enet] node in the same local network as the following usage.


```
Usage : uechopost <address> <obj> <esv> <property (code, data) ...>
```

The [`uechopost`](bin/uechopost.py) can send any request message of [ECHONET Lite][enet] to an object in the specified node, and print the response message. The following example controls the power status of a [ECHONET Lite][enet] standard light device.

```
$ uechopost 192.168.aaa.bbb 029101 62 8A    --> READ REQ (62) : Manufacture Code (0x8A)
192.168.aaaa.bbb 0EF001 72 8A 00000B        --> READ RES (72) : Panasonic (0x00000B)

$ uechopost 192.168.aaa.bbb 029101 62 80    --> READ REQ (62) : Operation status (0x80)
192.168.aaa.bbb 029101 72 80 31             --> READ RES (72) : OFF (0x31)

$ uechopost 192.168.aaa.bbb 029101 61 80 30 --> WRITE REQ (61) : Operation status (0x80) ON (0x30)
192.168.aaa.bbb 029101 71 80                --> WRITE RES (71) : (No Data)

$ uechopost 192.168.aaa.bbb 029101 62 80    --> READ REQ (62) : Operation status (0x80)
192.168.aaa.bbb 029101 72 80 30             --> READ RES (72) : ON (0x30)
```

## References

* [Documentation (docstring)](https://cybergarage.github.io/uecho-py/)

[enet]:http://echonet.jp/english/
