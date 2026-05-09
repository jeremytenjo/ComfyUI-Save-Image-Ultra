# ComfyUI Save Image Ultra

Custom ComfyUI output node that mirrors core `Save Image` behavior and adds a boolean toggle (Ultra edition):

- `attach_prompt_metadata` (default: `false`)

When enabled, the node writes `prompt` into PNG metadata. When disabled, prompt metadata is not embedded.

## Install

1. Copy/clone this folder into `ComfyUI/custom_nodes/`
2. Restart ComfyUI

## Node

- Display name: `Save Image Ultra`
- Category: `image`
- Inputs:
  - `images` (`IMAGE`)
  - `filename_prefix` (`STRING`)
  - `attach_prompt_metadata` (`BOOLEAN`, default `false`)

`extra_pnginfo` metadata is still preserved when ComfyUI metadata is enabled.

## View Metadata

If `attach_prompt_metadata` is enabled, the output PNG will include a `prompt` text chunk.

You can inspect PNG metadata with any of these methods:

- macOS/Linux (`exiftool`):

```bash
exiftool -a -G1 -s output.png
```

- Node.js (`png-chunks-extract` + `png-chunk-text`):

```bash
npm i png-chunks-extract png-chunk-text
node -e 'const fs=require("fs");const extract=require("png-chunks-extract");const text=require("png-chunk-text");const chunks=extract(fs.readFileSync("output.png"));for(const c of chunks){if(c.name==="tEXt"){const d=text.decode(c.data);console.log(d.keyword+":", d.text)}}'
```

- ComfyUI workflow tools that read PNG text chunks (many "Load/Info" nodes expose these fields).
