"""
Module of color objects
"""
from PIL import Image
from PIL import ImageEnhance
from colorthief import ColorThief

from .const import Settings


class ColorThiefCustom(ColorThief):
    """
    Color extractor
    """
    def __init__(self, img):
        """
        Original __init__ uses Image.open(file) so takes only file object.
        But PIL Image needed.
        :param img:
        """
        self.image = img


class Color:
    """
    Custom color class.
    """

    def __init__(self, red, green, blue):
        self.blue = blue
        self.green = green
        self.red = red

    def tuple(self):
        """
        :return: RGB tuple (r, g, b).
        """
        return self.red, self.green, self.blue

    def __repr__(self):
        return f"<{self.red} {self.green} {self.blue}>"

    def saturated(self):
        """
        Uses ImageEnhance.Color to produce saturated version of current color.
        :return:
        """
        image = Image.new('RGB', (1, 1), self.tuple())
        filter_ = ImageEnhance.Color(image)
        new_image = filter_.enhance(Settings.SATURATION_FACTOR)
        rgb = tuple(map(lambda x: max(Settings.MIN_COLOR_VALUE, min(Settings.MAX_COLOR_VALUE, x)),
                        new_image.getpixel((0, 0))))
        new_color = Color(*rgb)
        return new_color

    def show(self):
        """
        Shows a 32x32 image filled with current color.
        :return:
        """
        image = Image.new('RGB', (32, 32), self.tuple())
        image.show()
