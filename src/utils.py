import io
import numpy as np
from PIL import Image
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError

SIG_BITS = 64*8

def load_rgba(path) -> np.ndarray:
    return np.array(Image.open(path).convert("RGBA"), dtype=np.uint8)


def clear_lsb(arr: np.ndarray) -> np.ndarray:
    out = arr.copy()
    out[..., :3] &= 0xFE
    return out


def signed_payload(arr: np.ndarray) -> bytes:
    h, w, _ = arr.shape
    return b"RGB" + w.to_bytes(4, "big") + h.to_bytes(4, "big") + arr.tobytes()


def sign_and_embed(src, dst, signing_key: SigningKey):
    arr = clear_lsb(load_rgba(src))
    rgb = arr[..., :3]
    if rgb.size < SIG_BITS:
        raise ValueError("Image too small to hold the signature")

    sig = signing_key.sign(signed_payload(arr)).signature
    bits = np.unpackbits(np.frombuffer(sig, dtype=np.uint8))

    flat = rgb.reshape(-1).copy()
    flat[:SIG_BITS] |= bits
    arr[..., :3] = flat.reshape(rgb.shape)

    Image.fromarray(arr, "RGBA").save(dst, format="PNG")


def verify_embedded(path, verify_key: VerifyKey) -> bool:
    arr = load_rgba(path)
    flat = arr[..., :3].reshape(-1)
    sig = np.packbits(flat[:SIG_BITS] & 1).tobytes()
    try:
        verify_key.verify(signed_payload(clear_lsb(arr)), sig)
        return True
    except BadSignatureError:
        return False


def load_rgba_from_bytes(data: bytes) -> np.ndarray:
    return np.array(Image.open(io.BytesIO(data)).convert("RGBA"), dtype=np.uint8)


def verify_embedded_from_bytes(data: bytes, verify_key: VerifyKey) -> bool:
    arr = load_rgba_from_bytes(data)
    flat = arr[..., :3].reshape(-1)
    sig = np.packbits(flat[:SIG_BITS] & 1).tobytes()
    try:
        verify_key.verify(signed_payload(clear_lsb(arr)), sig)
        return True
    except BadSignatureError:
        return False