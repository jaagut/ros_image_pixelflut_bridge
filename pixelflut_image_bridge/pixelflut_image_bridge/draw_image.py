import telnetlib

from PIL import Image


class Sender:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def send_image(self, image: Image.Image):
        draw_image(self.host, self.port, image)


def draw_image(host: str, port: int, image: Image.Image):
    """Draws an image on the matrixflut
    Based on: https://github.com/mythsunwind/matrixflut-client

    :param host: The host of the matrixflut
    :param port: The port of the matrixflut
    :param image: The image to draw
    """
    pixel = image.load()
    width, height = image.size
    telnet = telnetlib.Telnet(host, port)
    for x in range(width):
        for y in range(height):
            telnet.write(f"PX {x} {y} {'{:02x}{:02x}{:02x}'.format(*pixel[x, y])}\n".encode("ascii"))
    telnet.close()
