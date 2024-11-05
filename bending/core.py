import typing
import math

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
            for pt in [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]:
                x, y, z = f(*pt)
                pts += (
                    X[0] * x + Y[0] * y + Z[0] * z,
                    X[1] * x + Y[1] * y + Z[1] * z,
                )
            polygons.append(((x, y, z), pts, img.getpixel((i, j))))

    polygons.sort(key=lambda x: x[0][0] - x[0][1] + x[0][2])

    return [i[1:] for i in polygons]
