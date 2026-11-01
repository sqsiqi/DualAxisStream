"""RefStreamEdit public package.

The core identity--motion decoupling modules are withheld in this pre-release.
See :mod:`refstreamedit.core` for the release note and the core hook.
"""

from .pipeline import RefStreamEditPipeline
from .core import CoreNotReleasedError

__all__ = ["RefStreamEditPipeline", "CoreNotReleasedError"]
__version__ = "0.1.0"
