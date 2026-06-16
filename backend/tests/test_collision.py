import uuid
import hashlib
import base64
import string
import random

def _generate_share_token() -> str:
    raw = hashlib.sha256(str(uuid.uuid4()).encode()).digest()
    token = base64.b64encode(raw, altchars=b"AB").decode()[:8]
    return token

def test_token_collision_10000():
    tokens = {_generate_share_token() for _ in range(10000)}
    assert len(tokens) == 10000

def _random_token() -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=8))

def test_partial_token_collision_10000():
    tokens = {_random_token() for _ in range(10000)}
    assert len(tokens) == 10000
