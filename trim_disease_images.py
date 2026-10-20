"""Remove only the white seams from the current treatment image crops.

The originals stay untouched. Coordinates were checked against the existing
323 x 323 generated-disease images, including the adjacent-image seams.
"""

from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parent / "assets" / "optimized"
CROPS = {
    1: (0, 0, 316, 316),
    3: (7, 0, 322, 316),
    4: (7, 0, 323, 316),
    5: (14, 0, 323, 316),
    6: (0, 0, 317, 307),
    7: (4, 0, 322, 307),
    8: (7, 0, 322, 307),
    10: (15, 0, 323, 307),
    11: (0, 0, 317, 323),
    12: (4, 0, 322, 323),
    13: (7, 0, 322, 323),
    14: (7, 0, 323, 323),
    15: (15, 0, 323, 323),
}


for number, bounds in CROPS.items():
    source = ROOT / f"generated-disease-{number}.png"
    target = ROOT / f"generated-disease-{number}-trim.png"
    with Image.open(source) as image:
        if image.size != (323, 323):
            raise ValueError(f"Unexpected size for {source.name}: {image.size}")
        image.crop(bounds).save(target, optimize=True)
    print(f"{source.name} -> {target.name}: {bounds}")
