"""Declares :class:`EllipticCurvePrivateKey`."""
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import utils

from .. import oid
from ..algorithms import SECP256K1SHA256
from ..algorithms import SECP256R1SHA256
from ..private import PrivateKey
from .public import EllipticCurvePublicKey


class EllipticCurvePrivateKey(PrivateKey):
    __algorithm_mapping = {
        'P-256K'    : oid.SECP256K1,
        'SECP256K1' : oid.SECP256K1,
        'P-256'     : oid.ECDSASHA256,
        'SECP256R1' : oid.ECDSASHA256,
    }

    capabilities = [
        SECP256K1SHA256,
        SECP256R1SHA256
    ]

    @property
    def curve(self):
        return self.__key.curve

    @property
    def id(self) -> str:
        return self.keyid

    @property
    def keyid(self) -> str:
        return self.get_public_key().keyid

    @classmethod
    def generate(cls, curve):
        """Generate a new elliptic curve private key."""
        return cls(ec.generate_private_key(curve()))

    def __init__(self, key):
        self.__key = key
        self.__public = key.public_key()

    def setup(self, opts):
        pass

    def get_public_key(self) -> EllipticCurvePublicKey:
        return EllipticCurvePublicKey(self.__public)

    def has_public_key(self) -> bool:
        """Return a boolean indicating if the private key is able to
        extract and provide its public key.
        """
        return True

    async def sign(self,
        digest: bytes,
        algorithm,
        *args, **kwargs
    ) -> bytes:
        """Returns the signature of byte-sequence `blob`, DER-encoded."""
        return self.__key.sign(
            digest,
            ec.ECDSA(utils.Prehashed(algorithm))
        )

    def _get_key(self):
        return self.__key
