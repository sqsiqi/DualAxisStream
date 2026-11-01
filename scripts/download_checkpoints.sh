#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "${ROOT}/wan_models" "${ROOT}/longlive_models"

huggingface-cli download Wan-AI/Wan2.1-T2V-1.3B \
  --local-dir-use-symlinks False \
  --local-dir "${ROOT}/wan_models/Wan2.1-T2V-1.3B"

huggingface-cli download Efficient-Large-Model/LongLive \
  --local-dir "${ROOT}/longlive_models"

echo "Base checkpoints downloaded under ${ROOT}."
echo "The task LoRA and the core editing modules are released separately."
