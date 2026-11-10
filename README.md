# ed25519 X LSB Image Watermarking 

A Python proof of concept that embeds an Ed25519 signature in the least significant bits (LSBs) of a PNG image’s RGB channels, then verifies that signature later.

## How it works

The project clears the RGB LSBs before signing the image data. It embeds the resulting 64-byte Ed25519 signature into the first 512 RGB channel bits. Verification extracts the signature and checks it against the image data using the public verification key.

## Requirements

- Python
- GNU Make
- The `py` Python launcher used by the Makefile (or adjust the Makefile to use your Python command)

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run these commands from the repository root.

### 1. Set up directories

```bash
make config
```

This creates the `images/inputs`, `images/outputs`, and `keys` directories.

### 2. Generate a keypair

```bash
make key
```

This creates:

- `keys/signing.key`: the private signing key
- `keys/verify.key`: the public verification key

Keep the signing key private and secure.

### 3. Add PNG images

Place the images you want to sign in:

```text
images/inputs/
```

Images must have at least 512 RGB channel values available for the embedded signature.

### 4. Sign and embed

```bash
make sign
```

The script processes PNG files in `images/inputs` and saves signed images to `images/outputs`.

### 5. Verify

```bash
make verify
```

The verifier checks PNG files in `images/outputs` and reports the number of valid, invalid, and failed checks.

## Make targets

| Target | Description |
| --- | --- |
| `make config` | Create the required directories |
| `make key` | Generate a new signing and verification keypair |
| `make sign` | Sign input PNGs and write results to the output directory |
| `make verify` | Verify signed PNGs in the output directory |
| `make clean` | Remove the output directory and generated keys |
| `make all` | Clean, configure, generate keys, sign, and verify |

**Warning:** `make all` starts by running `make clean`, which deletes `images/outputs` and `keys/`. It then creates a new keypair. Previously signed images will no longer verify with the newly generated verification key.

## Notes

- Only PNG files are processed.
- Signing modifies RGB channel LSBs; the output is saved as PNG.
- Image transformations that change pixel values or dimensions can invalidate the signature.
- This is a demonstration project, not a complete image-authentication or watermarking product.