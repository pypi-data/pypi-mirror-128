"""
Module of manager for managing multiple bulbs.
"""
import logging
import platform
import subprocess
import time
from typing import List

import ifaddr
from sqlalchemy import func
from yeelight import discover_bulbs, BulbException

from .bulb import Bulb, session
from .color import Color
from .exception import BulbConnectionLostException
from .generator import ColorGenerator


class BulbManager:
    """
    Class for managing bulbs.
    """

    def __init__(self, use_last_bulb: bool, bulb_ip_address: str,
                 effect: str = 'smooth', timeout: int = 5):
        self.use_last_bulb = use_last_bulb
        self.effect = effect
        self.bulb_ip_address = bulb_ip_address
        self.timeout = timeout
        self.cached_bulbs = None
        self.chosen_bulbs = set()

    def run_atmosphere(self, strategy, delay):
        """
        Main entrypoint. Chooses bulb, starts color generator and changes colors of bulbs.
        :param strategy: defines screens areas to capture
        :param delay: delay (secs) between generator yield colors
        :return:
        """
        self.choose()

        for new_color in ColorGenerator(strategy).generator(delay):
            self.change_color(new_color)

    def choose(self, reset=False):
        """
        Choose bulbs to interact with.
        :param reset:
        :return:
        """
        result = None
        if reset:
            self.use_last_bulb = False
            self.bulb_ip_address = None
            self.cached_bulbs = None

        if self.use_last_bulb:
            last_bulb = self.get_last_bulb()
            if last_bulb and last_bulb.is_valid():
                last_bulb.last_ip = self.get_current_ip_by_bulb_id(last_bulb.id)
                last_bulb.last_usage = func.now()
                self.send_to_db(last_bulb)
                result = last_bulb
            else:
                logging.info("Last bulb was not found.")
        elif self.bulb_ip_address:
            if self.is_bulb_alive(self.bulb_ip_address):
                result = self.get_bulb_by_ip(self.bulb_ip_address)
            else:
                logging.info("IP %s is not active.", self.bulb_ip_address)

        if not result:
            result = self.choose_alive()
        if result:
            self.chosen_bulbs.add(result)
        return result

    def get_current_ip_by_bulb_id(self, id_) -> str:
        """
        :param id_: bulb id given by discover_bulbs(), example: '0x00000000129f22a6'
        :return: ip address string
        """
        alive_bulbs = self.get_alive_bulbs()
        current_ip = None
        for bulb_d in alive_bulbs:
            capabilities = bulb_d.get('capabilities', None)
            if isinstance(capabilities, dict):
                cur_id = capabilities.get('id', None)
                if cur_id == id_:
                    cur_ip = bulb_d.get("ip", None)
                    current_ip = cur_ip

        return current_ip

    def get_bulb_by_ip(self, ip_address) -> Bulb:
        """
        :param ip_address:
        :return: dict from discover_bulbs() representing a bulb
        """
        bulbs = self.get_alive_bulbs()
        res = None
        for bulb in bulbs:
            if bulb.get('ip') == ip_address:
                res = bulb
                break

        new_bulb = None
        if res:
            new_bulb = self.new_bulb_from_dict(res)
            self.send_to_db(new_bulb)

        return new_bulb

    @staticmethod
    def get_last_bulb() -> Bulb:
        """
        :return: last used bulb from database
        """
        max_query = session.query(func.max(Bulb.last_usage))
        bulb = session.query(Bulb).filter(Bulb.last_usage == max_query.scalar_subquery()).first()
        if bulb and bulb.last_ip is None:
            bulb = None

        return bulb if bulb else None

    def get_alive_bulbs(self, reset=False) -> List[dict]:
        """
        :param reset: flag to reset cached list of bulbs
        :return: result of discover_bulbs(), list of dicts:
        {'ip': '192.168.1.4', 'port': 55443, 'capabilities': {...}}
        """
        if (not self.cached_bulbs) or reset:
            tmp_res = []
            srt_adapters = sorted(
                ifaddr.get_adapters(), key=lambda a: tuple(sorted(
                    [ip.ip for ip in a.ips if isinstance(ip.ip, str)]
                )),
                reverse=True)  # Sorting of adapters by IP, to visit local 192.* first
            for adapter in srt_adapters:
                logging.info("Start discover bulbs with %s s timeout "
                             "at interface %s.",
                             self.timeout, adapter.nice_name)
                try:
                    tmp_res = discover_bulbs(self.timeout, adapter.name)
                except OSError:
                    tmp_res = []
                if tmp_res:
                    break
            self.cached_bulbs = tmp_res
            logging.info("Found %s bulbs.", len(self.cached_bulbs))
        return self.cached_bulbs

    def is_bulb_alive(self, ip_address) -> bool:
        """
        :param ip_address: ip address of bulb
        :return: True if a bulb is pinging
        """
        res = self._ping_bulb(ip_address)
        return res

    @staticmethod
    def _ping_bulb(host) -> bool:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', host]
        with subprocess.Popen(command,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True) as pipe:
            _, errors = pipe.communicate()
        return not errors

    def choose_alive(self) -> (Bulb, None):
        """
        Command line function to choose bulb.
        :return: chosen bulb
        """
        while True:
            try:
                bulbs = self.get_alive_bulbs()
                variants = set()
                for i, bulb in enumerate(bulbs):
                    print(f"{i}) {bulb.get('ip', None)}")
                    variants.add(str(i))
                while True:
                    inp = input("Enter bulb number ('' for none): ")
                    if inp == '':
                        return None
                    if inp in variants:
                        break
                choice = bulbs[int(inp)]
                new_bulb = self.new_bulb_from_dict(choice)

                self.send_to_db(new_bulb)
                break
            except BulbConnectionLostException:
                time.sleep(3)
                self.get_alive_bulbs(True)

        return new_bulb

    @staticmethod
    def send_to_db(inst: Bulb):
        """
        Saves instance to database.
        :param inst: instance of Bulb
        :return: None
        """
        session.merge(inst)
        session.commit()

    def new_bulb_from_dict(self, b_dict) -> Bulb:
        """
        Create Bulb object from dictionary (given by discover_bulbs())
        :param b_dict: dict of bulb
        :return: Bulb object
        """
        tmp_bulb = Bulb()
        caps = b_dict.get("capabilities", {})
        tmp_bulb.id = caps.get("id", '')
        tmp_bulb.name = caps.get("name", '')
        tmp_bulb.last_usage = func.now()
        tmp_bulb.last_ip = b_dict.get("ip", '')

        tmp_bulb.init_obj(tmp_bulb.last_ip, self.effect)
        return tmp_bulb

    def change_color(self, color: Color, bulb: Bulb = None):
        """
        Interface of changing bulb color, with catching connection errors.
        :param color: Color object to set.
        :param bulb_item: Bulb object to be changed,
        if None given operation applies to all chosen bulbs of BulbManager.
        :return: None
        """
        bulbs = self.chosen_bulbs if not bulb else set(bulb)
        for bulb_item in bulbs:
            try:
                bulb_item.change_color(color)
            except BulbException:
                logging.info("Connection lost. Retrying... ")
                try:
                    bulb_item.init_obj()
                except BulbConnectionLostException:
                    self.chosen_bulbs.clear()
                    logging.info("Connection was not established.")
                    self.choose(True)
