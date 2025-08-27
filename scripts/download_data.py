#!/usr/bin/env python3
import argparse, os, sys, pathlib, csv, hashlib, re

RAW_DIR = pathlib.Path("data/raw")
PROC_DIR = pathlib.Path("data/processed")
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)

# Try to use gdown (handles big Google Drive files & confirmation)
try:
    import gdown
    HAVE_GDOWN = True
except Exception:
    HAVE_GDOWN = False

_DRIVE_PATTERNS = [
    re.compile(r"https?://drive\.google\.com/file/d/([^/]+)/view"),         # /file/d/<ID>/view
    re.compile(r"https?://drive\.google\.com/open\?id=([^&]+)"),            # open?id=<ID>
    re.compile(r"https?://drive\.google\.com/uc\?export=download&id=([^&]+)") # already direct
]

def extract_drive_id(url: str):
    for pat in _DRIVE_PATTERNS:
        m = pat.search(url)
        if m:
            return m.group(1)
    return None

def sha256sum(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def download_drive(url: str, out_path: pathlib.Path):
    file_id = extract_drive_id(url)
    if not file_id:
        # Not a Drive link; tell the user to give a Drive link or add non-Drive logic
        raise ValueError(f"Not a recognized Google Drive link: {url}")
    if not HAVE_GDOWN:
        raise RuntimeError("gdown not installed. Run: pip install gdown")

    # gdown can use either id=... or full URL
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"[+] Downloading (gdown) id={file_id} -> {out_path}")
    gdown.download(id=file_id, output=str(out_path), quiet=False)
    print(f"[✓] Saved {out_path} ({out_path.stat().st_size/1e6:.2f} MB)")
    return out_path

def write_sample(src: pathlib.Path, dst: pathlib.Path, n: int = 5000):
    try:
        print(f"[+] Writing sample of {n} rows -> {dst}")
        with src.open("r", newline="", encoding="utf-8", errors="ignore") as fin, \
             dst.open("w", newline="", encoding="utf-8") as fout:
            reader = csv.reader(fin)
            writer = csv.writer(fout)
            for i, row in enumerate(reader):
                writer.writerow(row)
                if i >= n: break
        print("[✓] Sample written")
    except Exception as e:
        print(f"[!] Could not create sample: {e}")

def main():
    ap = argparse.ArgumentParser(description="Download large Google/Apple datasets from Google Drive.")
    ap.add_argument("--google-url", default=os.environ.get("GOOGLE_DATA_URL", ""),
                    help="Google Play dataset (Google Drive share link)")
    ap.add_argument("--apple-url",  default=os.environ.get("APPLE_DATA_URL", ""),
                    help="Apple App Store dataset (Google Drive share link)")
    ap.add_argument("--sample-rows", type=int, default=5000, help="Rows for sample CSVs in data/processed/")
    args = ap.parse_args()

    if not args.google_url and not args.apple_url:
        print("Provide at least one URL via --google-url/--apple-url or env GOOGLE_DATA_URL/APPLE_DATA_URL", file=sys.stderr)
        sys.exit(2)

    if args.google_url:
        g_path = download_drive(args.google_url, RAW_DIR / "google_play.csv")
        print(f"[✓] SHA256 google_play: {sha256sum(g_path)}")
        write_sample(g_path, PROC_DIR / "google_play.sample.csv", args.sample_rows)

    if args.apple_url:
        a_path = download_drive(args.apple_url, RAW_DIR / "apple_store.csv")
        print(f"[✓] SHA256 apple_store: {sha256sum(a_path)}")
        write_sample(a_path, PROC_DIR / "apple_store.sample.csv", args.sample_rows)

    print("\nDone. Update data/README.md with the SHA256 sums above.")

if __name__ == "__main__":
    main()
