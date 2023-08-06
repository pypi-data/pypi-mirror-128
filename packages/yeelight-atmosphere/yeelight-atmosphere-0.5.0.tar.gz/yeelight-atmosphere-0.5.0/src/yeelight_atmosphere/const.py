"""
Module for singleton class Settings.
"""


class Settings:
    """
    Settings singleton
    """
    # Strategies of selecting screen parts.
    CENTER_STRATEGY = 0
    BORDERS_STRATEGY = 1
    ALL_SCREEN_STRATEGY = 2

    # Queue of colors size.
    # Affects how smoothly the color of the light bulb changes when the dominant color changes.
    # The higher the value, the slower the transition.
    QUEUE_SIZE_CONST = 25

    # Saturation coefficient. If the scene is faded, saturation allows to choose the close color.
    # The higher the value, the quicker the transition.
    SATURATION_FACTOR = 7

    # Limits for RGB components.
    # To prevent toxic not balanced colors like (250, 0, 0)
    MAX_COLOR_VALUE = 180
    MIN_COLOR_VALUE = 30

    # TTL of screenshot
    SCREENSHOT_TTL = 30

    # Debugging section

    # Shows the picture of colors in queue.
    SHOW_COLORS_QUEUE = False
