## AI review (round 1): **blocked**

See the [review rubrics](https://github.com/FormalFrontier/TauCetiReview/tree/main/rubrics).

### ⛔ scope — block  `claude/claude-sonnet-4-6`
This PR adds a trivial theorem explicitly labeled in its own docstring as a throwaway auto-merge gate test that should never be merged. It has no connection to any roadmap target — the roadmap checkout is empty and no target is cited.
- `TauCeti/Basic.lean:16` — The added theorem `amGate : 0 < 19` carries a docstring stating it is a 'throwaway: auto-merge gate test (should be blocked, never merged).' This is self-admittedly off-roadmap and serves no mathematical purpose. _Fix:_ Do not merge. Remove the theorem entirely.
- No roadmap target is cited in the PR, and the roadmap checkout contains no files, so no path from this material to any target can exist. _Fix:_ A PR must identify a specific roadmap file and node/heading; this PR identifies none.

### ✅ correctness — approve  `codex/gpt-5.5`
No correctness or faithfulness issue found: the only new theorem states the true arithmetic fact `0 < 19`, and trivial-but-true material is outside this rubric's rejection criteria.

### ⛔ reuse — block  `claude/claude-sonnet-4-6`
`amGate : 0 < 19 := by norm_num` is a named export for a concrete numeric inequality that Mathlib's `norm_num` decision procedure already closes at every callsite. No caller needs to import this name instead of writing `by norm_num`.
- `TauCeti/Basic.lean:17` — `amGate` is a direct duplicate of `norm_num` capability: any use of `amGate` is replaceable by `by norm_num` or `by decide`, so the named theorem adds no reusable API and should not be exported. _Fix:_ Remove `amGate` entirely. Callers that need `0 < 19` should close the goal inline with `norm_num`.

### 🟡 proof-quality — request_changes  `claude/claude-sonnet-4-6`
The added theorem `amGate` is explicitly labelled by its own docstring as a throwaway test artifact that should never be merged. It contributes no reusable mathematical fact to the library and should be removed before merge.
- `TauCeti/Basic.lean:17` — `theorem amGate : 0 < 19` is self-described as 'should be blocked, never merged'. It adds a vacuous, purpose-free declaration to the public namespace — no reusable lemma, no meaningful mathematical content. _Fix:_ Delete the theorem entirely. If an auto-merge gate mechanism is needed, implement it outside the library's Lean source (e.g., a CI step or a separate file excluded from the public API).
