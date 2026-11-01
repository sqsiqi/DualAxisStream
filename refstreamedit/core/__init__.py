"""Core identity--motion decoupling modules.

The implementation of the per-token foreground--background bridge, cross-attention
value boosting, reference-first-frame key--value anchoring, the late identity lock, the
foreground edge guard, and the identity-orthogonal motion injection is temporarily
withheld. It will be released upon acceptance.

The public pipeline calls :func:`apply_edit`; the full release will replace this
placeholder with the actual implementation without changing the public interface.
"""

from __future__ import annotations

from typing import Any


class CoreNotReleasedError(NotImplementedError):
    """Raised when the withheld core modules are requested."""


_RELEASE_NOTE = (
    "The core identity-motion decoupling modules are not included in this "
    "pre-release. They will be released upon acceptance. See "
    "https://github.com/sqsiqi/RefStreamEdit for updates."
)


def apply_edit(**kwargs: Any) -> Any:
    """Apply the reference-guided edit.

    This placeholder keeps the public call signature stable. The full release will
    implement the streaming edit, the per-token bridge, the foreground identity
    modules, and the identity-orthogonal motion injection here.
    """

    raise CoreNotReleasedError(_RELEASE_NOTE)
