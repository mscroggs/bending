import math
import typing
from PIL import Image
from bending.images import make_frame, sample_image
from bending.file_io import save_frames


def animate_klein_bottle(
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
        frames.append(
            make_frame(
                img_data,
                lambda x, y: (
                    radius * math.sin(x / radius),
                    radius * (1 - math.cos(x / radius)),
                    y,
                ),
                lighten=lighten,
            )
        )

    for t in range(1, nframes + 1):
        print(f"Making {folder} frame {nframes + t}")
        scale = nframes / t

        def klein_pt(x, y):
            scaled_y = y / height / scale * (4 + 2 * math.pi)
            centre = None
            big_r = height * scale / (4 + 2 * math.pi)
            small_r_bounds = [3 * width / 10 / math.pi, width / 2 / math.pi]
            small_r = small_r_bounds[1]
            if scaled_y < 2:
                centre = (0, y)
                y_dir = (1, 0)
            elif scaled_y < 2 + 3 * math.pi / 2:
                angle = scaled_y - 2
                centre = (
                    -big_r * (1 - math.cos(angle)),
                    2 * big_r + big_r * math.sin(angle),
                )
                y_dir = (math.cos(angle), math.sin(angle))
                if angle > math.pi:
                    small_r = small_r_bounds[1] + (angle - math.pi) / (0.5 * math.pi) * (
                        small_r_bounds[0] - small_r_bounds[1]
                    )
            elif scaled_y < 2 + 2 * math.pi:
                angle = scaled_y - 2 - 3 * math.pi / 2
                centre = (
                    -big_r + big_r * math.sin(angle),
                    big_r * math.cos(angle),
                )
                y_dir = (-math.sin(angle), -math.cos(angle))
                small_r = small_r_bounds[0]
            else:
                scaled_y2 = scaled_y - 2 - 2 * math.pi
                y2 = scaled_y2 * height * scale / (4 + 2 * math.pi)
                if scaled_y2 < 1:
                    centre = (0, -y2)
                else:
                    centre = (0, y2 - 2 * height * scale / (4 + 2 * math.pi))
                y_dir = (-1, 0)
                small_r = small_r_bounds[0] + math.sin(
                    math.pi * scaled_y2 / 4
                ) ** 2 * (small_r_bounds[1] - small_r_bounds[0])

            y_offset = -small_r * math.cos(x * 2 * math.pi / width)
            return (
                small_r * math.sin(x * 2 * math.pi / width),
                width / 2 / math.pi + centre[0] + y_offset * y_dir[0],
                centre[1] + y_offset * y_dir[1],
            )

        frames.append(make_frame(img_data, klein_pt, lighten=lighten))

    save_frames(frames, folder, output_width=output_width, output_height=output_height)
