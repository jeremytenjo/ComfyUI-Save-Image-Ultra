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

## Metadata Structure

This node writes PNG text chunks (`tEXt`) using ComfyUI's standard behavior.

When `attach_prompt_metadata = true`:

- `prompt`: JSON string of the full ComfyUI `PROMPT` object.
- `<extra_pnginfo key>`: JSON string value for each key in `extra_pnginfo`.

When `attach_prompt_metadata = false`:

- `prompt`: not written.
- `<extra_pnginfo key>`: still written (same as core Save Image behavior).

Example shape of saved text entries:

```json
{
  "prompt": "{\"6\":{\"class_type\":\"KSampler\",\"inputs\":{...}},\"7\":{...}}",
  "workflow": "{\"last_node_id\":42,\"last_link_id\":108,...}",
  "other_key": "{\"any\":\"json-serializable value\"}"
}
```

Notes:

- Values are stored as JSON-encoded strings, not nested PNG binary objects.
- If ComfyUI is started with metadata disabled (for example `--disable-metadata`), no PNG text metadata is written.

## View Metadata

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
