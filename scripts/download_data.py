#!/usr/bin/env python3

import argparse, os, sys, urllib.request, hashlib, pathlib, csv, gzip, zipfile

RAW_DIR = pathlib.Path("data/raw")
PROC_DIR = pathlib.Path("data/processed")
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)

def sha256sum(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def smart_download(url: str, out_path: pathlib.Path):
    print(f"[+] Downloading {url} -> {out_path}")
    urllib.request.urlretrieve(url, out_path)
    print(f"[✓] Saved {out_path} ({out_path.stat().st_size/1e6:.2f} MB)")
    # auto-extract simple archives
    if out_path.suffix.lower() == ".gz":
        dst = out_path.with_suffix("")  # remove .gz
        print(f"[+] Extracting gzip -> {dst.name}")
        with gzip.open(out_path, "rb") as src, open(dst, "wb") as dstf:
            dstf.write(src.read())
        print("[✓] Extracted")
        return dst
    if out_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(out_path, "r") as z:
            # try to auto-pick first CSV
            csv_members = [m for m in z.namelist() if m.lower().endswith(".csv")]
            target = csv_members[0] if csv_members else z.namelist()[0]
            print(f"[+] Extracting {target}")
            z.extract(target, RAW_DIR)
            extracted = RAW_DIR / target
            print("[✓] Extracted")
            return extracted
    return out_path

def write_sample(src: pathlib.Path, dst: pathlib.Path, n: int = 5000):
    try:
        print(f"[+] Writing sample of {n} rows -> {dst}")
        with src.open("r", newline="", encoding="utf-8", errors="ignore") as fin,             dst.open("w", newline="", encoding="utf-8") as fout:
            reader = csv.reader(fin)
            writer = csv.writer(fout)
            for i, row in enumerate(reader):
                writer.writerow(row)
                if i >= n: break
        print("[✓] Sample written")
    except Exception as e:
        print(f"[!] Could not create sample: {e}")

def main():
    parser = argparse.ArgumentParser(description="Download Google/Apple app datasets into data/raw/.")
    parser.add_argument("--google-url", default=os.environ.get("GOOGLE_DATA_URL", ""),
                        help="URL to Google Play dataset (CSV/ZIP/GZ)")
    parser.add_argument("--apple-url",  default=os.environ.get("APPLE_DATA_URL", ""),
                        help="URL to Apple App Store dataset (CSV/ZIP/GZ)")
    parser.add_argument("--sample-rows", type=int, default=5000, help="Rows for sample CSVs in data/processed/")
    args = parser.parse_args()

    if not args.google_url and not args.apple_url:
        print("Provide at least one URL via --google-url/--apple-url or env GOOGLE_DATA_URL/APPLE_DATA_URL", file=sys.stderr)
        sys.exit(2)

    if args.google_url:
        g_path = smart_download(args.google_url, RAW_DIR / "google_play.csv" )
        print(f"[✓] SHA256 google_play: {sha256sum(g_path)}")
        write_sample(g_path, PROC_DIR / "google_play.sample.csv", args.sample_rows)

    if args.apple_url:
        a_path = smart_download(args.apple_url, RAW_DIR / "apple_store.csv" )
        print(f"[✓] SHA256 apple_store: {sha256sum(a_path)}")
        write_sample(a_path, PROC_DIR / "apple_store.sample.csv", args.sample_rows)

    print("\nDone. Update data/README.md with the SHA256 sums above.")
if __name__ == "__main__":
    main()
