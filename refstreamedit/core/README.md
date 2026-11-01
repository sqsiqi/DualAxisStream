# Core modules (withheld)

This directory will contain the core identity--motion decoupling modules:

- the per-token foreground--background bridge,
- cross-attention value boosting,
- reference-first-frame key--value anchoring,
- the late identity lock,
- the foreground edge guard,
- the identity-orthogonal motion injection.

The task LoRA will be released together with these modules. The public pipeline calls
`refstreamedit.core.apply_edit`; the full release will replace the placeholder with the
actual implementation without changing the interface.
