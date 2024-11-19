from PIL.Image import Image
import typing
import math

X = (math.sqrt(2), 0.5)
Y = (math.sqrt(2), -0.5)
Z = (0.0, 1.0)


def sample_image(
    img: Image,
) -> typing.List[typing.Tuple[typing.Tuple[int, int], typing.Tuple[int, int, int]]]:
    out = []
    width, height = img.size
    for i in range(width):
        for j in range(height):
            c = img.getpixel((i, j))
            out.append(((i, j), (c[0], c[1], c[2])))
    return out


def make_frame(
    img_data: typing.List[typing.Tuple[typing.Tuple[int, int], typing.Tuple[int, int, int]]],
    f: typing.Callable[[float, float], typing.Tuple[float, float, float]],
    lighten: bool = False,
) -> typing.List[typing.Tuple[typing.Tuple[float, ...], typing.Tuple[int, int, int, int]]]:
    polygons = []
    for ((i, j), c) in img_data:
        pts: typing.Tuple[float, ...] = ()
        for pt in [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]:
            x, y, z = f(*pt)
            pts += (
                X[0] * x + Y[0] * y + Z[0] * z,
                X[1] * x + Y[1] * y + Z[1] * z,
            )
        if lighten:
            color = (
                max(0, min(255, c[0] + min(120, max(0, int(y) // 3 + 66)))),
                max(0, min(255, c[1] + min(120, max(0, int(y) // 3 + 66)))),
                max(0, min(255, c[2] + min(120, max(0, int(y) // 3 + 66)))),
                255,
            )
        else:
            color = (c[0], c[1], c[2], 255)
        polygons.append(((x, y, z), pts, color))

    polygons.sort(key=lambda x: x[0][0] - x[0][1] + x[0][2])

    return [i[1:] for i in polygons]
