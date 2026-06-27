# DOE V10 PyTorch install helper.
# Paste this into a notebook code cell, run it once, restart the kernel,
# then rerun V10 so the Chong ANN section can import torch.
#
# Important: the PyTorch package name is "torch", not "pytorch".
# Official install selector: https://pytorch.org/get-started/locally/

import subprocess
import sys


CPU_INDEX_URL = "https://download.pytorch.org/whl/cpu"


def run(command):
    print("\n$", " ".join(command))
    subprocess.check_call(command)


print("Python executable:", sys.executable)
print("Python version:", sys.version)

# Remove the placeholder/wrong package name if it was attempted.
run([sys.executable, "-m", "pip", "uninstall", "-y", "pytorch"])

# Install CPU PyTorch into this exact notebook/kernel environment.
run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
run([sys.executable, "-m", "pip", "install", "torch", "--index-url", CPU_INDEX_URL])

import torch

print("torch version:", torch.__version__)
print("test tensor:")
print(torch.rand(2, 3))
print("cuda available:", torch.cuda.is_available())
print("\nRestart the notebook kernel, then rerun V10.")
