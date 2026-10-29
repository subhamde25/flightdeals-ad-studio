# Your First Commit: Step by Step

Your GitHub repo **https://github.com/subhamde25/flightdeals-ad-studio** already exists. It's public and holds one commit: the "Initial commit" with a short README that GitHub created for you. This guide puts the whole project on top of that commit.

Every grey block is a command you copy into **Git Bash** or **PowerShell** and press Enter.

---

## 1. How Git works

| Term | What it means here |
|---|---|
| **Repository (repo)** | This project folder plus a hidden `.git` folder where Git keeps the full history. |
| **Working folder** | The files you see and edit. |
| **Staging (`git add`)** | Choosing which changes go into the next snapshot. |
| **Commit (`git commit`)** | A saved snapshot with a message. You can always go back to it. |
| **Branch (`main`)** | A line of commits. You'll work on `main`. |
| **Remote (`origin`)** | The copy of the repo on GitHub. |
| **Fetch / Push** | Fetch downloads GitHub's commits to your PC; push uploads yours to GitHub. |
| **`.gitignore`** | Files Git must never upload (renders, `node_modules`). Already set up. |
| **Git LFS** | Large File Storage. Big files (our ~50 MB MP4s) are stored separately and the repo keeps a small pointer. Already set up in `.gitattributes`. |

The flow is: **edit files → `git add` → `git commit` → `git push`**.

---

## 2. What gets uploaded

| Goes into Git | Size | How |
|---|---|---|
| Code: `*.html`, `*.js`, `*.mjs`, `*.py`, `*.sh`, `*.json`, `*.md` | ~0.3 MB | normal Git (text) |
| Assets: fonts `.woff2`, images `.jpg/.png`, voice `.mp3/.wav` | ~15 MB | normal Git (binary, all well under 50 MB) |
| Final ads: `deliverables/*.mp4` (≈53 MB each) | ~106 MB | **Git LFS** |

| Stays on your PC only | Why |
|---|---|
| `node_modules/` | Reinstalled with `npm install`. |
| `build/` | Renders, mixes, stems and logs. Rebuilt with `npm run audio` and `npm run render`. |
| `_stills/`, `*.log`, decode caches | Temporary QA files. |

GitHub's limits are a warning above **50 MB** and a hard block above **100 MB** per file. That's why the MP4s use LFS.

---

## 3. One-time setup (only the first time you use Git on this PC)

Tell Git who you are. The email below is the private **no-reply address GitHub already used for your "Initial commit"**, so your real email stays hidden and GitHub won't block the push:

```bash
git config --global user.name "subhamde25"
```

```bash
git config --global user.email "139131879+subhamde25@users.noreply.github.com"
```

Turn on Git LFS:

```bash
git lfs install
```

---

## 4. Open a terminal in the project folder

The project lives in **`C:\Users\deysu\flightdeals-ad-studio`**. It sits outside OneDrive on purpose, because OneDrive sync can corrupt the hidden `.git` folder. Then use one of these:

- **Easiest:** in File Explorer, right-click inside the folder → *Show more options* → **Open Git Bash here**.
- **Or** open PowerShell or Git Bash and `cd` into it:

```bash
cd "C:\Users\deysu\flightdeals-ad-studio"
```

---

## 5. Create the local repository

```bash
git init -b main
```

This creates the hidden `.git` folder and a branch called `main`.

---

## 6. Connect to your GitHub repo and pick up its "Initial commit"

Link this folder to GitHub:

```bash
git remote add origin https://github.com/subhamde25/flightdeals-ad-studio.git
```

Download GitHub's history (just the one "Initial commit"):

```bash
git fetch origin
```

Make your local `main` start from that commit. **Your files are not touched.** This only tells Git where your history begins:

```bash
git reset origin/main
```

Without this step the push would be rejected, because GitHub already has a commit your PC doesn't know about.

---

## 7. Stage everything and check it

```bash
git add .
```

```bash
git status
```

You should see about **50 files**. `README.md` shows as **modified**, because the full project README replaces GitHub's short one (its description line is kept). Everything else shows as **new file**. Check two things:

- ❌ **No** `node_modules/` or `build/` in the list.
- ✅ `deliverables/FlightDeals_9x16_Reels.mp4` and `deliverables/FlightDeals_16x9_YouTube.mp4` **are** in the list.

You may see warnings like *"CRLF will be replaced by LF"*. These are normal on Windows and safe to ignore.

---

## 8. Make your commit

```bash
git commit -m "Add FlightDeals Ad Studio: pipeline, assets and final 9:16 + 16:9 ads"
```

Confirm the two videos went to LFS. You should see both MP4 names:

```bash
git lfs ls-files
```

Look at your history. You should see your new commit on top of `Initial commit`:

```bash
git log --oneline
```

---

## 9. Push to GitHub

```bash
git push -u origin main
```

- The first time, a **browser window opens asking you to sign in to GitHub**. Approve it. This is Git Credential Manager, which comes with Git for Windows.
- The upload takes a minute: about 15 MB of normal Git plus about 106 MB of LFS videos.
- This is a normal push. No `--force` needed.

---

## 10. Check on GitHub

Open https://github.com/subhamde25/flightdeals-ad-studio and refresh. You should see the full README with the pipeline diagram and **2 commits**. Click `deliverables/FlightDeals_9x16_Reels.mp4`: it should say **"Stored with Git LFS"** and offer a download. 🎉

---

## Everyday workflow (after the first push)

```bash
git status
```

```bash
git add .
```

```bash
git commit -m "Describe what you changed"
```

```bash
git push
```

Other handy commands: `git log --oneline` shows history, `git diff` shows unstaged changes, and `git pull` gets changes made on GitHub.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `! [rejected] main -> main (fetch first)` | Step 6 was skipped. Run `git fetch origin`, then `git reset --soft origin/main`, then `git commit -m "Add FlightDeals Ad Studio"`, then `git push -u origin main`. |
| `remote origin already exists` | `git remote set-url origin https://github.com/subhamde25/flightdeals-ad-studio.git` |
| `remote: GH007: Your push would publish a private email address` | Re-run the `user.email` command from step 3, then `git commit --amend --reset-author --no-edit` and push again. |
| `File ... exceeds GitHub's file size limit of 100 MB` | A large file slipped past LFS. Check `.gitattributes` has the `*.mp4` LFS line and run `git lfs install`. Add the file again with `git rm --cached <file>`, then `git add <file>`, then commit. |
| `detected dubious ownership in repository` | Run the `git config --global --add safe.directory ...` command that Git prints in the message. |
| Videos show as a tiny "version https://git-lfs…" text file after cloning elsewhere | Run `git lfs install`, then `git lfs pull` in that clone. |

---

## Starting a brand-new project later?

Create the GitHub repo **without** ticking "Add a README". Then you can skip `git fetch` and `git reset` (step 6) and just run `git remote add origin …` followed by `git push -u origin main` after your first commit.
