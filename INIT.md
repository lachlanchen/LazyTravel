# LazyTravel Resume Checklist

Use this project-local checklist when initializing or resuming work. It records
no private session history.

1. Read `AGENTS.md`, `PROJECT_GOAL.md`, and `PROJECT_MEMORY.md`.
2. Confirm the working directory is `/home/lachlan/ProjectsLFS/LazyTravel` and
   inspect `git status --short --branch`; preserve unrelated user changes.
3. Check shared-workstation RAM, swap, project-owned processes, tmux sessions,
   and ports before a heavy build. Never alter existing noVNC/Xvfb/x11vnc/
   websockify processes for this project or another project.
4. Run `python3 scripts/verify_sources.py`. External archives and visual
   references must remain at their hash-pinned read-only paths.
5. Continue only Lanzhou at `china/cities/lanzhou`. First establish its source
   ledger, travel-guide line, locked chapter spine, and canonical JSON shell.
   Do not reopen Xi'an or Hakone without a demonstrated failure.
6. Run focused tests while editing, then the full validation/build sequence:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_hakone_review.py --sync-nutstore
python3 scripts/build_series_website.py
python3 scripts/validate_site_parity.py \
  --book data/japan/prefectures/kanagawa/hakone/book.json \
  --site site/japan/prefectures/kanagawa/hakone
```

Serve `site` on one temporary unused project-owned port, run
`scripts/qa_destination_website.py` at desktop and mobile sizes, then terminate
only that exact temporary server. Leave the existing port `4173` server and all
noVNC/Xvfb/x11vnc/websockify processes untouched.

7. Review every new or changed B6 page and desktop/mobile screenshot. Record the
   review under `books/japan/prefectures/kanagawa/hakone/editorial/`.
8. Sync only the verified pocket PDF:

```bash
python3 scripts/build_hakone_review.py --sync-nutstore
```

Verify the Nutstore and `dist` SHA-256 values match.
9. Update the milestone in `README.md`, make one scoped commit, and push it to
   `origin/main`.

For a complete-book public website milestone, also run:

```bash
python3 scripts/verify_deployed_site.py \
  --url https://lachlanchen.github.io/LazyTravel/japan/prefectures/kanagawa/hakone/ \
  --book data/japan/prefectures/kanagawa/hakone/book.json
```

Current gate: Xi'an and Hakone are complete and publicly published. Hakone's
`218`-page pocket PDF is hash-synced to Nutstore, and Pages run `32418706768`
verified both destination manifests. Lanzhou is now the only active book;
never work on two destination books at once.
