import math
import typing
from PIL import Image
from bending.images import make_frame, sample_image
from bending.file_io import save_frames


def animate_mobius(
    filename: str,
    nframes: int = 15,
    width: typing.Optional[int] = None,
    height: typing.Optional[int] = None,
    folder: typing.Optional[str] = None,
    output_width: typing.Optional[int] = None,
    output_height: typing.Optional[int] = None,
    lighten: bool = False,
):
    if folder is None:
        folder = ".".join(filename.split(".")[:-1])
    img = Image.open(filename).convert("RGB")

    if width is None and height is None:
        width = 600
    if width is None:
        assert height is not None
        width = math.floor(img.size[0] * height / img.size[1])
    if height is None:
        assert width is not None
        height = math.floor(img.size[1] * width / img.size[0])

    small = img.resize((width, height), resample=Image.BILINEAR)
    img_data = sample_image(small)

    frames = [make_frame(img_data, lambda x, y: (x, 0, y), lighten=lighten)]

    for t in range(1, nframes + 1):
        print(f"Making {folder} frame {t}")
        radius = width / 2 / math.pi * nframes / t
        start = math.pi / 6

        def mobius_f(x, y):
            angle = x / radius
            if angle < start:
                return (
                    radius * math.sin(x / radius),
                    radius * (1 - math.cos(x / radius)),
                    y,
                )
            elif angle < start + math.pi / 2:
                angle2 = 2 * (angle - start)
                radius2 = radius + (height / 2 - y) * math.sin(angle2) / 2 / math.pi
                return (
                    radius2 * math.sin(x / radius),
                    radius2 * (1 - math.cos(x / radius)),
                    height / 2 + (y - height / 2) * math.cos(angle2),
                )
            else:
                return (
                    radius * math.sin(x / radius),
                    radius * (1 - math.cos(x / radius)),
                    height - y,
                )

        frames.append(
            make_frame(img_data, mobius_f, lighten=lighten)
        )

    save_frames(frames, folder, output_width=output_width, output_height=output_height)
