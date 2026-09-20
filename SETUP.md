# Setup for Neverfinished005 (about 5 minutes)

Your profile repo is `Neverfinished005/Neverfinished005`.

1. Open that repo on GitHub (create it as a *public* repo with that exact name if it doesn't exist).
2. Click **Add file → Upload files** and drag in the contents of this folder:
   `README.md`, `assets/`, `tools/`, `.github/`  (keep the folder structure).
   Choose "Commit directly to main". This replaces your old README.
   Note: the hidden `.github` folder can't always be drag-dropped from a browser. If it is skipped, use
   **Add file → Create new file**, type `.github/workflows/batmobile.yml` as the name, and paste the file's contents.
3. **Enable the Batmobile:** repo → Settings → Actions → General → Workflow permissions → *Read and write permissions* → Save.
   Then Actions tab → "Batmobile Patrol" → **Run workflow**. Wait for the green tick; this creates the `output` branch the snake image loads from.
4. Open `github.com/Neverfinished005` and hard-refresh (Ctrl+Shift+R). Done.

## Editing later
Change name, tagline, skills, rotating lines or footer text at the top of `tools/build.py`, then run:

    pip install fonttools
    python tools/build.py

and commit the regenerated `assets/` folder.

## Troubleshooting
- Stats card shows an error: the public Vercel instance is rate-limited. Refresh later, or self-host github-readme-stats on your own Vercel account.
- Snake image is broken: the workflow hasn't run yet (step 3).
- Header not animating in a preview: some editors don't run SVG animation. It plays on the real GitHub profile page.
