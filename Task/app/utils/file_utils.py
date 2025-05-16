from io import BytesIO
from app.core.config import settings
import mutagen
from PIL import Image
from typing import Optional, Tuple


def get_audio_duration(file: BytesIO) -> Optional[float]:
    try:
        audio = mutagen.File(file)
        return audio.info.length if audio else None
    except Exception:
        return None

def get_image_dimensions(file: BytesIO) -> Tuple[Optional[int], Optional[int]]:
    try:
        image = Image.open(file)
        return image.size
    except Exception:
        return None, None