from PIL import Image, ImageEnhance
from datetime import datetime
from random import choice


def to_bytes(pixels: list[list[tuple[int, int, int, int]]]):
    return bytes(yield_channels(pixels))


def yield_channels(pixels: list[list[tuple[int, int, int, int]]]):
    for row in pixels:
        for pixel in row:
            yield from pixel


def generate_image(*frame_pixels):
    frames = []
    size = len(frame_pixels[0])
    repl_size = int(320)
    repl_gutter = int(110)
    repl_image = Image.open("repl_bold.png").resize((repl_size,) * 2)
    repl = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    repl.paste(
        repl_image,
        (repl_gutter, repl_gutter, repl_gutter + repl_size, repl_gutter + repl_size),
        repl_image,
    )
    for pixels in frame_pixels:
        frame = Image.new("RGB", (size, size))
        layer = Image.frombytes("RGB", (size, size), to_bytes(pixels))
        frame.paste(layer, (0, 0))
        frame.paste(repl, (size - repl_size - repl_gutter * 2, 0), repl)
        frame = frame.crop((0, 0, 960, 540))
        frames.append(frame)

    date = (
        datetime.utcnow()
        .isoformat(sep="-")
        .replace("/", "")
        .replace(":", "")
        .split(".")[0]
    )
    frames[0].show()
    file_name = f"images/{date}-cover.png"
    with open(file_name, "wb") as image_file:
        frames[0].save(
            image_file,
            save_all=True,
            append_images=frames[1:],
            duration=0.1,
            loop=0,
            disposal=0,
        )
    print("Saved to", file_name)


def create_image(size, width):
    frames = []
    num_frames = 1
    dimension = width // size
    offsets = []
    for _ in range(dimension):
        options = [
            i
            for i in range(0, width // size)
            if not offsets
            or all(abs(i - o) > 3 - n for n, o in enumerate(offsets[-3:]))
        ]
        chose = choice(options)
        offsets.append(chose)
    for frame in range(num_frames):
        pixels = [[(0, 0, 0) for _ in range(width)] for _ in range(width)]
        bands = (
            (235, 50, 35),  # Red
            (243, 167, 59),  # Orange
            (255, 253, 84),  # Yellow
            (55, 125, 34),  # Green
            (0, 38, 245),  # Blue
            (117, 27, 124),  # Purple
        )
        for row in range(dimension):
            for column in range(dimension):
                band = int(column / (dimension / len(bands)))
                offset = int(row - offsets[column] - frame) % dimension
                r, g, b = bands[band]

                lum = offset / dimension
                if lum > 0.95:
                    lum = 1.5
                else:
                    lum = lum / 2 + 0.5
                r = min(255, int(r * lum))
                g = min(255, int(g * lum))
                b = min(255, int(b * lum))

                for i in range(0, size):
                    for j in range(0, size):
                        y = int(row * size + i) % width
                        x = int(column * size + j) % width
                        pixels[-y][x] = (r, g, b)

        frames.append(pixels)

    generate_image(*frames)


if __name__ == "__main__":
    create_image(30, 960)
