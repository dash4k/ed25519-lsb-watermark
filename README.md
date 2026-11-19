# ed25519 X LSB Image Watermarking

A Python proof of concept that signs PNG images with Ed25519 and embeds each 64-byte signature in the least significant bits (LSBs) of the image’s RGB channels. The signature can later be checked against the image using the corresponding public key.

## How it works

The signing process loads an image as RGBA, clears the LSBs of its RGB channels, and signs a payload containing a format marker, the image dimensions, and the pixel data. It embeds the resulting 512 signature bits in the first 512 RGB channel values and saves the result as a PNG.

Verification extracts those bits, clears the RGB LSBs, and checks the signature with the public key. Changes to the image’s pixel values or dimensions can invalidate the signature. This is a demonstration project, not a robust watermarking system: transformations such as resizing or lossy recompression are likely to break verification.

The repository also includes scripts for comparing image quality with PSNR and SSIM, and for calculating confusion-matrix counts from labeled images.

## Requirements

- Python 3.12 or later
- GNU Make
- The `py` Python launcher used by the Makefile, or a Makefile updated to use your Python command

Install the dependencies from the repository root:

```bash
pip install -r requirements.txt
```

## Local usage

Run these commands from the repository root.

### 1. Set up directories

```bash
make config
```

This creates the input, output, labeled-image, key, and benchmark directories.

### 2. Generate a keypair

```bash
make key
```

This generates:

- `keys/signing.key`: the private signing key
- `keys/verify.key`: the public verification key

Keep the signing key private. The verification key is used by the local verifier and HTTP API. Generating a new keypair means images signed with a previous keypair will no longer verify with the new public key.

### 3. Add PNG images

Place images to sign in:

```text
images/inputs/
```

### 4. Sign images

```bash
make sign
```

The script processes PNG files in `images/inputs` and saves signed PNGs in `images/outputs`. It also creates labeled copies in `images/labeled`: `true_` copies of signed images and `false_` copies of the original images.

Images must have enough RGB channel values to hold the 512 signature bits.

### 5. Verify signed images

```bash
make verify
```

The verifier checks PNG files in `images/outputs` and reports valid, invalid, and failed checks.

### 6. Run the image-quality benchmark

```bash
make benchmark
```

The benchmark compares matching images in `images/inputs` and `images/outputs`. It reports average PSNR and SSIM and saves per-image results to a timestamped CSV in `benchmarks/quality/`.

The benchmark recognizes PNG, JPEG, BMP, TIFF, and PGM files, but the signing and verification scripts process PNG files only.

### 7. Generate confusion-matrix results

```bash
make confusion-matrix
```

The script is intended to verify labeled images in `images/labeled` and save TP, FP, TN, and FN counts to a timestamped CSV in `benchmarks/cms/`.

## HTTP verification API

The FastAPI app verifies an uploaded image using `keys/verify.key`. Generate a keypair first, then start the server:

```bash
make key
make server
```

The server listens on `http://127.0.0.1:8000`. Send the image bytes as the request body to `POST /verify`:

```bash
curl -X POST \
  --data-binary @images/outputs/example.png \
  http://127.0.0.1:8000/verify
```

A successful request returns a JSON boolean:

```json
{"result": true}
```

The endpoint expects the image itself in the request body, not a JSON or multipart upload. It verifies the image; it does not save or sign uploaded images.

## Make targets

| Target | Description |
| --- | --- |
| `make config` | Create the required directories |
| `make key` | Generate a signing and verification keypair |
| `make sign` | Sign input PNGs, save signed images, and create labeled copies |
| `make verify` | Verify signed PNGs in the output directory |
| `make benchmark` | Compare matching images and write PSNR/SSIM results |
| `make confusion-matrix` | Run the labeled-image confusion-matrix script |
| `make server` | Start the HTTP verification API on port 8000 |
| `make clean` | Remove output and labeled image directories and generated keys |
| `make clean-outputs` | Remove output and labeled image directories |
| `make clean-keys` | Remove generated keys |
| `make clean-benchmarks` | Remove benchmark output files |
| `make all` | Clean, configure, generate keys, sign, verify, benchmark, and run the confusion-matrix script |

**Warning:** `make all` starts with `make clean`, which deletes `images/outputs`, `images/labeled`, and `keys/`, then generates a new keypair. Previously signed images will not verify with the newly generated key.

## Limitations

- Local signing and verification process PNG files only.
- Image transformations that change pixel values or dimensions can invalidate a signature.
- The LSB payload is not resilient to image editing, resizing, or lossy recompression.
- This is a proof of concept, not a complete image-authentication or watermarking product.