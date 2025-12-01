# 1. Chose architecture
# Decided to use local faster-whisper with GPU (no API).

# 2. Installed Python 3.10.x
# - Downloaded from python.org (not Microsoft Store)
# - Checked "Add Python to PATH"
# - Did NOT enable debug symbols or debug binaries

# 3. Disabled Microsoft Store Python redirects
# Settings → Apps → Advanced app settings → App execution aliases
# Turned OFF: python.exe and python3.exe

# 4. Verified Python & pip work
python --version
pip --version

# 5. Checked NVIDIA GPU detection
nvidia-smi   # Confirmed RTX 5060 Laptop GPU and drivers

# 6. Verified CUDA Toolkit installation
nvcc --version   # CUDA 13.0 installed (acceptable)

# 7. Installed PyTorch with CUDA 12.1 runtime
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 8. Tested PyTorch GPU availability using Temprary.py
# - CUDA available: TRUE
# - GPU detected
# - Warning about GPU being too new (expected, not a problem)

# 9. Installed faster-whisper
pip install faster-whisper
# Installed components: ctranslate2, onnxruntime, av, tokenizers, tqdm, huggingface-hub, etc.
