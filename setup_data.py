"""
Script to download and setup data for the Spotify Recommender System

This script tries to obtain the required CSV files in `data/` by:
  1) Using `kagglehub` if available (Kaggle download), or
  2) Falling back to the repository helper which pulls Git LFS files.

If neither method succeeds it prints manual instructions and exits
with a non-zero code so automated deploys fail clearly.
"""
from pathlib import Path
import shutil
import sys

DATA_DIR = Path(__file__).parent / "data"
REQUIRED = ["Music Info.csv", "User Listening History.csv"]


def has_files():
    return all((DATA_DIR / f).exists() for f in REQUIRED)


def try_kagglehub():
    try:
        import kagglehub
    except Exception:
        return False

    try:
        print("Downloading dataset from Kaggle via kagglehub...")
        dataset_path = kagglehub.dataset_download('undefinenull/million-song-dataset-spotify-lastfm')
        src = Path(dataset_path)
        for f in REQUIRED:
            s = src / f
            d = DATA_DIR / f
            if s.exists():
                shutil.copy2(s, d)
                print(f"[OK] copied {f} from kagglehub download")
            else:
                print(f"[WARN] {f} not found in kagglehub download")
        return has_files()
    except Exception as e:
        print(f"[ERROR] kagglehub failed: {e}")
        return False


def try_lfs_helper():
    try:
        from download_lfs_files import download_lfs_files
    except Exception as e:
        print(f"[ERROR] download_lfs_files import failed: {e}")
        return False

    try:
        print("Attempting to pull Git LFS files using download_lfs_files()...")
        download_lfs_files()
        return has_files()
    except Exception as e:
        print(f"[ERROR] download_lfs_files failed: {e}")
        return False


def main():
    DATA_DIR.mkdir(exist_ok=True)

    if has_files():
        print("✅ Data files already present in data/")
        return

    if try_kagglehub():
        print("✅ Downloaded required files via kagglehub")
        return

    if try_lfs_helper():
        print("✅ Pulled required files via Git LFS helper")
        return

    print("\n[ERROR] Could not obtain required data files.")
    print("Options:")
    print("  1) Install kagglehub and set up Kaggle credentials, then run setup_data.py")
    print("     pip install kagglehub")
    print("  2) Ensure Git LFS is installed and the repo LFS objects are accessible, then run 'git lfs pull'")
    print("  3) Manually place the following files into the 'data' folder:")
    for f in REQUIRED:
        print(f"     - {f}")
    sys.exit(2)


if __name__ == '__main__':
    main()
