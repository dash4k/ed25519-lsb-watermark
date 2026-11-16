# ed25519 X LSB Image Watermarking

A Python proof of concept that signs PNG images with Ed25519 and embeds the 64-byte signature in the least significant bits (LSBs) of the image’s RGB channels. The signature can be verified locally or through a small HTTP API.

## How it works

The tool loads each image as RGBA, clears the LSBs of its RGB channels, and signs a payload containing the image dimensions and pixel data. It embeds the signature in the first 512 RGB channel values.

Verification extracts the embedded signature and checks it against the image data using the Ed25519 public key. Changes to the image’s pixel values or dimensions can invalidate the signature. Images must have at least 512 RGB channel values available for the signature.

The repository also includes:
- A benchmark that compares input and signed images using PSNR and SSIM.
- A confusion-matrix script that verifies labeled images and records true-positive, false-positive, true-negative, and false-negative counts.

## Requirements

- Python
- GNU Make
- The `py` Python launcher used by the Makefile, or update the Makefile to use your Python command

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Local usage

Run these commands from the repository root.

### 1. Set up directories

```bash
make config
```

This creates the image directories (`images/inputs`, `images/outputs`, and `images/labeled`), key directory, and benchmark output directories.

### 2. Generate a keypair

```bash
make key
```

This generates:

- `keys/signing.key`: the private signing key
- `keys/verify.key`: the public verification key

Keep the signing key private and secure. The verification key is used by the local verifier and HTTP server.

### 3. Add PNG images

Place images to sign in:

```text
images/inputs/
```

### 4. Sign images

```bash
make sign
```

The script processes PNG files in `images/inputs` and saves signed images to `images/outputs`. It also creates labeled copies in `images/labeled`: a `true_` copy of each signed image and a `false_` copy of the original.

### 5. Verify signed images

```bash
make verify
```

The verifier checks PNG files in `images/outputs` and reports counts of valid, invalid, and failed checks.

### 6. Run the benchmark

```bash
make benchmark
```

The benchmark compares matching images in `images/inputs` and `images/outputs`, reports average PSNR and SSIM, and writes per-image results to a timestamped CSV in `benchmarks/quality/`. It supports PNG, JPEG, BMP, TIFF, and PGM files for the comparison.

### 7. Generate a confusion matrix

```bash
make confusion-matrix
```

The script verifies the labeled images in `images/labeled` and writes the TP, FP, TN, and FN counts to a timestamped CSV in `benchmarks/cms/`.

## HTTP verification API

The FastAPI app verifies an uploaded image’s bytes using `keys/verify.key`. Generate the keypair first, then start the server:

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

The response contains a boolean verification result:

```json
{"result": true}
```

The API expects the image itself in the request body, not a JSON or multipart upload. It verifies the image; it does not save or sign uploaded images.

## Make targets

| Target | Description |
| --- | --- |
| `make config` | Create the required directories |
| `make key` | Generate a new signing and verification keypair |
| `make sign` | Sign input PNGs, save signed images, and create labeled copies |
| `make verify` | Verify signed PNGs in the output directory |
| `make benchmark` | Compare matching images and write PSNR/SSIM results |
| `make confusion-matrix` | Verify labeled images and write TP/FP/TN/FN counts |
| `make server` | Start the HTTP verification API on port 8000 |
| `make clean` | Remove the output and labeled image directories and generated keys |
| `make clean-outputs` | Remove the output and labeled image directories |
| `make clean-keys` | Remove generated keys |
| `make clean-benchmarks` | Remove benchmark output files |
| `make all` | Clean, configure, generate keys, sign, verify, benchmark, and calculate the confusion matrix |

**Warning:** `make all` starts by running `make clean`, which deletes `images/outputs`, `images/labeled`, and `keys/`, then generates a new keypair. Previously signed images will not verify against the new keypair. Benchmark files are not removed by `make clean`; use `make clean-benchmarks` to remove them.

## Notes

- Local signing and verification process PNG files only.
- The benchmark supports additional formats for image comparison.
- Image transformations that change pixel values or dimensions can invalidate the signature.
- This is a demonstration project, not a complete image-authentication or watermarking product.