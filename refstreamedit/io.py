"""Small input-validation helpers used by the public interface."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import cv2


VIDEO_SUFFIXES = {".mp4", ".mov", ".mkv", ".avi", ".webm"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}


def _check_file(path: str | Path, suffixes: set[str], kind: str) -> Path:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"{kind} not found: {p}")
    if p.suffix.lower() not in suffixes:
        raise ValueError(f"Unsupported {kind} format: {p.suffix}")
    return p


def validate_video(path: str | Path) -> Dict[str, Any]:
    """Validate a video path and return basic metadata."""

    p = _check_file(path, VIDEO_SUFFIXES, "video")
    cap = cv2.VideoCapture(str(p))
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {p}")
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    cap.release()
    if frames <= 0 or width <= 0 or height <= 0:
        raise ValueError(f"Video has invalid metadata: {p}")
    return {
        "path": str(p),
        "fps": fps,
        "frames": frames,
        "width": width,
        "height": height,
    }


def validate_image(path: str | Path) -> Dict[str, Any]:
    """Validate an image path and return its shape."""

    p = _check_file(path, IMAGE_SUFFIXES, "image")
    image = cv2.imread(str(p), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Cannot read image: {p}")
    height, width = image.shape[:2]
    return {"path": str(p), "width": width, "height": height}
