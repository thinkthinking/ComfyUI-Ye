import folder_paths
from datetime import datetime
import comfy.sd
class Signature_Ye:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"text": ("STRING",{"forceInput": True})}
        }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "my_get"
    

    CATEGORY = "Ye"

    def my_get(self, text):
        # 获取当前时间
        current_time = datetime.now()
        # 格式化当前时间（可选）
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
        signature_text = f"MODEL:{text} | TIME:{formatted_time} | AUTHOR:thinkthinking | Powered By <CuteYou2>@Rui"
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
