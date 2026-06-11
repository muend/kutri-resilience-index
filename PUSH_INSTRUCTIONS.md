# How to push KUTRI to GitHub

The repository history was built and committed inside the sandbox (branch
`publication-ready-kutri`, commit `f9a3b7c`) and delivered as a git **bundle**:
`kutri-publication-ready.bundle`. The sandbox filesystem could not host a live `.git`
directory, so a bundle is the clean handoff.

## Option A — clone from the bundle, then push (recommended)

```bash
# from the "Resilliance Index" folder
git clone kutri-publication-ready.bundle kutri-clean
cd kutri-clean
git remote add origin https://github.com/<your-username>/kutri.git
git push -u origin publication-ready-kutri
```

Then open a PR from `publication-ready-kutri` into `main` on GitHub, or merge locally:

```bash
git checkout main 2>/dev/null || git checkout -b main
git merge publication-ready-kutri
git push origin main
```

(No force push is needed or used.)

## Option B — if you already created an empty GitHub repo

Use the same clone-from-bundle step, then set `origin` to your repo URL and push.

## Note on the leftover kutri/.git folder

The sandbox left a broken, empty `.git` folder inside `kutri/`. Delete it on your
machine before using that folder directly (or just use the clean clone from Option A):

```bash
rmdir /s /q kutri\.git    # Windows
# or
rm -rf kutri/.git         # macOS/Linux
```

The bundle clone (Option A) is unaffected by this and is the simplest path.
