# AGENTS.md

Project: GitHub Actions-only. No local dev.

Key files:
- `.github/workflows/download.yaml` - main workflow
- `README.md` - user docs

Test changes: fork → edit workflow → push → check Actions tab.

Test download: edit any file on GitHub web, commit msg: `download: <URL>` or `download-zip: <URL>`.

Notes:
- Needs "Read and write" workflow permissions in Settings → Actions → General
- Output: `downloads/` folder
- Uses `[skip ci]` to avoid infinite loops
