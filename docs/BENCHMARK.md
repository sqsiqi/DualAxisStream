# Benchmark and evaluation protocol

## Ref-Five-Bench-A

Ref-Five-Bench-A reuses the 100 source videos of
[FiVE-Bench](https://github.com/MinghanLi/FiVE-Bench) together with their paired object
masks and replacement prompts. For each source, a 1024 x 1024 reference image of the
target object is generated with Z-Image, and an edited first frame is generated with
DreamOmni2. The edit is restricted to the mask, and the edited first frame is stored as
the reference condition.

## Ref-Five-Bench-B

Ref-Five-Bench-B contains 148 videos:

- 98 FiVE-Bench sources with every replacement target re-authored (near-category
  substitutions such as cat to tiger), so prompts and references differ from A.
- 25 gameplay clips from `gaming-500-hours`, recorded at 1080p and cropped to 5 seconds
  at 864 x 480.
- 25 product clips from LoVoRA/MSRVTT, covering apparel, accessories, eyewear, kitchenware,
  and food.

For the new clips, reference images are rendered with Z-Image-Turbo on a white background,
foreground masks are obtained per frame with GroundingDINO and SAM2, and the edited first
frame is produced by FLUX.1-Fill-dev with Insert-Anything and Redux conditioning. All
videos are 864 x 480, 16 fps, H.264, and silent. Prompts follow the 13-field FiVE schema.

## Metrics

Nine metrics are grouped into four families.

| Family | Metric | Direction | Definition |
| --- | --- | --- | --- |
| Foreground | FG DreamSim | lower | DreamSim distance between the edited foreground and the reference first frame |
| Foreground | CLIP | higher | CLIP similarity between the edited foreground and the target prompt |
| Motion | mEPE | lower | RAFT end-point error in the foreground, normalized by the mean source-flow magnitude |
| Background | BG-LPIPS | lower | LPIPS between the edited and source background |
| Background | BG-DINO | lower | DINOv2 feature distance on the background |
| Background | BG-SSIM | higher | SSIM on the background |
| Background | BG-PSNR | higher | PSNR on the background |
| Consistency | Coverage@0.30 | higher | Fraction of videos with FG DreamSim below 0.30 |
| Consistency | TC | lower | Foreground LPIPS between the source-flow-warped current frame and the next frame, minus the same quantity for the source |

All metrics use 16 uniformly sampled frames per video. The main comparison uses all 100
videos of A and all 148 videos of B. The ablation and parameter-sensitivity studies use a
fixed development split of each benchmark.

## Baselines

The paper compares with ten methods: StreamEdit, AnyV2V, I2VEdit, Kiwi-Edit, LoRAEdit,
NovaEdit, Rerender, VACE, JoyAI-Video-Edit, and ReCo_ref. All methods use their default
configurations unless noted.

## Notes

- No ground-truth mask, flow, or velocity is used at inference.
- The main comparison and the multimodal-LLM study average over all videos for which
  every method yields valid measurements.
- The ablation and sensitivity studies use a fixed development split, not the test set.
