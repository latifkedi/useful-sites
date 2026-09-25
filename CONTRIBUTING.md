# Contributing

## Suggesting a link

Use the **Submit a Link** control on the site, or open a
[new-link issue](../../issues/new?template=new-link.yml) directly.

The form has a required field: **how does it differ from its neighbours.** That
field is the directory's only real value. An entry that says what a tool does
but not where it parts ways with the four tools like it does not carry what
readers come here for.

If the answer is not known, write that. It will be researched. Left empty, the
suggestion cannot be used.

Submissions open as GitHub issues. Nothing reaches the site automatically: an
issue is read, a description is written, and the entry goes in on the next
build if it fits the scope.

## What is in scope

Ten areas: software, artificial intelligence, infrastructure and systems,
security, data, science and mathematics, economics and finance, design and
media (including architecture), learning and reference, and open access and
archives.

What is turned away, and why:

| Not accepted | Reason |
|---|---|
| Account-gated dashboards | Useless to anyone but the account holder |
| Search engine result URLs | A query is not a resource |
| Personal file shares and profiles | Means nothing to a third party |
| Links that do not resolve | Checked before acceptance |
| Pure marketing pages with no product behind them | Nothing to describe |

A link being popular is not itself a reason to include it, and a link being
obscure is not a reason to exclude it. The question is whether a description
can be written that helps someone choose.

## Reporting a problem

Open a [broken-entry issue](../../issues/new?template=broken-entry.yml) for a
dead link, a moved address, a description that has gone stale, or a comparison
that is wrong.

Comparative claims are the most likely thing to be wrong, and corrections to
them are the most valuable. "X is lighter than Y" is a judgement; if it does
not match your experience, say so and say why.

## Adding an entry yourself

1. Append the record to `data/notes/<category>.json` (the file is the
   category — see [data/README.md](data/README.md) for the fields):

   ```json
   {
     "url": "https://example.com",
     "name": "Example",
     "tags": ["açık-kaynak", "python"],
     "tr": "Ne yaptığı ve komşularından nerede ayrıldığı.",
     "en": "What it does and where it parts ways with its neighbours.",
     "src": "kedi"
   }
   ```

2. Run `python data/build.py`
3. Run `python data/test_build.py` — it must pass
4. Commit the generated files along with your record

The build writes `links.js`, `links.en.js`, `feed.xml`, `sitemap.xml`,
`robots.txt` and the pages under `k/`. All of them are committed, and CI fails
if what you committed does not match a fresh build.

Both languages are required. Turkish and English descriptions should say the
same thing, not one be a machine translation of the other.

Tags come from the 63 canonical tags in `data/tags.py`. Anything else is mapped
through the `ALIAS` table or dropped — it is never invented. If a genuinely new
tag is needed, add it to `CANON` and to `LABELS` in the same change.

More detail: [data/README.md](data/README.md).

## Style of a description

Two sentences, occasionally three. First what the thing does, then where it
differs. No marketing register, no feature lists, no superlatives that cannot
be checked.

Weak:

> A powerful, modern and easy-to-use tool for developers.

Usable:

> Explains a regular expression token by token, and its debugger shows exactly
> where a match falls apart.

Where a project is dormant, archived or has a licensing catch, say so in the
entry. A directory that only praises is not useful.

## Licence

Contributions are published under CC BY 4.0, the same terms as the rest of the
descriptions.
