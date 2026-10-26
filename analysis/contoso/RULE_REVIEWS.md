# Rule reviews — contoso

A person who knows the business reviewed these rules from `BUSINESS_RULES.md`. A **Confirmed** rule is the intended behavior; where its note differs from the legacy code, the note is the intent. A rule marked **Wrong** either misdescribes the code or describes behavior the new system should not keep, and **Discuss** still needs a decision. Neither is settled: the brief lists them as open questions, and the build will not pin them as the oracle.

| Rule | Verdict | When | Title | Note |
|---|---|---|---|---|
| RULE-006 | Confirmed | 2026-10-26T22:22:36Z | Department edits use optimistic concurrency (first save wins) | First save wins, with a deliberate overwrite that works. Block a save made with a stale RowVersion, show 'Current value: X' next to each conflicting field, and let a second Save overwrite. The legacy second save fails because HiddenFor re-posts the stale RowVersion; the rewrite must fix this (refresh the token). A delete made with a stale RowVersion is blocked the same way. |
| RULE-033 | Wrong | 2026-10-26T22:20:26Z | No authentication or authorization required for any page |  |
