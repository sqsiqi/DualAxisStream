"""Command-line demo for the DualAxisStream public interface."""

from __future__ import annotations

import argparse
import json
import sys

from .core import CoreNotReleasedError
from .pipeline import DEFAULT_CONFIG, DualAxisStreamPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="DualAxisStream demo")
    parser.add_argument("--source", required=True, help="Path to the source video")
    parser.add_argument("--reference", required=True, help="Path to the reference image")
    parser.add_argument("--prompt", required=True, help="Text description of the edit")
    parser.add_argument("--output", default="outputs/edited.mp4", help="Output video path")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="YAML configuration")
    parser.add_argument("--device", default="cuda", help="Torch device")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate inputs and print the configuration without calling the core hook",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    pipeline = DualAxisStreamPipeline(config_path=args.config, device=args.device)

    if args.check:
        from .io import validate_image, validate_video

        source = validate_video(args.source)
        reference = validate_image(args.reference)
        print(json.dumps({"source": source, "reference": reference}, indent=2))
        print("\nConfiguration:")
        print(json.dumps(pipeline.config, indent=2))
        print("\nInputs and configuration are valid. The core modules are withheld in "
              "this pre-release.")
        return 0

    try:
        pipeline.edit(
            source_video=args.source,
            reference_image=args.reference,
            prompt=args.prompt,
            output_path=args.output,
        )
    except CoreNotReleasedError as exc:
        print(f"CoreNotReleasedError: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
