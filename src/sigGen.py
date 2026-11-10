from nacl.signing import SigningKey
from config import SIGNING_KEY_PATH, IMAGES_INPUTS_PATH, IMAGES_OUTPUTS_PATH, IMG_EXTS
from utils import sign_and_embed

with open(SIGNING_KEY_PATH, "rb") as f:
    signing_key = SigningKey(f.read())

files = IMAGES_INPUTS_PATH.glob("*")
results = {"signed": 0, "failed": []}

for path in files:
    if not path.is_file() or path.suffix.lower() not in IMG_EXTS:
        continue
    try:
        sign_and_embed(path, IMAGES_OUTPUTS_PATH / path.name, signing_key)
        results["signed"] += 1
    except Exception as e:
        results["failed"].append((str(path), str(e)))

print("Results:", "\nSigned: ", results["signed"], "\nFailed: ", len(results["failed"]))