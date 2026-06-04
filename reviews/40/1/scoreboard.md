<!--tauceti-scoreboard-->
## AI review — blocked

Each rubric is judged independently by Opus or Codex; only integrity angles can block. See the [rubrics](https://github.com/FormalFrontier/TauCetiReview/tree/main/rubrics).

| | rubric | state | judge | summary |
|---|---|---|---|---|
| ⛔ | scope | blocked | `claude/claude-opus-4-8` | The PR jumps to the Layer-6 endpoint (ReductiveGroup/SemisimpleGroup) and Layer-5 IsUnipotent with True/nilpotence placeholders, skipping the roadmap's prescribed Layer 0–5 dependency chain; there is no proximate path from these shells to the named target, and a real definition will replace rather than extend them. AffineAlgGroup/AlgPoints are plausible Layer-0 foundations, so the buildable material is bundled with premature endpoints. |
| ⛔ | correctness | blocked | `codex/gpt-5.5` | The PR encodes the central reductive/semisimple conditions as placeholders and mis-types unipotence as a property of coordinate-ring group-like elements rather than group points. These are semantic faults in the new API, not missing downstream lemmas. |
| ✅ | reuse | approved | `claude/claude-opus-4-8` | No duplication: the new declarations (AffineAlgGroup, IsUnipotent, ReductiveGroup, SemisimpleGroup, AlgPoints) have no existing counterparts in Mathlib or TauCeti, and the PR reuses GroupLike, IsNilpotent, Algebra.FiniteType, and Algebra.IsGeometricallyReduced where appropriate. |
| ✅ | attribution | approved | `claude/claude-opus-4-8` | The PR credits its central source (Kim Morrison's Mathlib draft #34897) in both the copyright header and the module docstring, with a link, and lists the relevant textbook references (Conrad, Borel). Attribution is complete for the work done. |
| 🟡 | api-design | changes requested | `claude/claude-opus-4-8` | The public class hierarchy exposes vacuous `True` fields, a content-free `True` lemma, and an unused `AlgPoints` definition with no API; the `IsUnipotent` characteristic API is also incomplete. The exposed interface either characterizes nothing or has no consumer. |
| 🟡 | generality | changes requested | `codex/gpt-5.5` | The new APIs are not at the natural Mathlib level: key definitions are either special cases where the general functor-of-points form is immediate, or vacuous subclasses that add no mathematical condition. |
| 🟡 | placement | changes requested | `codex/gpt-5.5` | The new declarations are in a plausible algebraic-group file, but one import is evidently broader than what the file uses. |
| 🟡 | naming | changes requested | `codex/gpt-5.5` | The introduced API contains names that advertise substantive radical-triviality statements while their types are only `True`. These names would be misleading once downstream code depends on them. |
| 🟡 | documentation | changes requested | `codex/gpt-5.5` | Several docstrings overstate placeholder definitions or misidentify the objects being documented. |
| ✅ | proof-quality | approved | `codex/gpt-5.5` | No proof-quality issues found in the added file. The only nontrivial proof is short, readable, and does not rely on undocumented `change`/`show` or obscure definitional equality. |
| ✅ | deprecation | approved | `claude/claude-opus-4-8` | Purely additive PR introducing a new file with new declarations; no existing public API is renamed, removed, or weakened, and there is no Mathlib bump. Nothing in the deprecation/backward-compatibility lane to flag. |

♻️ = approved on an earlier commit, re-run before merge. Spent today: $2.47/$10.