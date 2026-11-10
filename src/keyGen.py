from nacl.signing import SigningKey
from config import SIGNING_KEY_PATH, VERIFY_KEY_PATH

signing_key = SigningKey.generate()
verify_key = signing_key.verify_key

with open(SIGNING_KEY_PATH, "wb") as f:
    f.write(signing_key.encode())
with open(VERIFY_KEY_PATH, "wb") as f:
    f.write(verify_key.encode())