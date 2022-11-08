import base64
from binascii import unhexlify
import pytest
from ecdsa.keys import VerifyingKey, BadSignatureError

from xbox.webapi.common.request_signer import RequestSigner


def test_synthetic_proof_key(synthetic_request_signer: RequestSigner):
    correct_proof = {
        "crv": "P-256",
        "alg": "ES256",
        "use": "sig",
        "kty": "EC",
        "x": "OKyCQ9qH5U4lZcS0c5_LxIyKvOpKe0l3x4Eg5OgDbzc",
        "y": "syjS0YE9vH3eBat61P9TkCpseo0qtL0weQKP-PJtIho",
    }
    assert synthetic_request_signer.proof_field == correct_proof


def test_synthetic_concat(synthetic_request_signer: RequestSigner, synthetic_timestamp):
    ts_bytes = RequestSigner.get_timestamp_buffer(synthetic_timestamp)

    test_data = synthetic_request_signer._concat_data_to_sign(
        signature_version=b"\x00\x00\x00\x01",
        method="POST",
        path_and_query="/path?query=1",
        body=b"thebodygoeshere",
        authorization="XBL3.0 x=userid;jsonwebtoken",
        ts_bytes=ts_bytes,
        max_body_bytes=8192,
    )

    assert (
        test_data.hex()
        == "000000010001d6138d10f7cc8000504f5354002f706174683f71756572793d310058424c332e3020783d7573657269643b6a736f6e776562746f6b656e00746865626f6479676f65736865726500"
    )


def test_synthetic_hash(synthetic_request_signer: RequestSigner, synthetic_timestamp):
    ts_bytes = RequestSigner.get_timestamp_buffer(synthetic_timestamp)

    test_data = synthetic_request_signer._concat_data_to_sign(
        signature_version=b"\x00\x00\x00\x01",
        method="POST",
        path_and_query="/path?query=1",
        body=b"thebodygoeshere",
        authorization="XBL3.0 x=userid;jsonwebtoken",
        ts_bytes=ts_bytes,
        max_body_bytes=8192,
    )

    test_hash = synthetic_request_signer._hash(test_data)

    assert (
        test_hash.hex()
        == "f7d61b6f8d4dcd86da1aa8553f0ee7c15450811e7cd2759364e22f67d853ff50"
    )


def test_synthetic_signature(
    synthetic_request_signer: RequestSigner, synthetic_timestamp
):
    test_signature = synthetic_request_signer.sign(
        method="POST",
        path_and_query="/path?query=1",
        body=b"thebodygoeshere",
        authorization="XBL3.0 x=userid;jsonwebtoken",
        timestamp=synthetic_timestamp,
    )

    assert (
        test_signature
        == "AAAAAQHWE40Q98yAFe3R7GuZfvGA350cH7hWgg4HIHjaD9lGYiwxki6bNyGnB8dMEIfEmBiuNuGUfWjY5lL2h44X/VMGOkPIezVb7Q=="
    )


def test_synthetic_verify_digest(
    synthetic_request_signer: RequestSigner, ecdsa_verifying_key: VerifyingKey
):
    message = unhexlify(
        "f7d61b6f8d4dcd86da1aa8553f0ee7c15450811e7cd2759364e22f67d853ff50"
    )
    signature = base64.b64decode(
        "Fe3R7GuZfvGA350cH7hWgg4HIHjaD9lGYiwxki6bNyGnB8dMEIfEmBiuNuGUfWjY5lL2h44X/VMGOkPIezVb7Q=="
    )
    invalid_signature = b"\xFF" + bytes(signature)[1:]
    success = synthetic_request_signer.verify_digest(signature, message)
    success_via_vk = synthetic_request_signer.verify_digest(
        signature, message, ecdsa_verifying_key
    )
    with pytest.raises(BadSignatureError):
        synthetic_request_signer.verify_digest(invalid_signature, message)

    assert success is True
    assert success_via_vk is True


def test_import(ecdsa_signing_key_str: str):
    signer = RequestSigner.from_pem(ecdsa_signing_key_str)
    export = signer.export_signing_key()

    assert ecdsa_signing_key_str == export
