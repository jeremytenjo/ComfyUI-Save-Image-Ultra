import json
import os

import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo

import folder_paths
from comfy.cli_args import args


class SaveImageWithPromptToggle:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", {"tooltip": "The images to save."}),
                "filename_prefix": (
                    "STRING",
                    {
                        "default": "ComfyUI",
                        "tooltip": "The prefix for the file to save.",
                    },
                ),
                "attach_prompt_metadata": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "When enabled, writes prompt data into PNG metadata.",
                    },
                ),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "image"
    DESCRIPTION = "Saves images like the core Save Image node, with optional prompt metadata embedding."

    def save_images(
        self,
        images,
        filename_prefix="ComfyUI",
        attach_prompt_metadata=False,
        prompt=None,
        extra_pnginfo=None,
    ):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, _ = folder_paths.get_save_image_path(
            filename_prefix,
            self.output_dir,
            images[0].shape[1],
            images[0].shape[0],
        )

        results = []
        for batch_number, image in enumerate(images):
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if attach_prompt_metadata and prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for key, value in extra_pnginfo.items():
                        metadata.add_text(key, json.dumps(value))

            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            img.save(
                os.path.join(full_output_folder, file),
                pnginfo=metadata,
                compress_level=self.compress_level,
            )

            results.append(
                {
                    "filename": file,
                    "subfolder": subfolder,
                    "type": self.type,
                }
            )
            counter += 1

        return {"ui": {"images": results}}


NODE_CLASS_MAPPINGS = {
    "SaveImageWithPromptToggle": SaveImageWithPromptToggle,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImageWithPromptToggle": "Save Image Ultra",
}
