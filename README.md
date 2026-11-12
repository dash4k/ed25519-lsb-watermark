# ed25519 X LSB Image Watermarking

A Python proof of concept that signs PNG image data with Ed25519 and embeds the 64-byte signature in the least significant bits (LSBs) of the image’s RGB channels. Signatures can be checked locally or through a small HTTP API.

## How it works

The tool loads each image as RGBA, clears the LSBs of its RGB channels, and signs a payload containing the image dimensions and pixel data. It embeds the resulting 64-byte signature in the first 512 RGB channel bits and saves the result as PNG.

Verification extracts those bits and checks the signature against the image data using the Ed25519 public key. Changing the image’s pixel values or dimensions can invalidate the signature.

The benchmark process compares the images in inputs/ and outputs/ to calculate both PSNR and SSIM values.

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

This creates the image input/output directories and the `keys` directory.

### 2. Generate a keypair

```bash
make key
```

This generates:

- `keys/signing.key`: the private signing key
- `keys/verify.key`: the public verification key

Keep the signing key private and secure. The verification key is used by both the local verifier and HTTP server.

### 3. Add PNG images

Place images to sign in:

```text
images/inputs/
```

Images must have at least 512 RGB channel values available for the embedded signature.

### 4. Sign images

```bash
make sign
```

The script processes PNG files in `images/inputs` and saves signed images to `images/outputs`.

### 5. Verify signed images

```bash
make verify
```

The verifier checks PNG files in `images/outputs` and reports counts of valid, invalid, and failed checks.

### 6. The benchmark

```bash
make benchmark
```

The benchmarking script compares the PNG files in images/inputs and images/outputs and writes the PSNR and SSIM values for each image to a .csv file.

## HTTP verification API

The repository includes a FastAPI app that verifies an uploaded image’s raw bytes using `keys/verify.key`. Generate the keypair first, then start the server:

```bash
make key
py -m uvicorn server:app --reload
```

The app listens on `http://127.0.0.1:8000` by default. Send the image bytes as the request body to `POST /verify`:

```bash
curl -X POST \
  --data-binary @images/outputs/example.png \
  http://127.0.0.1:8000/verify
```

The response contains a boolean verification result:

```json
{"result": true}
```

The API expects the image itself in the request body, not a JSON or multipart upload.

## Make targets

| Target | Description |
| --- | --- |
| `make config` | Create the required directories |
| `make key` | Generate a new signing and verification keypair |
| `make sign` | Sign input PNGs and write results to the output directory |
| `make verify` | Verify signed PNGs in the output directory |
| `make benchmark` | Calculates PSNR and SSIM values of each stego media |
| `make clean` | Remove the output directory and generated keys |
| `make all` | Clean, configure, generate keys, sign, and verify |

**Warning:** `make all` starts by running `make clean`, which deletes `images/outputs` and `keys/`, then generates a new keypair. Previously signed images will not verify against the new keypair.

## Notes

- Only PNG files are processed by the local signing and verification scripts.
- The HTTP endpoint verifies image bytes; it does not save or sign uploaded images.
- Image transformations that change pixel values or dimensions can invalidate the signature.
- This is a demonstration project, not a complete image-authentication or watermarking product.