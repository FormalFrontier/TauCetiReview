#!/usr/bin/env python3
"""The merge sweep's decision must re-drive evicted-but-green PRs without thrashing on broken ones.

Covers decide_action (the pure policy) and that the merge gate it relies on (decide_from_comments) is
the SAME one the merge-only path uses, so the sweep can never enqueue something the normal gate refuses.
Dependency-free — run with `python tests/test_sweep.py` or under pytest.
"""
import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "runner"))
import sweep  # noqa: E402
import merge_from_scoreboard as mfs  # noqa: E402


def test_not_green_skips():
    action, _ = sweep.decide_action(merge_ok=False, in_queue=False, evictions_at_head=5, behind=9)
    assert action == "skip", action


def test_in_queue_skips():
    action, _ = sweep.decide_action(merge_ok=True, in_queue=True, evictions_at_head=0, behind=0)
    assert action == "skip", action


def test_green_not_queued_reenqueues():
    # The #311 case: green, evicted once transiently, not yet at the escalation threshold -> re-enqueue.
    action, _ = sweep.decide_action(merge_ok=True, in_queue=False, evictions_at_head=1, behind=4,
                                    escalate=2)
    assert action == "enqueue", action


def test_first_pass_reenqueues_even_when_behind():
    # Re-enqueue is the default even for a behind PR: the queue's rebuild is the cheap real test, and it
    # preserves the head-pinned green review (no re-review spend).
    action, _ = sweep.decide_action(merge_ok=True, in_queue=False, evictions_at_head=0, behind=20,
                                    escalate=2)
    assert action == "enqueue", action


def test_repeated_eviction_behind_updates_branch():
    # The #391 case: the queue keeps evicting this head and the PR is behind main -> stop re-enqueuing,
    # update the branch onto main (re-test + re-review against current main).
    action, _ = sweep.decide_action(merge_ok=True, in_queue=False, evictions_at_head=2, behind=7,
                                    escalate=2)
    assert action == "update_branch", action


def test_repeated_eviction_not_behind_flags():
    # Evicted past the threshold but already up to date with main: nothing to update, so surface it
    # rather than loop.
    action, _ = sweep.decide_action(merge_ok=True, in_queue=False, evictions_at_head=3, behind=0,
                                    escalate=2)
    assert action == "flag", action


def _scoreboard(head, states):
    meta = "<!--tauceti-meta:v1 " + json.dumps({"head_sha": head, "states": states}) + "-->"
    return [{"body": "<!--tauceti-scoreboard-->\n" + meta, "updated_at": "2026-06-26T00:00:00Z"}]


def test_gate_is_shared_with_merge_only():
    head = "deadbee"
    required = {"correctness", "reuse"}
    green = {"correctness": "green", "reuse": "green"}
    diff = "diff --git a/TauCeti/Foo.lean b/TauCeti/Foo.lean\n+x\n"
    # green + TauCeti-only + build green -> mergeable
    assert mfs.decide_from_comments(_scoreboard(head, green), head, required, diff, "SUCCESS", "")["merge"]
    # a stale scoreboard (different head) is refused — the sweep must never enqueue an unreviewed commit
    assert not mfs.decide_from_comments(_scoreboard(head, green), "other99", required, diff,
                                        "SUCCESS", "")["merge"]
    # a path outside TauCeti/ is refused
    diff2 = "diff --git a/.github/workflows/x.yml b/.github/workflows/x.yml\n+y\n"
    assert not mfs.decide_from_comments(_scoreboard(head, green), head, required, diff2, "SUCCESS", "")["merge"]


def run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")


if __name__ == "__main__":
    run()
