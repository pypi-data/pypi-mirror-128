"""
Entrypoint module for script execution
"""
import argparse
import logging
import sys

from .const import Settings
from .manager import BulbManager


def set_logging():
    """
    Sets logging parameters
    :return:
    """
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def main():
    """
    Entrypoint
    :return:
    """
    set_logging()
    parser = argparse.ArgumentParser()

    parser.add_argument('--choose', '-c', dest='choose', action='store_true', default=False)
    parser.add_argument("--strategy", "-s", type=int, default=Settings.BORDERS_STRATEGY)
    parser.add_argument("--bulb_ip_address", "-i", type=str, default=None)
    parser.add_argument("--timeout", "-t", type=int, default=5)
    parser.add_argument("--delay", "-d", type=float, default=0.2)
    parser.add_argument("--queue_size", "-q", type=int, default=30)
    parser.add_argument("--saturation_factor", "-f", type=float, default=7)
    parser.add_argument("--screenshot_ttl", "-ttl", type=int, default=5)

    args = parser.parse_args()

    # don't use last bulb if IP or forced choice flagged
    use_last_bulb = not (args.choose or args.bulb_ip_address)

    strategy = args.strategy
    bulb_ip_address = args.bulb_ip_address
    timeout = args.timeout
    delay = args.delay
    Settings.QUEUE_SIZE_CONST = args.queue_size
    Settings.SATURATION_FACTOR = args.saturation_factor
    Settings.SCREENSHOT_TTL = args.screenshot_ttl

    logging.info("QUEUE_SIZE_CONST: %s SATURATION_FACTOR: %s",
                 Settings.QUEUE_SIZE_CONST, Settings.SATURATION_FACTOR)
    logging.info("Screenshot estimated delay: %s s.", delay * Settings.SCREENSHOT_TTL)

    manager = BulbManager(use_last_bulb, bulb_ip_address, timeout=timeout)
    manager.run_atmosphere(strategy, delay)
