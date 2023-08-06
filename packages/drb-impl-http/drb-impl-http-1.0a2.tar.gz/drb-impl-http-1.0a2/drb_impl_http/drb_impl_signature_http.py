import uuid

from drb.factory import DrbSignature, DrbSignatureType, DrbFactory

from drb import DrbNode
from drb_impl_http import DrbHttpFactory


class DrbHttpSignature(DrbSignature):
    def __init__(self):
        self._factory = DrbHttpFactory()

    @property
    def uuid(self) -> uuid.UUID:
        return uuid.UUID('b065a5aa-35a3-11ec-8d3d-0242ac130003')

    @property
    def label(self) -> str:
        return 'http'

    @property
    def category(self) -> DrbSignatureType:
        return DrbSignatureType.PROTOCOL

    @property
    def factory(self) -> DrbFactory:
        return self._factory

    def match(self, node: DrbNode) -> bool:
        if node.path.is_remote:
            scheme = node.path.scheme
            return scheme == 'http'
        return False
