# About

## The problem this addresses

A link's name and URL do not tell you what it is. A line reading
`regex101.com` says nothing until the site is opened. Whereas the following
lets a reader decide in seconds whether it is worth opening:

> Explains a regular expression token by token, and its debugger shows exactly
> where a match falls apart.

Every entry in this directory carries that: **what the resource does** and
**where it parts ways with its neighbours.** The second is the substantive
half. Choosing among several tools that address the same problem does not call
for a feature list; it calls for the line along which they differ.

## Attribution

The links were selected and curated by hand. The descriptions, the category
scheme, the tag vocabulary and the site itself were produced with AI assistance
and reviewed before publication: the text is **machine-assisted and
human-reviewed**.

This matters because of what the directory claims. Each entry carries a
comparative judgement — "lighter than", "unlike", "in exchange for" — and those
judgements are machine-generated and human-reviewed rather than
human-authored. They are grounded in the projects' own documentation and in
metadata retrieved from the sites themselves, not invented, but they remain
judgements. Read them as a starting point rather than a verdict, and file a
correction as an issue where one is wrong.

## Who maintains it

The directory is maintained by the owner of the repository,
[latifkedi](https://github.com/latifkedi) on GitHub. There is no organisation
behind it, no sponsorship, no advertising, and the site carries no trackers or
analytics.

## Where the entries come from

Every entry records which source surfaced it, and that source is shown on the
entry and offered as a filter. There are three tiers, and they are not held to
the same standard:

- **The curator's own archive** — a bookmark collection gone through one entry
  at a time; each description was written against the project's own
  documentation.
- **Published compilations** — public lists such as awesome-lists. Only the
  in-scope, live and worthwhile entries were taken; each was checked and its
  description written here rather than copied, but it was not part of the
  original archive and carries less first-hand use.
- **Community submissions** — suggestions made through the issue form. Nothing
  is published automatically: a person reads the issue, writes the
  description and decides whether it fits.

Presenting these as equal would misrepresent the directory, so they are kept
apart. Entries excluded during curation:

- Account-gated dashboards, which are of no use to a reader
- Search engine result URLs
- Personal file shares
- Links that failed a liveness check

## Scope

This is not a "best tools" list. Two or three entries per category are marked
as starting points, which means "begin here if the area is new to you", not
"this is the best available".

## How the links are checked

Link directories share a common failure: they rot. After a period, a
significant fraction stops resolving and the collection loses its value.

Three mechanisms work against that.

Every week a scheduled job requests every link. A page that answers is marked
checked on that date, and the date is shown on the entry. A 404, a 410 or a
domain that no longer resolves counts against a link, but only two such scans
in a row mark it dead: sites go down for an afternoon. Other failures —
timeouts, refused connections, the 403 a bot-shy site returns — are recorded as
suspect, not dead. Where a person has opened a flagged link in a browser and
found it fine, that decision is recorded and the scan cannot overturn it, but
it falls due for another look after half a year. Such a link, and any the scanner is
turned away from, shows the date of the latest scan, not of the human check.

Linked GitHub repositories receive a second, separate audit, because a
repository can cease to be maintained without ever returning a 404 — one entry
here is exactly that case: a 76,000-star compilation whose pages still load,
archived in November 2025. A link check cannot detect this; a repository audit
can. Entries whose repository is archived, deleted or has had no push in two
years carry a badge saying so.

Anything the scan finds dead is marked on the site itself, so a visitor is
warned before following the link rather than after. Every entry additionally
carries a Wayback Machine link, so it retains some value once its target is
gone permanently.

What was removed on purpose, and why, is listed on the changes page with the
weekly digests of what arrived.

## Contributing and reporting a problem

The **Submit a Link** control on the site accepts a single entry through a
form, or reads a bookmark export (`.html`, `.json`, `.csv`) and filters out
everything already present, leaving only what is new. The file is parsed in the
browser and uploaded nowhere; there is no server to upload it to.

Submissions open as GitHub issues. Nothing reaches the site automatically: an
issue is read, a description is written, and the entry is included in the next
build if it fits the scope.

The submission form requires a "how does it differ" field. If the answer is not
known, saying so is acceptable and it will be researched — but left empty, the
entry does not carry what the directory exists to provide.

A dead link, a wrong description or a comparison that is off is best reported
as an [issue on GitHub](https://github.com/latifkedi/useful-sites/issues/new/choose);
each entry in the app has a "report a problem" link that fills the form in.

---

*Build scripts, data layout and the procedure for adding an entry:
[data/README.md](data/README.md).*
