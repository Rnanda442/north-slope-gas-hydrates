# DOE V10 Install Torch Code Block

Use this if the V10 share packet says the Chong ANN block failed with
`No module named 'torch'`.

Do not run `pip install pytorch`. That package name is a placeholder/error
package. The actual PyTorch package is `torch`.

## Anaconda Prompt

Run this in the same Anaconda Prompt/environment used by VS Code/Jupyter:

```powershell
python -m pip uninstall -y pytorch
python -m pip install --upgrade pip
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -c "import torch; print(torch.__version__); print(torch.rand(2,3)); print('cuda:', torch.cuda.is_available())"
```

Then restart the notebook kernel and rerun V10.

## Notebook Cell Alternative

If you are not sure which Python environment the notebook is using, paste the
contents of this file into a new notebook code cell and run it once:

```text
DOE_V10_INSTALL_TORCH_CODE_BLOCK.py
```

That helper uses `sys.executable`, so it installs into the exact notebook kernel
environment.

Official source: https://pytorch.org/get-started/locally/
