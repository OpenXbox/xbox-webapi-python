"""
Request Signer

Employed for generating the "Signature" header in authentication requests.
"""
import base64
from datetime import datetime
import hashlib
import struct

from ecdsa import NIST256p, SigningKey

from xbox.webapi.authentication.models import SignaturePolicy
from xbox.webapi.common import filetimes

DEFAULT_SIGNING_POLICY = SignaturePolicy(
    version=1, supported_algorithms=["ES256"], max_body_bytes=8192
)


class RequestSigner:
    def __init__(self, signing_key=None, signing_policy=None):
        self.signing_key = signing_key or SigningKey.generate(curve=NIST256p)
        self.signing_policy = signing_policy or DEFAULT_SIGNING_POLICY

        pk_point = self.signing_key.verifying_key.pubkey.point
        self.proof_field = {
            "use": "sig",
            "alg": self.signing_policy.supported_algorithms[0],
            "kty": "EC",
            "crv": "P-256",
            "x": self.__encode_ec_coord(pk_point.x()),
            "y": self.__encode_ec_coord(pk_point.y()),
        }

    def export_signing_key(self) -> str:
        return self.signing_key.to_pem().decode()

    @staticmethod
    def import_signing_key(signing_key: str) -> SigningKey:
        return SigningKey.from_pem(signing_key)

    @classmethod
    def from_pem(cls, pem_string: str):
        request_signer = RequestSigner.import_signing_key(pem_string)
        return cls(request_signer)

    @staticmethod
    def get_timestamp_buffer(dt: datetime) -> bytes:
        """
        Get usable buffer from datetime

        dt: Input datetime

        Returns:
            bytes: FILETIME buffer (network order/big endian)
        """
        filetime = filetimes.dt_to_filetime(dt)
        return struct.pack("!Q", filetime)

    @staticmethod
    def get_signature_version_buffer(version: int) -> bytes:
        """
        Get big endian uint32 bytes-representation from
        signature version

        version: Signature version

        Returns: Version as uint32 big endian bytes
        """
        return struct.pack("!I", version)

    def sign(
        self,
        method: str,
        path_and_query: str,
        body: bytes = b"",
        authorization: str = "",
        timestamp: datetime = None,
    ) -> str:
        if timestamp is None:
            timestamp = datetime.utcnow()

        signature = self._sign_raw(
            method, path_and_query, body, authorization, timestamp
        )
        return base64.b64encode(signature).decode("ascii")

    def _sign_raw(
        self,
        method: str,
        path_and_query: str,
        body: bytes,
        authorization: str,
        timestamp: datetime,
    ) -> bytes:
        # Calculate hash
        signature_version_bytes = self.get_signature_version_buffer(
            self.signing_policy.version
        )
        ts_bytes = self.get_timestamp_buffer(timestamp)
        hash = self._hash(
            signature_version_bytes,
            method,
            path_and_query,
            body,
            authorization,
            ts_bytes,
            self.signing_policy.max_body_bytes,
        )

        # Sign the hash
        signature = self.signing_key.sign_digest_deterministic(hash)

        # Return signature version + timestamp encoded + signature
        return signature_version_bytes + ts_bytes + signature

    @staticmethod
    def _hash(
        signature_version: bytes,
        method: str,
        path_and_query: str,
        body: bytes,
        authorization: str,
        ts_bytes: bytes,
        max_body_bytes: int,
    ) -> bytes:
        hash = hashlib.sha256()

        # Version + null
        hash.update(signature_version)
        hash.update(b"\x00")

        # Timestamp + null
        hash.update(ts_bytes)
        hash.update(b"\x00")

        # Method (in uppercase) + null
        hash.update(method.upper().encode("ascii"))
        hash.update(b"\x00")

        # Path and query
        hash.update(path_and_query.encode("ascii"))
        hash.update(b"\x00")

        # Authorization (even if an empty string)
        hash.update(authorization.encode("ascii"))
        hash.update(b"\x00")

        # Body
        body_size_to_hash = min(len(body), max_body_bytes)
        hash.update(body[:body_size_to_hash])
        hash.update(b"\x00")

        return hash.digest()

    @staticmethod
    def __base64_escaped(binary: bytes) -> str:
        encoded = base64.b64encode(binary).decode("ascii")
        encoded = encoded.rstrip("=")
        encoded = encoded.replace("+", "-")
        encoded = encoded.replace("/", "_")
        return encoded

    @staticmethod
    def __encode_ec_coord(coord) -> str:
        return RequestSigner.__base64_escaped(coord.to_bytes(32, "big"))
