# Deploying to Streamlit Community Cloud

Follow these steps to deploy this project to Streamlit Community Cloud (share.streamlit.io).

1) Push this repository to GitHub (if not already):

```bash
git init
git add .
git commit -m "ready for streamlit deploy"
git branch -M main
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```

2) Ensure large data files are available to Streamlit Cloud

- Recommended: use Git LFS to store large files. This repo includes a `.gitattributes` that tracks `data/*.npz`, `data/*.npy`, and `data/*.csv` with LFS.

Install LFS and push LFS objects:

```bash
git lfs install
git add .gitattributes
git add data/*.npz data/*.npy data/*.csv
git commit -m "track data with LFS"
git push
```

If you prefer not to use LFS, host the dataset externally (S3, Google Drive) and update `setup_data.py` to download from that URL.

3) Make sure `requirements.txt` lists all Python dependencies (present in repo).

4) Deploy on Streamlit Cloud

- Go to https://share.streamlit.io and sign in with GitHub.
- Click 'New app', select your repository, branch `main`, and set `app.py` as the entrypoint.
- Click 'Deploy'. Streamlit will install dependencies and run the app.

5) Troubleshooting

- If the build fails due to missing data files, update `setup_data.py` to download or pull LFS objects. The repo contains `download_lfs_files.py` to help pull LFS objects on cloud startup; `setup_data.py` now attempts to use either `kagglehub` or this helper.
- Check app logs in Streamlit deploy details for errors and fix missing packages or file paths.

If you'd like, I can prepare a single commit with these changes and give you the exact git commands to push. After you push, I can help monitor and debug the cloud build logs.
