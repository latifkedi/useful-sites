# Maintaining the directory

The runbook: what runs by itself, what only the owner can do, and how to
recover. Commands run from the repository root. Install the tools once:

```sh
pip install -r requirements-dev.txt   # requests (scans), Pillow (images)
npm ci                                # browser tests only
```

## What each workflow does

| Workflow | When | What it does |
|---|---|---|
| `build.yml` (Build check) | every push to `main`, every pull request, by hand, and when another workflow starts it | Rebuilds, runs `test_build.py`, `test_helpers.py`, `test_search.js`, `test_repo.py`, checks the committed output equals a fresh build; the browser tests in a second job |
| `link-check.yml` | Sunday 23:00 UTC (starts hours late, usually early Monday), or by hand | Scans every link, audits GitHub repositories and description freshness, rebuilds on the current `main`, tests, pushes `verified.json`, `health.json` and the rebuilt site (retrying if `main` moved), starts the Build check, comments on the pinned `link-check` issue |
| `approve-link.yml` | the `approved` label on a `new-link` issue | Writes the record (`data/from_issue.py`), rebuilds, opens a pull request on `link/issue-N`, starts the Build check on that branch; never merges |
| `backup.yml` | Wednesday 03:30 UTC, or by hand | Attaches a full git bundle and a tarball of `data/notes` and `data/*.json` to a release tagged `backup-YYYY-MM-DD`; keeps the latest 8 |
| Dependabot (`.github/dependabot.yml`) | weekly | Pull requests for GitHub Actions, npm and pip (`requirements-dev.txt`) versions |

Commits and pull requests made with `GITHUB_TOKEN` trigger no workflow. That is
why `link-check.yml` tests before it pushes and both bots start the Build check
with `gh workflow run`. If a bot commit or bot pull request shows no Build
check, start it: Actions → Build check → Run workflow → pick the branch.

## Things only the owner can do

- **Check flagged links in a real browser.** The scanner is blocked by
  Cloudflare and the like. Open the address; if the real page loads, record it:
  `python data/mark_ok.py https://example.com ...` (writes `ok`, today's date
  and a recheck date half a year on into `data/manual.json`). Commit
  `data/manual.json`.
- **Approve submissions.** Read a `new-link` issue; if it fits, add the
  `approved` label. Then rewrite the pull request's descriptions in both
  languages, delete the `review` field, `python data/build.py`, push to the
  branch, merge when green.
- **Repository settings** (Settings → Actions → General):
  `Read and write permissions` for workflows (the scan pushes, the approval
  workflow pushes a branch), and `Allow GitHub Actions to create and approve
  pull requests` (otherwise `approve-link.yml` fails at `gh pr create`; this
  was off as of 22 October 2026).
- **GitHub Pages** (Settings → Pages): deploy from branch `main`, folder `/`.
- **Labels.** `.github/labels.yml` lists what must exist; `data/test_repo.py`
  fails when a form or workflow names a label not listed there. A label listed
  but missing on GitHub is created by hand:

  ```sh
  gh label create new-link     --color 0e8a16 --description "A link suggested through the issue form"
  gh label create broken-entry --color d93f0b --description "A dead link, moved address or wrong description"
  gh label create approved     --color 5319e7 --description "Maintainer-only: turns a new-link issue into a pull request"
  gh label create link-check   --color fbca04 --description "The pinned weekly maintenance issue (link and repository health)"
  gh label create dependencies --color 0366d6 --description "Dependabot version updates"
  ```
- **Images, drawn by hand.** CI does not run them (`make_og.py` refuses to run
  where `CI` is set: its monospace face is a system font, Consolas on Windows,
  and differs elsewhere). After adding or removing a category or a
  learning path: `python data/make_og.py` and commit `og/` (it deletes images
  nothing claims). After the record
  count passes a new hundred: the same for `og.png`. After changing the mark:
  `python data/make_icons.py` and commit `icons/`.
- **Pin the `link-check` issue** if the workflow could not (it tries once, when
  it opens the issue).

## Weekly (after the Monday scan, about 15 minutes)

1. Open the pinned `link-check` issue and read the newest comment. The top is
   only what changed since last week.
2. **Newly dead:** replace the address, or remove the record (add it to
   `data/removed.txt` with the reason so it is not re-imported).
3. **Newly failing:** open each in a browser. Opens fine → `mark_ok.py`.
   Gone → wait for next week's scan to confirm, or remove it now.
4. **Newly archived / stale / deleted repositories:** say so in the
   description, or remove the record.
5. **Description freshness** (the Turkish section): fix any taken-over or
   parked domain at once; check perishable claims (free, beta, waitlist).
6. Merge or close Dependabot pull requests once their Build check is green.
7. Triage new issues: `broken-entry` fixes, `new-link` approvals.

## Quarterly

- Work through **Manual decisions due for a recheck** (folded in the weekly
  comment): reopen each in a browser, renew with `mark_ok.py` or remove.
- Run `python data/coverage.py` and update the "Wanted" counts and date in
  `CONTRIBUTING.md`.
- Download the newest backup release (bundle + tarball) and keep it off GitHub.
- Check that the last few Build check runs on `main` include the bot commits.

## Yearly

- Re-check every source's licence in `data/sources.py`
  (`gh api repos/OWNER/REPO --jq .license.spdx_id`, the LICENSE file or README
  where that says `NOASSERTION`, the footer for blogs); upstream licences change.
- Read `ABOUT.md`, `README.md` and `CONTRIBUTING.md` against what the site does.
- Review `data/removed.txt` and `data/manual.json` for entries nobody needs.
- Prune labels, workflows and dependencies that no longer earn their keep.

## Restoring from a backup

Each `backup-YYYY-MM-DD` release (Releases page) has two files.

The whole repository, with history:

```sh
gh release download backup-YYYY-MM-DD --repo latifkedi/useful-sites   # or from the browser
git bundle verify useful-sites-YYYY-MM-DD.bundle
git clone useful-sites-YYYY-MM-DD.bundle useful-sites
cd useful-sites
git remote set-url origin https://github.com/latifkedi/useful-sites.git   # or a new home
git push origin main          # add --force only if you mean to overwrite what is there
```

Only the data, without git:

```sh
tar -xzf data-YYYY-MM-DD.tar.gz        # restores data/notes/ and data/*.json
python data/build.py                   # regenerates everything else
python data/test_build.py
```

If GitHub itself is gone, the bundle is enough to publish anywhere that serves
static files: the repository root is the site.

## Adding a collaborator

1. Settings → Collaborators → Add people. `Write` is enough to push, label and
   merge; keep `Admin` with the owner.
2. Point them at this file, `CONTRIBUTING.md` and `data/README.md`.
3. They can do everything under "Weekly" and approve submissions. Repository
   settings, Pages and the labels on GitHub stay with the owner.
