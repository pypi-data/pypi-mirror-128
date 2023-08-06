# Copyright (C) 2021 Satoshi Konno. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .object import Object


class Node(object):
    PORT = 3610

    def __init__(self):
        self.__address = ()
        self.__objects = {}

    def set_address(self, addr):
        if not isinstance(addr, tuple) or len(addr) != 2:
            return False
        self.__address = addr
        return True

    @property
    def address(self):
        return self.__address

    @property
    def ip(self):
        return self.__address[0]

    @property
    def port(self):
        return Node.PORT

    def add_object(self, obj):
        if not isinstance(obj, Object):
            return False
        self.__objects[obj.code] = obj
        return True

    @property
    def objects(self):
        objs = []
        for obj in self.__objects.values():
            objs.append(obj)
        return objs

    def has_object(self, code):
        return code in self.__objects.keys()
