from __future__ import annotations

from typing import Optional

from sila2.framework.errors.defined_execution_error import DefinedExecutionError

from .silaservice_feature import SiLAServiceFeature


class UnimplementedFeature(DefinedExecutionError):
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The Feature specified by the given Feature identifier is not implemented by the server."
        super().__init__(SiLAServiceFeature.defined_execution_errors["UnimplementedFeature"], message=message)
