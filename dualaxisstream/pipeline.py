"""Public inference interface for DualAxisStream."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from .core import apply_edit
from .io import validate_image, validate_video


DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "configs" / "dualaxisstream.yaml"


class DualAxisStreamPipeline:
    """Reference-guided streaming video editing.

    Parameters
    ----------
    config_path:
        Path to the YAML configuration. Defaults to ``configs/dualaxisstream.yaml``.
    device:
        Torch device string used by the full implementation.
    """

    def __init__(
        self,
        config_path: Optional[str | Path] = None,
        device: str = "cuda",
    ) -> None:
        self.config_path = Path(config_path) if config_path else DEFAULT_CONFIG
        if not self.config_path.is_file():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
        self.config: Dict[str, Any] = yaml.safe_load(self.config_path.read_text())
        self.device = device

    def edit(
        self,
        source_video: str | Path,
        reference_image: str | Path,
        prompt: str,
        output_path: str | Path,
        **overrides: Any,
    ) -> Any:
        """Edit ``source_video`` according to ``reference_image`` and ``prompt``.

        The inputs are validated before the core hook is called. The full release will
        run the streaming edit and write the result to ``output_path``.
        """

        source_info = validate_video(source_video)
        reference_info = validate_image(reference_image)
        if not prompt or not str(prompt).strip():
            raise ValueError("The editing prompt must be a non-empty string.")

        config = dict(self.config)
        if overrides:
            config.update(overrides)

        return apply_edit(
            source_video=str(source_video),
            reference_image=str(reference_image),
            prompt=str(prompt).strip(),
            output_path=str(output_path),
            source_info=source_info,
            reference_info=reference_info,
            config=config,
            device=self.device,
        )
