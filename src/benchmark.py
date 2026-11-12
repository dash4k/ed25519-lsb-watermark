from datetime import datetime
import os
import cv2
import numpy as np
import pandas as pd
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from config import IMAGES_INPUTS_PATH, IMAGES_OUTPUTS_PATH, BENCHMARK_OUTPUTS_PATH

COVER_DIR = IMAGES_INPUTS_PATH
STEGO_DIR = IMAGES_OUTPUTS_PATH
OUTPUT_CSV = BENCHMARK_OUTPUTS_PATH / f"results_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv"
VALID_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".pgm")


def evaluate(cover_dir, stego_dir):
    results = []

    for filename in sorted(os.listdir(stego_dir)):
        if not filename.lower().endswith(VALID_EXT):
            continue

        stego_path = os.path.join(stego_dir, filename)
        cover_path = os.path.join(cover_dir, filename)

        if not os.path.exists(cover_path):
            print(f"[SKIP] No matching cover image for {filename}")
            continue

        cover = cv2.imread(cover_path, cv2.IMREAD_UNCHANGED)
        stego = cv2.imread(stego_path, cv2.IMREAD_UNCHANGED)

        if cover is None or stego is None:
            print(f"[SKIP] Could not read {filename}")
            continue

        if cover.shape != stego.shape:
            print(f"[SKIP] Shape mismatch for {filename}: {cover.shape} vs {stego.shape}")
            continue

        data_range = 255 if cover.dtype == np.uint8 else 65535

        p = psnr(cover, stego, data_range=data_range)

        if cover.ndim == 3:
            s = ssim(cover, stego, data_range=data_range, channel_axis=2)
        else:
            s = ssim(cover, stego, data_range=data_range)

        results.append({"filename": filename, "PSNR (dB)": p, "SSIM": s})
        print(f"{filename}: PSNR = {p:.4f} dB, SSIM = {s:.6f}")

    return pd.DataFrame(results)


if __name__ == "__main__":
    df = evaluate(COVER_DIR, STEGO_DIR)

    if df.empty:
        print("No image pairs were evaluated.")
    else:
        print("\n--- Average ---")
        print(f"PSNR: {df['PSNR (dB)'].replace(np.inf, np.nan).mean():.4f} dB")
        print(f"SSIM: {df['SSIM'].mean():.6f}")
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"\nSaved results to {OUTPUT_CSV}")