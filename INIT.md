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
5. Continue only the next unfinished Hakone chapter. Chapters 1 through 9 are
   accepted; Chapter 10 is next. Update its fact ledger, aligned JSON, three
   language passes, pinyin/furigana review, assets, and QA before moving
   forward.
6. Run focused tests while editing, then the full validation/build sequence:

```bash
python3 -m pytest -q
python3 scripts/build_hakone_review.py
python3 scripts/build_website.py \
  --book data/japan/prefectures/kanagawa/hakone/book.json \
  --output build/site-hakone
```

Serve `build/site-hakone` on one temporary unused project-owned port, run
`scripts/qa_destination_website.py` at desktop and mobile sizes, then terminate
only that exact temporary server. Leave the existing port `4173` server and all
noVNC/Xvfb/x11vnc/websockify processes untouched.

7. Review every new or changed B6 page and desktop/mobile screenshot. Record the
   review under `books/japan/prefectures/kanagawa/hakone/editorial/`.
8. After every accepted chapter milestone, sync only the verified pocket PDF:

```bash
python3 scripts/build_hakone_review.py --skip-map --sync-nutstore
```

Verify the Nutstore and `dist` SHA-256 values match.
9. Update the milestone in `README.md`, make one scoped commit, and push it to
   `origin/main`.

For a complete-book public website milestone, also run:

```bash
python3 scripts/verify_deployed_site.py \
  --url https://lachlanchen.github.io/LazyTravel/
```

Current gate: Xi'an is complete and publicly published. Continue with Hakone
at `japan/prefectures/kanagawa/hakone`. Hakone Chapters 1 through 9 are accepted
and synced; Chapter 10 is next. Lanzhou follows the complete Hakone book; never
work on both destination books at once.
