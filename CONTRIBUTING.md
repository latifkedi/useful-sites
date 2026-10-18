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

Ten areas: software, data and AI, infrastructure and systems, security,
science and mathematics, economics and finance, design and media (including
architecture), learning and reference, developer tools and discovery, and open
access and archives.

What is turned away, and why:

| Not accepted | Reason |
|---|---|
| Account-gated dashboards | Useless to anyone but the account holder |
| Search engine result URLs | A query is not a resource |
| Personal file shares and profiles | Means nothing to a third party |
| Links that do not resolve | Checked before acceptance |
| Pure marketing pages with no product behind them | Nothing to describe |

## Where the directory is thin, and what it leaves out on purpose

`python data/coverage.py` counts how many records touch a set of topics (a rough
instrument: it matches words, so it finds a gap, it does not measure one).

**Wanted** — topics a programmer, data person or maker looks for and the
directory barely has (as of 6 October 2026, matching records in brackets):
WebAssembly (2), regular expressions (8), accessibility (10), LaTeX and
typesetting (3), maps and GIS (4), low-code and no-code (3), cryptography for
learners (12). A suggestion in one of these is welcome even if it is not
famous; the question is still whether a description of how it differs can be
written.

**Left out on purpose** — these are not gaps, and a suggestion there will
usually be turned away:
- The natural sciences as a subject. Chemistry (4), biology and genomics (2)
  and astronomy (14) are thin because the directory takes science as data,
  tools and open access (one category, *Bilim & Akademik*), not as a general
  science directory. A genome browser or an open dataset fits; a popular
  astronomy blog does not.
- Hobby and leisure sites with no tool, data or learning path behind them
  (chess, music listings, entertainment, shopping).
- News and opinion, except where a source is a standing reference (a changelog,
  a newsletter a field depends on).
- Anything whose entry could only say what it is, never how it differs.

This list is a decision, not a law: if you think a line is drawn wrongly, say
so in an issue with an example.

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

The build writes `links.js`, `desc.tr.js`, `links.en.js`, `app.js` (joined from `src/app/*.js` -- edit the parts), `feed.xml`, `sitemap.xml`,
`robots.txt` and the pages under `k/`. All of them are committed, and CI fails
if what you committed does not match a fresh build.

Both languages are required. Turkish and English descriptions should say the
same thing, not one be a machine translation of the other.

Tags come from the 73 canonical tags in `data/tags.py`. Anything else is mapped
through the `ALIAS` table or dropped — it is never invented. If a genuinely new
tag is needed, add it to `CANON` and to `LABELS` in the same change, and to a
facet head if it is not a topic.

Each record carries exactly one price tag (`ücretsiz`, `freemium`, `ücretli`),
and two to four tags besides price and licence (`açık-kaynak`, `açık-ağırlık`
do not count): a content type (`referans` for something you read or look up,
`araç` for something you operate), a topic, and where it is clear from the
record, a platform (`tarayıcı-içi`, `masaüstü`, `mobil`, `cli`, `eklenti`,
`çevrimdışı`, `self-hosted`, `hesap-gerekmez`) or a stack. Every tag has to be
supported by the record's own text or be plain fact about the thing; a weak
second tag is worse than none. `test_build.py` fails above four, and holds the
number of records under two to a ceiling that only goes down.

Learning records (the learning, practice, books, programming-language and
security lab and career categories) also carry one level, judged from what the
resource assumes, not from its name:

- `başlangıç` — written for newcomers: a curriculum or tutorial that assumes no prior knowledge of the subject.
- `orta` — assumes you already work in the subject: practice, interview prep, references and courses that build on the basics.
- `ileri` — deep material: research papers and journals, internals, compilers and hardware-level performance, contest problems that need mathematics.

Leave the level off when the resource spans all three (a course platform, a
project list) or is not a learning resource at all (a certification body, a
newsletter).

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
