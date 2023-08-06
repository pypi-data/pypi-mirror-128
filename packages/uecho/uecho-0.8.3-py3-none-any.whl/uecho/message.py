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

from .protocol.message import Message as ProtocolMessage

from .util.bytes import Bytes
from .property import Property
from .object import Object
from .node_profile import NodeProfile


class Message(ProtocolMessage):

    def __init__(self):
        super(Message, self).__init__()

    def add_property(self, prop: Property):
        if not isinstance(prop, Property):
            return False
        self.properties.append(prop)
        return True

    def add_object_as_class_instance_list_property(self, obj: Object):
        if not isinstance(obj, Object):
            return False
        prop = Property()
        prop.code = NodeProfile.CLASS_SELF_NODE_INSTANCE_LIST_S
        prop_data = bytearray([1])
        prop_data.extend(Bytes.from_int(obj.code, Object.CODE_SIZE))
        prop.data = prop_data
        self.properties.append(prop)
        return True
