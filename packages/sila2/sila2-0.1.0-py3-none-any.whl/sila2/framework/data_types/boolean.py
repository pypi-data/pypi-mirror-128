from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type

from sila2.framework.abc.data_type import DataType
from sila2.framework.abc.named_data_node import NamedDataNode

if TYPE_CHECKING:
    from sila2.pb2_stubs import SiLAFramework_pb2
    from sila2.pb2_stubs.SiLAFramework_pb2 import Boolean as SilaBoolean


class Boolean(DataType):
    native_type = bool
    message_type: Type[SilaBoolean]

    def __init__(self, silaframework_pb2_module: SiLAFramework_pb2):
        self.message_type = silaframework_pb2_module.Boolean

    def to_native_type(self, message: SilaBoolean, toplevel_named_data_node: Optional[NamedDataNode] = None) -> bool:
        return message.value

    def to_message(self, value: bool, toplevel_named_data_node: Optional[NamedDataNode] = None) -> SilaBoolean:
        if not isinstance(value, bool):
            raise TypeError("Expected a bool value")
        return self.message_type(value=value)
