#!/usr/bin/env python3
"""upsert_scoreboard() must publish exactly one scoreboard comment per PR, editing in place.

The regression it guards (kim-em/TauCetiWorker#3): a review run whose local store does not know the
scoreboard's comment id used to POST a duplicate. Now it discovers the existing trusted scoreboard
from GitHub, edits that, and collapses older duplicates. Dependency-free — run with
`python tests/test_post.py` or under pytest.
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "runner"))
import post  # noqa: E402


class FakeGH:
    """Records gh_api calls; PATCH succeeds/fails per `patch_ok`, POST returns `post_id`."""
    def __init__(self, patch_ok=True, post_id=None):
        self.calls = []
        self.patch_ok = patch_ok
        self.post_id = post_id

    def __call__(self, method, endpoint, fields=None, body_file=None, failures=None, action=""):
        self.calls.append((method, endpoint))
        if method == "PATCH":
            if self.patch_ok:
                return {}
            if failures is not None:
                failures.append({"action": action})
            return None
        if method == "POST":
            return {"id": self.post_id} if self.post_id else {}
        return {}  # DELETE

    def methods(self):
        return [m for m, _ in self.calls]

    def to(self, method):
        return [e for m, e in self.calls if m == method]


def run(fake, existing, pr_state, plan_sb_id=None):
    post.gh_api = fake
    post.find_scoreboard_comments = lambda repo, pr: list(existing)
    failures = []
    sb_id, ok = post.upsert_scoreboard("o/r", 1, "body.md", plan_sb_id, pr_state, failures)
    return sb_id, ok, failures


def test_known_id_edits_in_place():
    fake = FakeGH(patch_ok=True)
    sb_id, ok, failures = run(fake, existing=[999], pr_state={"scoreboard_comment_id": 100})
    assert ok and sb_id == 100, (sb_id, ok)
    assert fake.to("PATCH") == ["/repos/o/r/issues/comments/100"], fake.calls
    assert "POST" not in fake.methods() and "DELETE" not in fake.methods(), fake.calls
    assert not failures


def test_adopts_existing_and_collapses_older():
    fake = FakeGH(patch_ok=True)
    pr_state = {}
    sb_id, ok, failures = run(fake, existing=[200, 150, 120], pr_state=pr_state)
    assert ok and sb_id == 200, (sb_id, ok)
    assert pr_state["scoreboard_comment_id"] == 200
    assert fake.to("PATCH") == ["/repos/o/r/issues/comments/200"]
    assert "POST" not in fake.methods()
    assert sorted(fake.to("DELETE")) == ["/repos/o/r/issues/comments/120",
                                         "/repos/o/r/issues/comments/150"], fake.calls
    assert not failures


def test_uneditable_adopted_id_falls_back_to_post():
    fake = FakeGH(patch_ok=False, post_id=999)
    sb_id, ok, failures = run(fake, existing=[300], pr_state={})
    assert ok and sb_id == 999, (sb_id, ok)
    assert fake.to("PATCH") == ["/repos/o/r/issues/comments/300"]
    assert fake.to("POST") == ["/repos/o/r/issues/1/comments"]
    assert not failures, "an uneditable adopted comment must not be recorded as a hard failure"


def test_no_existing_posts_new():
    fake = FakeGH(patch_ok=True, post_id=888)
    sb_id, ok, failures = run(fake, existing=[], pr_state={})
    assert ok and sb_id == 888, (sb_id, ok)
    assert "PATCH" not in fake.methods()
    assert fake.to("POST") == ["/repos/o/r/issues/1/comments"]


def test_our_failed_edit_is_recorded_not_duplicated():
    fake = FakeGH(patch_ok=False, post_id=777)
    sb_id, ok, failures = run(fake, existing=[], pr_state={"scoreboard_comment_id": 100})
    assert not ok, (sb_id, ok)
    assert "POST" not in fake.methods(), "a failed edit of our own comment must not post a duplicate"
    assert failures, "a failed edit of our own scoreboard must be recorded"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\nall {len(fns)} scoreboard-upsert checks passed")
