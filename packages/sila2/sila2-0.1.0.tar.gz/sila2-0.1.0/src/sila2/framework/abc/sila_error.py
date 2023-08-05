from __future__ import annotations

from abc import ABC, abstractmethod
from base64 import standard_b64decode
from os.path import join
from typing import TYPE_CHECKING

import grpc

from sila2 import resource_dir
from sila2.framework.utils import run_protoc

pb2_module, _ = run_protoc(join(resource_dir, "proto", "SiLAFramework.proto"))

if TYPE_CHECKING:
    from sila2.client.sila_client import SilaClient
    from sila2.pb2_stubs import SiLAFramework_pb2
    from sila2.pb2_stubs.SiLAFramework_pb2 import SiLAError

    pb2_module = SiLAFramework_pb2


class SilaError(Exception, ABC):
    pb2_module: SiLAFramework_pb2 = pb2_module

    def __init__(self, message: str):
        super().__init__(message)

    @abstractmethod
    def to_message(self) -> SiLAError:
        pass

    @classmethod
    @abstractmethod
    def from_message(cls, message: SiLAError, client: SilaClient) -> SiLAError:
        pass

    @staticmethod
    def is_sila_error(exception: Exception) -> bool:
        if not isinstance(exception, grpc.RpcError):
            return False

        if not exception.code() == grpc.StatusCode.ABORTED:
            return False

        try:
            SilaError.pb2_module.SiLAError.FromString(standard_b64decode(exception.details()))
        except:  # noqa: 722
            return False

        return True

    @staticmethod
    def from_rpc_error(rpc_error: grpc.RpcError, client: SilaClient):
        if not SilaError.is_sila_error(rpc_error):
            raise ValueError("Error is no SiLAError")

        sila_err = SilaError.pb2_module.SiLAError.FromString(standard_b64decode(rpc_error.details()))

        if sila_err.HasField("validationError"):
            from sila2.framework.errors.validation_error import ValidationError

            return ValidationError.from_message(sila_err.validationError, client)
        if sila_err.HasField("definedExecutionError"):
            from sila2.framework.errors.defined_execution_error import DefinedExecutionError

            return DefinedExecutionError.from_message(sila_err.definedExecutionError, client)
        if sila_err.HasField("undefinedExecutionError"):
            from sila2.framework.errors.undefined_execution_error import UndefinedExecutionError

            return UndefinedExecutionError.from_message(sila_err.undefinedExecutionError, client)
        if sila_err.HasField("frameworkError"):
            from sila2.framework.errors.framework_error import FrameworkError

            return FrameworkError.from_message(sila_err.frameworkError, client)

        raise NotImplementedError(f"SiLAError type not supported: {sila_err}")  # should not happen
