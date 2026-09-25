Closes #ISSUENO

Written by `data/from_issue.py` from the submitted issue form.

**Before merging, the description needs a pass.** The submitter wrote one
language in one voice, so the Turkish and English fields currently carry the
same text, and the "how does it differ" half may need sharpening. The new
record carries a `review` field saying so; the build check fails while it is
present. Rewrite both descriptions, delete the `review` field, rebuild, and
the check goes green.

Check the category and tags as well: the category comes from the form's
dropdown ("Not sure" lands in `araclar`), and any tag that did not match the
canonical table in `data/tags.py` was dropped rather than guessed at.
