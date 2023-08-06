"""
Module for bulbs of different type.
"""
import logging
import os
import time
from collections import deque
from pathlib import Path

import yeelight
from PIL import Image, ImageDraw
from sqlalchemy import Column, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from yeelight import Bulb as BulbYee, BulbException

from .color import Color
from .const import Settings
from .exception import BulbConnectionLostException
from .generator import ColorGenerator

# Declaring of local sqlite to storage list of used bulbs.

HOME = str(Path.home())
db_path = os.path.join(HOME, 'local.db')
engine = create_engine('sqlite:///' + db_path)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Bulb(Base):
    """
    Base class of bulb.
    """
    __tablename__ = 'bulb'

    id = Column(String, primary_key=True)
    model = Column(String)
    name = Column(String)
    last_ip = Column(String)
    last_usage = Column(DateTime)
    bulb_obj_ = None
    colors_queue = deque()
    default_effect = "smooth"

    @property
    def queue_size(self):
        """
        :return: Queue size from settings
        """
        return Settings.QUEUE_SIZE_CONST

    @property
    def bulb_obj(self):
        """
        :return: Bulb object (if exists), if not creates and returns it
        """
        if self.bulb_obj_ is None:
            self.init_obj()
        return self.bulb_obj_

    def init_obj(self, ip_address: str = None, effect: str = None) -> BulbYee:
        """
        :param ip_address: IP address of bulb in local network.
        :param effect: Effect of changing color. Can be "smooth" or "sudden".
        :return:
        """
        ip_address = ip_address if ip_address else self.last_ip
        effect = effect if effect else self.default_effect

        for _ in range(5):
            try:
                logging.info("Connecting: %s", ip_address)
                self.bulb_obj_ = BulbYee(ip_address, effect=effect, auto_on=True)
                self.bulb_obj_.set_power_mode(yeelight.PowerMode.RGB)
                self.bulb_obj_.start_music()
                logging.info("Connected: %s", ip_address)
                return self.bulb_obj_
            except (BulbException, ConnectionResetError, TypeError):
                time.sleep(5)

        raise BulbConnectionLostException(f"No connection established with {ip_address}")

    def show_queue(self) -> None:
        """
        Draw the state of colors queue.
        Queue is used to determine the current color (as avg of all in queue).
        Function for debugging purposes.
        :return: None, shows image with Image.show()
        """
        image_new = Image.new('RGB', (self.queue_size * 10, 50), (224, 224, 224))
        draw = ImageDraw.Draw(image_new)
        for i, color in enumerate(self.colors_queue):
            hor_shift = 10 * i
            box = (hor_shift, 50, hor_shift + 10, 0)
            fill = color.tuple()
            draw.rectangle(box, fill=fill)
        image_new.show()

    def change_color(self, color: Color):
        """
        The interface for smooth changing the color of the light bulb.
        Saturates the transmitted color, adds to the color queue.
        :param color: Object Color.
        :return: None
        """
        color = color.saturated()
        self.colors_queue.append(color)
        if len(self.colors_queue) > self.queue_size:
            self.colors_queue.popleft()
        if Settings.SHOW_COLORS_QUEUE:
            self.show_queue()
        color = ColorGenerator.extract_avg_color(list(self.colors_queue))
        self.bulb_obj.set_rgb(*color.tuple())

    def __repr__(self):
        return f"<Bulb(id='{self.id}', name='{self.name}', " \
               f"last_ip='{self.last_ip}, last_usage='{self.last_usage}')>"

    def is_valid(self):
        """
        Checks if bulb last_ip and last_usage are not None.
        :return:
        """
        return bool(self.last_ip and self.last_usage and self.id)


Base.metadata.create_all(engine)
