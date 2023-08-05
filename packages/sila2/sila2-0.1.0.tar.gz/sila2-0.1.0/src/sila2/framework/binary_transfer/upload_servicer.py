from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Dict, Iterable, Optional
from uuid import UUID, uuid4

from grpc import ServicerContext

from sila2.framework.abc.binary_transfer_handler import grpc_module as binary_transfer_grpc_module
from sila2.framework.abc.binary_transfer_handler import pb2_module as binary_transfer_pb2_module
from sila2.framework.binary_transfer.binary_upload_failed import BinaryUploadFailed
from sila2.framework.binary_transfer.invalid_binary_transfer_uuid import InvalidBinaryTransferUUID
from sila2.framework.command.duration import Duration
from sila2.framework.utils import raise_as_rpc_error

if TYPE_CHECKING:
    from sila2.framework.binary_transfer.server_binary_transfer_handler import ServerBinaryTransferHandler
    from sila2.pb2_stubs import SiLABinaryTransfer_pb2


class BinaryUploadServicer(binary_transfer_grpc_module.BinaryUploadServicer):
    binaries_in_progress: Dict[UUID, Dict[int, Optional[bytes]]]
    _duration_field: Duration

    def __init__(self, parent_handler: ServerBinaryTransferHandler):
        self.parent_handler = parent_handler
        self.binaries_in_progress = {}
        self._duration_field = Duration(binary_transfer_pb2_module.SiLAFramework__pb2)

    def CreateBinary(self, request: SiLABinaryTransfer_pb2.CreateBinaryRequest, context: ServicerContext):
        try:
            bin_id = uuid4()
            chunk_count = request.chunkCount

            self.binaries_in_progress[bin_id] = {i: None for i in range(chunk_count)}

            return binary_transfer_pb2_module.CreateBinaryResponse(
                binaryTransferUUID=str(bin_id), lifetimeOfBinary=self._duration_field.to_message(timedelta(minutes=1))
            )
        except Exception as ex:
            raise_as_rpc_error(BinaryUploadFailed(f"Upload of large binary failed: {ex}"), context)

    def UploadChunk(
        self, request_iterator: Iterable[SiLABinaryTransfer_pb2.UploadChunkRequest], context: ServicerContext
    ):
        try:
            for chunk_request in request_iterator:
                bin_id = UUID(chunk_request.binaryTransferUUID)

                if bin_id not in self.binaries_in_progress:
                    raise InvalidBinaryTransferUUID(f"Upload of large binary failed: invalid UUID {bin_id}")

                index = chunk_request.chunkIndex
                payload = chunk_request.payload

                self.binaries_in_progress[bin_id][index] = payload
                if all(isinstance(b, bytes) for b in self.binaries_in_progress[bin_id].values()):
                    self.parent_handler.known_binaries[bin_id] = b"".join(
                        self.binaries_in_progress[bin_id][i] for i in sorted(self.binaries_in_progress[bin_id].keys())
                    )
                    self.binaries_in_progress.pop(bin_id)

                yield binary_transfer_pb2_module.UploadChunkResponse(
                    binaryTransferUUID=str(bin_id),
                    chunkIndex=index,
                    lifetimeOfBinary=self._duration_field.to_message(timedelta(minutes=1)),
                )
        except InvalidBinaryTransferUUID as ex:
            raise_as_rpc_error(ex, context)
        except Exception as ex:
            raise_as_rpc_error(BinaryUploadFailed(f"Upload of large binary failed: {ex}"), context)

    def DeleteBinary(self, request: binary_transfer_pb2_module.DeleteBinaryRequest, context: ServicerContext):
        try:
            bin_id = UUID(request.binaryTransferUUID)

            if bin_id not in self.parent_handler.known_binaries:
                raise InvalidBinaryTransferUUID(f"Deletion of large binary failed: invalid UUID {bin_id}")

            self.parent_handler.known_binaries.pop(UUID(request.binaryTransferUUID))
            return binary_transfer_pb2_module.DeleteBinaryResponse()
        except InvalidBinaryTransferUUID as ex:
            raise_as_rpc_error(ex, context)
        except Exception as ex:
            raise_as_rpc_error(BinaryUploadFailed(f"Deletion of large binary failed: {ex}"), context)
