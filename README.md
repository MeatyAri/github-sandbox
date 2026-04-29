# github-sandbox

# 📥 Download Anything via Commit Message

**For people in countries with limited or throttled internet.**

Your ISP blocks YouTube? Slow downloads? GitHub is usually open. Use GitHub's servers as a proxy and download at full speed anywhere in the world.

No terminal. No CLI. Just a commit message → files land in `downloads/`.

---

## ✨ Features

- **YouTube**: videos, music, age-restricted, members-only (cookies required)
- **Ollama models**: download LLMs directly from ollama.com library
- **Apple Podcasts** + Rumble + Odysee + BitChute + Bandcamp + Pexels
- **Bunkr**: automatic extraction
- **Twitch** + **Reddit** + **SoundCloud**: with cookies
- **Any URL**: publicly accessible link
- **Large files 5GB+**: infinite scaling across multiple repos
- **Split archives**: download-zip bundles everything into timestamped tar.gz

**Streaming sites not working?** Report issues, we'll investigate, DRM protected music such as Spotify, Apple Music won't work.

---

## ⚡ Quick Start

```bash
git commit --allow-empty -m "download: https://example.com/file.zip" && git push
```

Files → `downloads/` folder.

---

## 🛠️ Setup

### 1. Fork repo

### 2. Enable workflow permissions

1. **Settings** → **Actions** → **General**
2. **Workflow permissions** → **Read and write**
3. **Save**

### 3. Add GitHub token (required only for files > 4.5GB)

1. Create **GitHub Fine-grained** token:
   - Go to **Settings** → **Developer settings** → **Personal access tokens** → **Fine-grained tokens**
   - **Generate new token** → select **All Repositories** and set a name → copy token
2. **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret**
4. Name: `CROSS_REPO_PAT`
5. Paste token → **Add secret**

### 4. Pre-create large file repos (only if downloading > 4.5GB)

Each `large-files-part-*` repo = 4.5GB capacity.

Example: 10GB file → create `large-files-part-1`, `large-files-part-2`, `large-files-part-3`.

1. Create new repo on GitHub: `large-files-part-1`
2. Repeat for each additional repo needed

---

## 🍪 Streaming Site Cookies (Optional)

Required for age-restricted / member-only / private content / bot errors.

**Supported:** YouTube, Twitch, Reddit, SoundCloud.

### Get cookies

1. Install **"Get cookies.txt LOCALLY"** extension (Chrome)
2. Enable **Allow in incognito**
3. Open **Incognito window** → log into site
4. Visit `https://[site].com/robots.txt`
5. Right-click extension → **Export** → save as `[site]_cookies.txt`

### Add to GitHub Secrets

| Site | Secret Name |
|------|-------------|
| YouTube | `YOUTUBE_COOKIES` |
| Twitch | `TWITCH_COOKIES` |
| Reddit | `REDDIT_COOKIES` |
| SoundCloud | `SOUNDCLOUD_COOKIES` |

Copy file contents → paste as secret value.

**Refresh frequently** — sites rotate cookies every 3-5 days.

---

## 📋 Commands

### Download files individually

```
download: URL
```

```
download: https://example.com/file.zip
```

### Download + archive into single tar.gz

```
download-zip: URL
```

```
download-zip: https://example.com/a.zip https://example.com/b.pdf
```

Output: `archive_YYYYMMDD_HHMMSS.tar.gz`

### Download Ollama model

```
ollama: gemma4:e4b
```

```
ollama: qwen3.6:35b
```

Downloads all model shards and manifest file automatically.

---

## 📂 Large Files 5GB+

Downloads > 4.5GB auto-split into 90MB parts → pushed to `large-files-part-*` repos.

**Infinite scaling** — create more repos as needed.

**Flow:**
1. Pre-create `large-files-part-1`, `large-files-part-2`, etc. (each = 4.5GB)
2. Add `CROSS_REPO_PAT` secret to each new repo
3. Trigger download
4. Workflow splits → distributes → pushes to repos
5. **Reassemble locally:**

```bash
# Linux/macOS
cat large-files-part-1/*.part_* > original_filename.tar.gz

# Windows - join split files
REM Option 1: copy
copy /b large-files-part-1\*.part_* combined_filename.tar.gz

REM Option 2: 7zip (command line)
7z x large-files-part-1\*.part_* -ofile.tar.gz

REM Option 3: 7zip (GUI)
1. Put all of the downloaded parts in one folder
2. Select the first part_* file in folder
3. Right-click → 7-Zip → Combine Files
4. Save as combined_filename.tar.gz
```

### Extract tar.gz

```bash
# Linux/macOS
tar -xzf archive_YYYYMMDD_HHMMSS.tar.gz

# Or specify destination
tar -xzf archive_YYYYMMDD_HHMMSS.tar.gz -C /path/to/folder
```

### Windows - extract tar.gz

**GUI:**
1. Right-click `archive.tar.gz`
2. 7-Zip → Extract Here

**Command line:**
```cmd
7z x file.tar.gz

REM Or to folder
7z x file.tar.gz -ofolder
```

---

## ✅ Result

| Command | Output |
|---------|--------|
| `download:` | Files in `downloads/` with original names |
| `download-zip:` | Single `archive_YYYYMMDD_HHMMSS.tar.gz` in `downloads/` |
| `ollama:` | Model shards in `downloads/` |

Check **Actions** tab for progress → **Code** tab → `downloads/` for files.

---

## ⚠️ Notes

- Separate multiple URLs with spaces
- Commit message contains `[skip ci]` → workflow skips itself
- No valid command found → workflow exits silently
- Spotify + Apple Music = blocked (DRM)
