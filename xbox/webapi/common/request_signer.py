"""
Request Signer

Employed for generating the "Signature" header in authentication requests.
"""
import base64
import hashlib
import time

from ecdsa import NIST256p, SigningKey


class RequestSigner:

    # Version 1
    SIGNATURE_VERSION = b"\x00\x00\x00\x01"

    def __init__(self, signing_key=None):
        self.signing_key = signing_key or SigningKey.generate(curve=NIST256p)

        pk_point = self.signing_key.verifying_key.pubkey.point
        self.proof_field = {
            "use": "sig",
            "alg": "ES256",
            "kty": "EC",
            "crv": "P-256",
            "x": self.__encode_ec_coord(pk_point.x()),
            "y": self.__encode_ec_coord(pk_point.y()),
        }

    def sign(self, method, path_and_query, body=b"", authorization="", timestamp=None):
        if timestamp is None:
            timestamp = round(time.time())

        signature = self._sign_raw(
            method, path_and_query, authorization, body, timestamp
        )
        return base64.b64encode(signature).decode("ascii")

    def _sign_raw(self, method, path_and_query, body, authorization, timestamp):
        # Calculate hash
        ts_bytes = timestamp.to_bytes(8, 'big')
        hash = self._hash(method, path_and_query, body, authorization, ts_bytes)

        # Sign the hash
        signature = self.signing_key.sign_digest_deterministic(hash)

        # Return signature version + timestamp encoded + signature
        return self.SIGNATURE_VERSION + ts_bytes + signature

    @staticmethod
    def _hash(method, path_and_query, authorization, body, ts_bytes):
        hash = hashlib.sha256()

        # Version + null
        hash.update(RequestSigner.SIGNATURE_VERSION)
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
        hash.update(authorization.encode('ascii'))
        hash.update(b'\x00')

        # Body
        hash.update(body)
        hash.update(b"\x00")

        return hash.digest()

    @staticmethod
    def __base64_escaped(binary):
        encoded = base64.b64encode(binary).decode("ascii")
        encoded = encoded.rstrip("=")
        encoded = encoded.replace("+", "-")
        encoded = encoded.replace("/", "_")
        return encoded

    @staticmethod
    def __encode_ec_coord(coord):
        return RequestSigner.__base64_escaped(coord.to_bytes(32, "big"))
