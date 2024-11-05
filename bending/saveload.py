import math
import imageio
from PIL import Image, ImageDraw
import typing
import os


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


def make_gif(
    folder: str,
    gif_filename: typing.Optional[str] = None,
    loop: int = 0,
    boomerang: bool = True,
):
    if gif_filename is None:
        gif_filename = f"{folder}.gif"
    images = []
    frame = 0
    while os.path.isfile(f"{folder}/{frame}.png"):
        images.append(imageio.imread(f"{folder}/{frame}.png"))
        frame += 1

    images += images[::-1]

    imageio.mimsave(gif_filename, images, loop=loop)
