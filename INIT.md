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
5. Keep Xi'an, Hakone, and all 11 Lanzhou chapters closed. Lanzhou's verified
   release commit and public deployed-site comparison are the only active
   gate. Do not reopen a chapter without a demonstrated failure and do not
   start another destination before publication closes.
6. Run focused tests while editing, then the full validation/build sequence:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/verify_sources.py
python3 scripts/build_series_website.py
python3 scripts/validate_site_parity.py \
  --book data/china/cities/lanzhou/book.json \
  --site site/china/cities/lanzhou
```

Serve `site` on one temporary unused project-owned port, run
`scripts/qa_destination_website.py` at desktop and mobile sizes, then terminate
only that exact temporary server when no review is waiting. Reuse an existing
LazyTravel HTTP server when one is already active, and leave all
noVNC/Xvfb/x11vnc/websockify processes untouched.

7. Review every new or changed B6 page and desktop/mobile screenshot. Record the
   review under `books/china/cities/lanzhou/editorial/`.
8. Sync only a verified Lanzhou pocket PDF through the destination build script.
   Verify the Nutstore and `dist` SHA-256 values match after every accepted
   chapter.
9. Update the milestone in `README.md`, make one scoped commit, and push it to
   `origin/main`.

For a public Lanzhou chapter milestone, also run after deployment:

```bash
python3 scripts/verify_deployed_site.py \
  --url https://lachlanchen.github.io/LazyTravel/china/cities/lanzhou/ \
  --book data/china/cities/lanzhou/book.json
```

Current gate: Xi'an and Hakone are complete and publicly published. All 11
Lanzhou chapters pass as a reproducible `216`-page pocket and synchronized
website; the repository and Nutstore SHA-256 is
`a6b70500bbe599b636786f4c5bd012c26fb8a3f2a5715909f729f1bc2e8a7dee`. Commit,
push, and verify the deployed Lanzhou payload, then close the destination. No
later destination is active, and two books must never enter production at once.
