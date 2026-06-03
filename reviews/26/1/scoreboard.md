<!--tauceti-scoreboard-->
## AI review — changes requested

Each rubric is judged independently by Opus or Codex; only integrity angles can block. See the [rubrics](https://github.com/FormalFrontier/TauCetiReview/tree/main/rubrics).

| | rubric | state | judge | summary |
|---|---|---|---|---|
| ✅ | scope | approved | `claude/claude-opus-4-8` | The PR ports the deck transformation group Deck p from mathlib4#40135, which the UniversalCovers roadmap names verbatim as Stage 0 item 4 and as the prerequisite for the Stage 1 target Deck(proj) ≃* FundamentalGroup. The vendored Homeomorph.applyMulAction is the genuine prerequisite action the same node calls for, making this one coherent unit. |
| ✅ | correctness | approved | `codex/gpt-5.5` | The new `Deck p` definition faithfully formalizes deck transformations as self-homeomorphisms of `E` over an arbitrary map `p : E → X`, and the action/continuity instances match the visible subgroup-action construction. I found no semantic mis-formalization, vacuity, or prerequisite smuggling in the diff. |
| ✅ | reuse | approved | `codex/gpt-5.5` | No reuse or duplication issue is apparent in this PR: the new `Deck p` API and the vendored homeomorphism evaluation action are narrowly scoped and match the stated missing prerequisite. |
| ✅ | attribution | approved | `codex/gpt-5.5` | The added files credit the stated Mathlib draft PR and author in both headers/module docs, including the vendored `Homeomorph.applyMulAction` material. I found no attribution issue from the provided diff; local grep was unavailable due a sandbox setup failure before shell startup. |
| 🟡 | api-design | changes requested | `claude/claude-opus-4-8` | Minimal surface, bodies hidden, and the membership/projection characterization is present. The key equivariance lemma proj_smul lacks @[simp] even though no simp lemma can otherwise reduce p (h • e). |
| ✅ | generality | approved | `claude/claude-opus-4-8` | Material sits at the natural Mathlib level: `Deck p` is stated for an arbitrary map with no covering hypothesis and no topology on `X`, and the vendored `Homeomorph.applyMulAction` carries only the intrinsic `[TopologicalSpace Y]`. No unused/too-strong assumptions or special-case duplication. |
| ✅ | placement | approved | `codex/gpt-5.5` | The new declarations are placed in natural homes for their dependency level: generic homeomorphism-action instances under `TauCeti.Topology.Algebra`, and the roadmap-facing deck transformation subgroup under `TauCeti.AlgebraicTopology.UniversalCover`. The imports are direct and topic-specific rather than broad. |
| ✅ | naming | approved | `codex/gpt-5.5` | Names describe the introduced objects and conclusions at the expected strength, and no notation is introduced. I found no naming or notation issue material enough to request changes. |
| 🟡 | documentation | changes requested | `codex/gpt-5.5` | The substantive file/module documentation is present, but a public result advertised as a main result is missing its own docstring. |
| ✅ | proof-quality | approved | `codex/gpt-5.5` | No proof-quality issues found in the visible diff; the proofs are short, direct, and do not use undocumented `change`/`show` or brittle named-lemma chains. |
| ✅ | deprecation | approved | `claude/claude-opus-4-8` | Purely additive PR: two new files, no public declaration renamed, removed, or weakened, and no Mathlib bump. Vendored instances are namespaced under TauCeti, so no backward-compatibility concerns. |

♻️ = approved on an earlier commit, re-run before merge. Spent today: $1.41/$10.