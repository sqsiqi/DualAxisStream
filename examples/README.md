# Example inputs

Place a source video and a reference image here, for example:

```text
examples/source.mp4
examples/reference.png
```

Run:

```bash
bash scripts/run_demo.sh \
  --source examples/source.mp4 \
  --reference examples/reference.png \
  --prompt "Change the city bus to a double-decker bus." \
  --output outputs/edited.mp4
```

Use `--check` to validate the inputs and print the paper configuration without calling
the core hook:

```bash
bash scripts/run_demo.sh --check \
  --source examples/source.mp4 \
  --reference examples/reference.png \
  --prompt "Change the city bus to a double-decker bus."
```
