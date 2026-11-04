# Tesseract projects

[Tesseract by Mirage](https://github.com/mirage-hq/Tesseract) renders editable `.tsrct` projects locally: motion graphics,
footage edits, static designs and Scene3D scenes. Each project here keeps its editable document, its source assets and the
render made from it together, so the next revision starts from the real project, not from a video.

The CLI and the skills are **not** committed (the Tesseract terms forbid redistributing them). Reinstall them in a fresh
cloud container with the steps below; everything else in this folder is our own output.

## Setup in a fresh container (Linux x86_64)

1. Skills (official installer, user level, for Claude Code):

   ```bash
   npx -y skills@latest add mirage-hq/Tesseract -g -a claude-code -s tesseract-3d tesseract-design tesseract-motion tesseract-video -y --copy
   ```

2. CLI, pinned by the skills (`cli-version.txt`, 0.5.0 when this was written), checksum verified before installing:

   ```bash
   V=$(cat ~/.claude/skills/tesseract-motion/references/cli-version.txt); D=$(mktemp -d); cd "$D"; B=https://github.com/mirage-hq/tesseract/releases/download/v$V; curl -fL -O "$B/tesseract-$V-linux-x86_64.zip" -O "$B/tesseract-$V-linux-x86_64.zip.sha256" && sha256sum -c "tesseract-$V-linux-x86_64.zip.sha256" && unzip -q "tesseract-$V-linux-x86_64.zip" -d x && bash "x/tesseract-$V-linux-x86_64/install.sh" && ~/.local/share/Tesseract/bin/tsrct --version
   ```

3. A Vulkan driver (the container has the loader but no driver; Mesa lavapipe renders on the CPU):

   ```bash
   apt-get install -y --no-install-recommends mesa-vulkan-drivers
   ```

The command is `~/.local/share/Tesseract/bin/tsrct`. Checked on 2026-11-04: zip SHA-256
`4b77a2f163247ef6215e879a582a7ecd37b98118ea3f63af26057ec0907668c4`, `tsrct 0.5.0 (ac63ae1)`, skills from commit `0889725`.

## What works here, and the limits

- **H.264 export needs the system FFmpeg.** The Linux bundle has no H.264 encoder. Add
  `--encoder-backend external-ffmpeg-command --ffmpeg-path /usr/bin/ffmpeg` to every MP4 export.
- **Everything renders on the CPU.** These timings were measured while another render was using the machine:
  - a 2D still at 1080×1920 takes about 1 s;
  - a 2D export runs at about 0.08 s per frame;
  - a Scene3D raster frame at 1080×1920 takes 55-75 s, shader compilation included;
  - a path tracer frame at 270×480 (16 samples) takes about 36 s.

  Plan 3D renders accordingly.
- **The path tracer's denoiser cannot download here.** The CLI does not use the container's HTTPS proxy (it fails with a DNS error
  on `captions-cdn.xyz`). Use `--no-denoise` with more samples, or make denoised path-traced finals on a machine with direct
  network access.
- **Telemetry is on by default.** The CLI sends anonymous usage events for project create, preview, filmstrip and export: no
  content, paths or prompts. `tsrct telemetry disable` turns it off.

## Project layout

One folder per project, numbered:

```text
NN-name/
  Name.tsrct          editable document (packages its fonts, images, footage and audio)
  Name.mp4            the render of the current revision
  Previews/           filmstrips and stills worth keeping
  sources/            original assets as supplied (brand files, footage, music), with their licence or origin
  .tesseract-work/    action batches and notes; schema dumps and frame dumps are not committed
```

Commit only fonts and media whose licence allows sharing them inside the repository: a `.tsrct` embeds them. Inter (OFL) is
fine.

## Projects

- `00-install-check/`: the installation check. It has a 3-second 2D motion test (slide-in card, Inter Bold title, procedural
  spinner, H.264 export) and a two-box Scene3D test rendered with both the raster renderer and the path tracer.
