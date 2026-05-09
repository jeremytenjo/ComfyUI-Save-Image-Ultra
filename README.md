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
