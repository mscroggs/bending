import math
import typing
from PIL import Image
from bending.core import make_frame
from bending.saveload import save_frames


def animate_torus(
    filename: str,
    nframes: int = 15,
    width: typing.Optional[int] = None,
    height: typing.Optional[int] = None,
    folder: typing.Optional[str] = None,
    output_width: typing.Optional[int] = None,
    output_height: typing.Optional[int] = None,
):
    if folder is None:
        folder = ".".join(filename.split(".")[:-1])
    img = Image.open(filename).convert("RGB")

    if width is None and height is None:
        width = 600
    if width is None:
        width = math.floor(img.size[0] * height / img.size[1])
    if height is None:
        height = math.floor(img.size[1] * width / img.size[0])

    small = img.resize((width, height), resample=Image.BILINEAR)
    small.save("test.png")

    frames = [make_frame(small, lambda x, y: (x, 0, y))]

    for t in range(1, nframes + 1):
        print(f"Making {folder} frame {t}")
        radius = width / 2 / math.pi * nframes / t
        frames.append(make_frame(small, lambda x, y: (
            radius * math.sin(x / radius),
            radius * (1 - math.cos(x / radius)),
            y,
        )))
    for t in range(1, nframes + 1):
        print(f"Making {folder} frame {nframes + t}")
        radius = height / 2 / math.pi * nframes / t
        origin = -radius
        frames.append(make_frame(small, lambda x, y: (
            width / 2 / math.pi * math.sin(x * 2 * math.pi / width),
            origin + (radius + width / 2 / math.pi * (1 - math.cos(x * 2 * math.pi / width))) * math.cos(y / radius),
            (radius + width / 2 / math.pi * (1 - math.cos(x * 2 * math.pi / width))) * math.sin(y / radius),
        )))

    save_frames(frames, folder, output_width=output_width, output_height=output_height)
