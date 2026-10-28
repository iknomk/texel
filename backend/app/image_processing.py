"""удаление фона с ограниченным расходом оперативной памяти."""

from functools import lru_cache
from pathlib import Path
from threading import Lock

import onnxruntime as ort
from PIL import Image, ImageOps
from rembg import new_session, remove


_processing_lock = Lock()


@lru_cache(maxsize=1)
def _background_session():
    options = ort.SessionOptions()
    options.intra_op_num_threads = 1
    options.inter_op_num_threads = 1
    options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
    options.enable_cpu_mem_arena = False
    options.enable_mem_pattern = False
    return new_session("u2netp", sess_opts=options, providers=["CPUExecutionProvider"])


def prepare_foreground(source: Path, destination: Path):
    # bound both decoding/inference work and session creation to one photo.
    with _processing_lock:
        with Image.open(source) as original:
            # jpeg draft reduces decoding memory before loading large photos.
            original.draft("RGB", (1024, 1024))
            image = ImageOps.exif_transpose(original)
            image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
            image = image.convert("RGB")
        result = remove(image, session=_background_session())
        result.convert("RGBA").save(destination, format="PNG")
