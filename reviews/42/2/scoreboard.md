<!--tauceti-scoreboard-->
## AI review — changes requested (budget cap reached; deferred api-design and after)

Each rubric is judged independently by Opus or Codex; only integrity angles can block. See the [rubrics](https://github.com/FormalFrontier/TauCetiReview/tree/main/rubrics).

| | rubric | state | judge | summary |
|---|---|---|---|---|
| ♻️ | scope | stale (re-run pending) | `claude/claude-opus-4-8` | Ports Stage 0.1 (SLSC typeclass + discreteness of homotopy-class fibres, #31576) and Stage 0.2 (based-path space + endpoint-preimage path components, #38292) named in the UniversalCovers roadmap, plus a prelude vendoring pending-Mathlib API. The three files form a single prerequisite dependency stack toward the one universal-cover target. |
| ♻️ | correctness | stale (re-run pending) | `codex/gpt-5.5` | No correctness or faithfulness issues found in the new based-path, SLSC, and prelude declarations under this rubric. |
| 🟡 | reuse | changes requested | `codex/gpt-5.5` | One public prelude theorem adds a parallel path-connectedness API where the existing `JoinedIn` API already supplies the same data. |
| ✅ | attribution | approved | `claude/claude-opus-4-8` | All three new files now carry in-file source-PR credit and author attribution matching the roadmap: SemilocallySimplyConnected.lean cites #31576 (discreteness) and #31449, BasedPath.lean cites #38292, and the prelude cites #38292, all crediting Kim Morrison. The prior review's two findings (missing #31576 credit, missing per-file PR credit) are resolved. |
| 🟡 | api-design | changes requested | `codex/gpt-5.5` | The PR exposes more implementation surface and reducible bodies than the universal-cover Stage 0 API appears to need. Several new definitions are made public by unfolding rather than by characteristic lemmas. |
| 🟡 | generality | changes requested | `codex/gpt-5.5` | The PR introduces useful local notions but several exported declarations are not at their natural level: some global hypotheses should be local, one structure carries unused endpoint parameters, and one theorem has an unused SLSC assumption. |
| ♻️ | placement | stale (re-run pending) | `claude/claude-opus-4-8` | Files are coherently placed under AlgebraicTopology/FundamentalGroupoid/, matching Mathlib's home for this material; the Prelude vendors only declarations genuinely absent from the pinned Mathlib, with attribution. No evidently-wrong or unused imports (e.g. Topology.Order.Basic is needed for exists_Ioc_subset_of_mem_nhds'). |
| 🟡 | naming | changes requested | `codex/gpt-5.5` | Two public names overstate or misdescribe their conclusions and should be renamed before exposing this API. |
| 🟡 | documentation | changes requested | `claude/claude-opus-4-8` | The mathematics is documented, but several docstrings carry dangling or stale cross-references and one theorem documents its proof. Module-level and definition docstrings cite declarations that do not exist under the names given. |
| 🟡 | proof-quality | changes requested | `claude/claude-opus-4-8` | Proofs are generally robust automation, but several goals are closed by `change` across Subtype/coercion definitional equality without justification (one with no comment), and the deformTerminal evaluation lemmas rely on simp-unfolding a tactic-constructed definition. |
| ♻️ | deprecation | stale (re-run pending) | `claude/claude-opus-4-8` | Purely additive PR: three new files (BasedPath, SemilocallySimplyConnected, UniversalCoverPrelude) in a new directory, with no modification, rename, removal, or weakening of any existing public API and no Mathlib bump. Nothing in the deprecation/backward-compatibility angle is at risk. |

♻️ = approved on an earlier commit, re-run before merge. Deferred api-design and after to the next run.

<sub>Review spend: $7.09.</sub>