from ecdsa import SigningKey

from xbox.webapi.common.request_signer import RequestSigner


def test_real():
    signer = RequestSigner()

    # This request and its hash has been obtained by tracing a live,
    # running Xbox authentication process under Windows 10
    with open("tests/data/real_signed_request.json", "rb") as f:
        body = f.read()

    test_hash = signer._hash(
        method="POST",
        path_and_query="/xsts/authorize",
        body=body,
        authorization="",
        ts_bytes=(132315559631448749).to_bytes(8, "big"),
    )
    assert (
        test_hash.hex()
        == "c063346ae3212fde085620ceb162452b048b7327dd26cec5f30ffbdf654ac6c0"
    )


def test_synthetic():
    with open("tests/data/test_signing_key.pem") as f:
        signing_key = SigningKey.from_pem(f.read())

    signer = RequestSigner(signing_key)

    correct_proof = {
        "crv": "P-256",
        "alg": "ES256",
        "use": "sig",
        "kty": "EC",
        "x": "OKyCQ9qH5U4lZcS0c5_LxIyKvOpKe0l3x4Eg5OgDbzc",
        "y": "syjS0YE9vH3eBat61P9TkCpseo0qtL0weQKP-PJtIho",
    }
    assert signer.proof_field == correct_proof

    import datetime

    dt_timestamp = datetime.datetime.utcfromtimestamp(1586999965)
    ts_bytes = RequestSigner.get_timestamp_buffer(dt_timestamp)

    test_hash = signer._hash(
        method="POST",
        path_and_query="/path?query=1",
        body=b"thebodygoeshere",
        authorization="XBL3.0 x=userid;jsonwebtoken",
        ts_bytes=ts_bytes,
    )
    assert (
        test_hash.hex()
        == "f7d61b6f8d4dcd86da1aa8553f0ee7c15450811e7cd2759364e22f67d853ff50"
    )

    test_signature = signer.sign(
        method="POST",
        path_and_query="/path?query=1",
        body=b"thebodygoeshere",
        authorization="XBL3.0 x=userid;jsonwebtoken",
        timestamp=dt_timestamp,
    )

    assert (
        test_signature
        == "AAAAAQHWE40Q98yAFe3R7GuZfvGA350cH7hWgg4HIHjaD9lGYiwxki6bNyGnB8dMEIfEmBiuNuGUfWjY5lL2h44X/VMGOkPIezVb7Q=="
    )


def test_import():
    with open("tests/data/test_signing_key.pem") as f:
        key = f.read()

    signer = RequestSigner.from_pem(key)
    export = signer.export_signing_key()

    assert key == export
