# Method

RefStreamEdit edits a source video according to a reference image and a text prompt. The
source video supplies the scene, the camera path, and the motion; the reference supplies
the target object's appearance. The edited foreground must follow the reference, while
the background and the source motion stay unchanged.

The method is built on a few-step streaming video generator. A source branch and a noisy
target branch are processed in parallel, and the edit is controlled at the token level
rather than by a single global blend rate.

## Why a global schedule is not enough

For a self-attention layer, let `K_src` and `K_trg` be the source and target keys. A
streaming editor with a global schedule blends them as

```text
K_hat_trg = beta(t) * K_trg + (1 - beta(t)) * K_src,
```

where `beta(t)` is shared by every spatial token. The foreground edit energy and the
background deviation energy are

```text
E_F = sum_{i in F} ||K_hat_trg_i - K_src_i||^2,
E_B = sum_{i in B} ||K_hat_trg_i - K_src_i||^2.
```

Because `K_hat_trg_i - K_src_i = beta(t) * (K_trg_i - K_src_i)`, the ratio

```text
E_B / E_F = sum_{i in B} Delta_i / sum_{i in F} Delta_i
```

is independent of `beta(t)`. A stronger edit therefore multiplies the foreground change
and the background perturbation by the same factor. The two cannot be controlled
independently with a scalar schedule.

## Per-token foreground--background bridge

The global schedule is replaced by a per-token rate. A foreground indicator is derived
from the trigger phrase's cross-attention response, propagated over the stream, and
merged with the target foreground mask. Foreground tokens receive a higher rate, while
background tokens keep the native rate and stay source-anchored. The background is
preserved structurally by the source branch; no explicit background anchor is needed.

## Foreground identity injection

Three mechanisms make the foreground edit decisive and temporally stable:

1. **Cross-attention value boosting** amplifies the trigger phrase's response on
   foreground tokens before value aggregation.
2. **Reference-first-frame key--value anchoring (FFKV)** appends the edited first-frame
   foreground keys and values to the target attention context, repeated a small number of
   times. The anchor is foreground-only, so the reference object, never the background,
   is the identity source.
3. **Late identity lock** raises the foreground rate in later streaming blocks when the
   edited foreground is compact, preventing source keys from pulling the identity back.

A **foreground edge guard** dilates the first-frame foreground support and takes the
union with the dynamic foreground mask, closing tokenization gaps at the object boundary.

## Identity-orthogonal motion injection

A strong edit overwrites the temporal correspondence carried by the source keys, so the
foreground can freeze or move incorrectly. The source velocity correction contains a
motion component and an appearance component. Let `Delta v = v_gt - v_src` be the source
correction and `e_hat = v_trg - v_src` the edit direction. The method removes the
edit-direction component from the low-pass-filtered correction:

```text
v_mot = LP(Delta v) - (<LP(Delta v), e_hat> / (||e_hat||^2 + eps)) * e_hat.
```

The result is orthogonal to the edit direction. It is injected into the foreground
velocity with a cosine ramp, so the source dynamics are restored without pulling the
appearance back toward the source.

## Few-step acceleration

The method uses an endpoint-preserving schedule that truncates the low-noise region and
samples the remaining range linearly. In the paper, 8 steps with terminal timestep 66
replace 15 steps to zero. The task LoRA is merged into the base weights before inference,
which removes the per-layer adapter overhead and reduces peak memory.

## Differences from streaming baselines

Streaming editors such as StreamEdit apply one global blending schedule to every token
and handle the background implicitly. RefStreamEdit separates the two regions and the two
factors: the per-token bridge decides where the reference identity acts, the foreground
modules make the edit stable, and the orthogonal motion field decides what part of the
source correction acts. The background is preserved structurally, and the method requires
no per-video optimization.
