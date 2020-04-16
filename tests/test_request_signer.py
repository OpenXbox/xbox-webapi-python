from ecdsa import SigningKey

from xbox.webapi.common.request_signer import RequestSigner


def test_signing():
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
