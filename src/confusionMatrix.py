import csv
from datetime import datetime
import re
from nacl.signing import VerifyKey
from config import VERIFY_KEY_PATH, IMAGES_LABELED_PATH, IMG_EXTS, CF_OUTPUTS_PATH
from utils import verify_embedded

with open(VERIFY_KEY_PATH, "rb") as f:
    verify_key = VerifyKey(f.read())

files = IMAGES_LABELED_PATH.glob("*")
results = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
failed = []
OUTPUT_CSV = CF_OUTPUTS_PATH / f"results_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv"

for path in files:
    if not path.is_file() and path.suffix.lower() not in IMG_EXTS:
        continue
    try:
        label_rg = re.search(r"\\(true|false)_[^\\]*$", str(path))
        label = label_rg.group(1)
        result = verify_embedded(path, verify_key)
        match label:
            case "true":
                results["tp" if result else "fn"] += 1
            case "false":
                results["tn" if not result else "fp"] += 1
    except Exception as e:
        failed.append((str(path), str(e)))

if len(failed) > 0:
    print(failed)

with open(OUTPUT_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results.keys())
    writer.writeheader()
    writer.writerow(results)

print(f"Saved results to {OUTPUT_CSV}\n")