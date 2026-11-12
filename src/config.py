from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SIGNING_KEY_PATH = BASE_DIR / "keys" / "signing.key"
VERIFY_KEY_PATH = BASE_DIR / "keys" / "verify.key"
IMAGES_INPUTS_PATH = BASE_DIR / "images" / "inputs"
IMAGES_OUTPUTS_PATH = BASE_DIR / "images" / "outputs"
BENCHMARK_OUTPUTS_PATH = BASE_DIR / "benchmarks"

SIGNING_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)

IMAGES_INPUTS_PATH.mkdir(parents=True, exist_ok=True)
IMAGES_OUTPUTS_PATH.mkdir(parents=True, exist_ok=True)
BENCHMARK_OUTPUTS_PATH.mkdir(parents=True, exist_ok=True)

IMG_EXTS = {".png"}