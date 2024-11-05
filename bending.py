import imageio
import os
import math
import typing
from PIL import Image, ImageDraw

X = (math.sqrt(2), 0.5)
Y = (math.sqrt(2), -0.5)
Z = (0, 1)


def make_frame(
    img,
    f,
) -> typing.List[typing.Tuple[typing.Tuple[float, ...], typing.Tuple[int, int, int, int]]]:
    width, height = img.size
    polygons = []
    for i in range(width):
        for j in range(height):
            pts = ()
            for pt in [(i,j),(i+1,j),(i+1,j+1),(i,j+1)]:
                x, y, z = f(*pt)
                pts += (
                    X[0] * x + Y[0] * y + Z[0] * z,
                    X[1] * x + Y[1] * y + Z[1] * z,
                )
            polygons.append(((x, y, z), pts, img.getpixel((i, j))))

    polygons.sort(key = lambda x: x[0][0] - x[0][1] + x[0][2])

    return [i[1:] for i in polygons]


def save_frames(
    frames: typing.List[typing.Tuple[typing.Tuple[float, ...], typing.Tuple[int, int, int, int]]],
    folder: str,
    bg: str = "#FFFFFF",
    output_width: typing.Optional[int] = None,
    output_height: typing.Optional[int] = None,
):
    if not os.path.isdir(folder):
        os.system(f"mkdir {folder}")
    if os.path.isfile(f"{folder}/0.png"):
        os.system(f"rm {folder}/*.png")

    xmin = math.floor(min(min(min(pts[::2]) for pts, _ in polygons) for polygons in frames))
    xmax = math.ceil(max(max(max(pts[::2]) for pts, _ in polygons) for polygons in frames))
    ymin = math.floor(min(min(min(pts[1::2]) for pts, _ in polygons) for polygons in frames))
    ymax = math.ceil(max(max(max(pts[1::2]) for pts, _ in polygons) for polygons in frames))

    scale = 1
    if output_width is not None:
        scale = min(scale, output_width / (xmax - xmin))
    if output_height is not None:
        scale = min(scale, output_height / (ymax - ymin))

    size = (math.ceil(scale * (xmax - xmin)), math.ceil(scale * (ymax - ymin)))
    for frame_n, polygons in enumerate(frames):
        frame = Image.new("RGB", size, bg)
        draw = ImageDraw.Draw(frame)

        for pts, color in polygons:
            draw.polygon(tuple(
                scale * (j - (xmin if i % 2 == 0 else ymin))
                for i, j in enumerate(pts)
            ), color)

        frame.save(f"{folder}/{frame_n}.png")


def animate_cylinder(
    filename: str,
    direction: str = "vertical",
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
        if direction == "horizontal":
            radius = height / 2 / math.pi * nframes / t
            frames.append(make_frame(small, lambda x, y: (
                x,
                radius * (1 - math.cos(y / radius)),
                radius * math.sin(y / radius),
            )))
        elif direction == "vertical":
            radius = width / 2 / math.pi * nframes / t
            frames.append(make_frame(small, lambda x, y: (
                radius * math.sin(x / radius),
                radius * (1 - math.cos(x / radius)),
                y,
            )))
        else:
            raise ValueError(f"Unsupported direction: {direction}")

    save_frames(frames, folder, output_width=output_width, output_height=output_height)


def make_gif(
    folder: str,
    gif_filename: typing.Optional[str] = None
    loop: int = 0
):
    if gif_filename is None:
        gif_filename = f"{folder}.gif"
    images = []
    frame = 0
    while os.path.isfile(f"{folder}/{frame}.png"):
        images.append(imageio.imread(f"{folder}/{frame}.png"))
        frame += 1
    print(folder, frame)
    imageio.mimsave(gif_filename, images, loop=loop)
