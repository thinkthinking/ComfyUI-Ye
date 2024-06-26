from .nodes.basic import *

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Signature|Ye": Signature_Ye,
    "CheckpointLoader|Ye": CheckpointLoader_Ye,
    "PrintHelloWorld|Ye": PrintHelloWorld_Ye,
    "OllamaVision|Ye": OllamaVision
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Signature|Ye": "Signature",
    "CheckpointLoader|Ye": "Checkpoint Loader",
    "PrintHelloWorld|Ye": "Print Hello World",
    "OllamaVision|Ye": "Ollama Vision"
}

print("\033[34mComfyUI-Ye Nodes: \033[92mLoaded\033[0m")