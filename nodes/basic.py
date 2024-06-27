import folder_paths
from datetime import datetime
import comfy.sd
import random

from ollama import Client
from PIL import Image
import numpy as np
import base64
from io import BytesIO
import json
import re

class Signature_Ye:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"model": ("STRING",{"forceInput": True}),"author": ("STRING",{"forceInput": True}),"copyright": ("STRING",{"forceInput": True})}
        }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "my_get"
    

    CATEGORY = "Ye"

    def my_get(self, model,author,copyright):
        # 获取当前时间
        current_time = datetime.now()
        # 格式化当前时间（可选）
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
        signature_text = f"MODEL:{model} | TIME:{formatted_time} | AUTHOR:{author} | Powered By {copyright}"
        return {"result": (signature_text,),}

    """
        The node will always be re executed if any of the inputs change but
        this method can be used to force the node to execute again even when the inputs don't change.
        You can make this node return a number or a string. This value will be compared to the one returned the last time the node was
        executed, if it is different the node will be executed again.
        This method is used in the core repo for the LoadImage node where they return the image hash as a string, if the image hash
        changes between executions the LoadImage node is executed again.
    """

class CheckpointLoader_Ye:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "ckpt_name": (folder_paths.get_filename_list("checkpoints"), ),
                             }}
    RETURN_TYPES = ("MODEL", "CLIP", "VAE","STRING")
    FUNCTION = "load_checkpoint"

    CATEGORY = "Ye"

    def load_checkpoint(self, ckpt_name):
        print(ckpt_name)
        ckpt_path = folder_paths.get_full_path("checkpoints", ckpt_name)
        out = comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=True, output_clip=True, embedding_directory=folder_paths.get_folder_paths("embeddings"))
        result = list(out[:3])+[ckpt_name]
        return result


class PrintHelloWorld_Ye:     

    @classmethod
    def INPUT_TYPES(cls):
               
        return {"required": {       
                    "text": ("STRING", {"multiline": False, "default": "Hello World"}),
                    }
                }

    RETURN_TYPES = ()
    FUNCTION = "print_text"
    OUTPUT_NODE = True
    CATEGORY = "Ye"

    def print_text(self, text):

        print(f"Tutorial Text : {text}")
        
        return {}

prompt_template = {
  "description": "",
  "long_prompt": "",
  "camera_angle_word": "",
  "style_words": "",
  "subject_words": "",
  "light_words": "",
  "environment_words": ""
}


class OllamaVision:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "query": ("STRING", {
                    "multiline": True,
                    "default": "describe the image"
                }),
                "debug": (["enable", "disable"],),
                "url": ("STRING", {
                    "multiline": False,
                    "default": "http://127.0.0.1:11434"
                }),
                "model": (["llava-llama3:latest", "llava-phi3:latest", "llava:latest"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "keep_alive": (["0", "60m"],),
                
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("description",)
    FUNCTION = "ollama_vision"
    CATEGORY = "Ollama"

    def ollama_vision(self, images, query,seed, debug, url, keep_alive, model):
        images_b64 = []

        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_bytes = base64.b64encode(buffered.getvalue())
            images_b64.append(str(img_bytes, 'utf-8'))

        client = Client(host=url)
        options = {
            "seed": seed,
        }

        if debug == "enable":
            print(f"""[Ollama Vision] 
request query params:

- query: {query}
- url: {url}
- model: {model}
- options: {options}
- keep_alive: {keep_alive}

""")

        response = client.generate(model=model, prompt=query, keep_alive=keep_alive, options=options, images=images_b64)



        return (response['response'],)
