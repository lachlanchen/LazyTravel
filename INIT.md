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
5. Continue only the next unfinished Xi'an chapter. Update its fact ledger,
   aligned JSON, three language passes, pinyin/furigana review, assets, and QA.
6. Run focused tests while editing, then the full validation/build sequence:

```bash
python3 -m unittest discover -s tests
python3 scripts/build_xian_review.py
python3 scripts/build_website.py
python3 scripts/validate_site_parity.py
python3 scripts/qa_website.py --url http://127.0.0.1:4173/
```

7. Review every new or changed B6 page and desktop/mobile screenshot. Record the
   review under `books/china/cities/xian/editorial/`.
8. Copy only `dist/books/xian/xian-pocket-review.pdf` to
   `/home/lachlan/Nutstore Files/Share/LazyTravel/` after all checks pass, and
   verify the copied SHA-256.
9. Update the milestone in `README.md`, make one scoped commit, and push it to
   `origin/main`.

Current gate: all 11 Xi'an chapters are internally reviewed and reproducibly
built as the synchronized pocket book and website. Present the complete Xi'an
milestone for user review. Do not start Lanzhou until that review is accepted.
