from nacl.signing import VerifyKey
from config import VERIFY_KEY_PATH, IMAGES_OUTPUTS_PATH, IMG_EXTS
from utils import verify_embedded

with open(VERIFY_KEY_PATH, "rb") as f:
    verify_key = VerifyKey(f.read())

files = IMAGES_OUTPUTS_PATH.glob("*")
results = {"valid": 0, "invalid": 0, "failed": []}

for path in files:
    if not path.is_file() or path.suffix.lower() not in IMG_EXTS:
        continue
    try:
        result = verify_embedded(path, verify_key)
        if result:
            results["valid"] += 1
        else:
            results["invalid"] += 1
    except Exception as e:
        results["failed"].append((str(path), str(e)))

print("Results:", "\nValid: ", results["valid"], "\nInvalid: ", results["invalid"], "\nFailed: ", len(results["failed"]))