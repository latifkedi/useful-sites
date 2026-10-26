Closes #ISSUENO

Written by `data/from_issue.py` from the submitted issue form. The record is
credited to the `community` source and dated the day it was approved.

**Before merging, the description needs a pass.** The submitter wrote one
language in one voice, so the Turkish and English fields currently carry the
same text, and the "how does it differ" half may need sharpening. The new
record carries a `review` field saying so, and `data/test_build.py` fails
while it is present. Rewrite both descriptions, delete the `review` field,
run `python data/build.py`, and push to this branch.

About the checks: a pull request opened by a workflow does not start other
workflows, so the approval workflow started the **Build check** on this branch
itself (Actions tab, "Build check", run on this branch). Expect it to be red
until the `review` field is gone. Your own push to this branch runs it again
the normal way. If no run shows up, start it by hand: Actions → Build check →
Run workflow → this branch.

Check the category and tags as well: the category comes from the form's
dropdown ("Not sure" lands in `araclar`), and any tag that did not match the
canonical table in `data/tags.py` was dropped rather than guessed at.
