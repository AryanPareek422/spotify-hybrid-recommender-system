"""
Download Git LFS files on Streamlit Cloud startup
"""
import os
import subprocess
import sys

def download_lfs_files():
    """Download Git LFS files if they're pointer files"""
    data_files = [
        'data/Music Info.csv',
        'data/User Listening History.csv',
        'data/cleaned_data.csv',
        'data/collab_filtered_data.csv',
        'data/interaction_matrix.npz',
        'data/track_ids.npy',
        'data/transformed_data.npz',
        'data/transformed_hybrid_data.npz'
    ]
    
    # Check if any file is a Git LFS pointer (small size indicates pointer file)
    needs_download = False
    for file_path in data_files:
        if os.path.exists(file_path):
            # LFS pointer files are typically less than 200 bytes
            if os.path.getsize(file_path) < 200:
                needs_download = True
                break
    
    if needs_download:
        print("📥 Downloading Git LFS files...")
        try:
            # Install git-lfs if not present
            subprocess.run(['git', 'lfs', 'install'], check=True, capture_output=True)
            # Pull LFS files
            subprocess.run(['git', 'lfs', 'pull'], check=True, capture_output=True)
            print("✅ Git LFS files downloaded successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error downloading LFS files: {e}")
            print("Please check Streamlit Cloud logs for details")
            sys.exit(1)
    else:
        print("✅ All data files are already available")

if __name__ == "__main__":
    download_lfs_files()
