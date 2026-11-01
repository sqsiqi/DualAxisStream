"""DualAxisStream public package.

The core identity--motion decoupling modules are withheld in this pre-release.
See :mod:`dualaxisstream.core` for the release note and the core hook.
"""

from .pipeline import DualAxisStreamPipeline
from .core import CoreNotReleasedError

__all__ = ["DualAxisStreamPipeline", "CoreNotReleasedError"]
__version__ = "0.1.0"
