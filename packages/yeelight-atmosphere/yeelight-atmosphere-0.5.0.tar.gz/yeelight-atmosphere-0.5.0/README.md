# yeelight-atmosphere

The package allows you to control yeelight smart bulbs, changes color according to the color scheme of the image on the
screen.

## Installation

    pip install yeelight-atmosphere

## Usage:

    python -m yeelight_atmosphere

Use --choose flag to force choose a bulb by network scanning otherwise previous bulb if exists will be used.

    python -m yeelight_atmosphere --choose

To choose a part of screen to parse for a color use --strategy flag. Full screen needs more CPU.

- Center area of screen = 0
- Top and bottom borders = 1
- Full screen = 2

    python -m yeelight_atmosphere --strategy 0

To modify delay of changing color use --dalay (seconds). The less the smoother.

    python -m yeelight_atmosphere --delay 0.3

All flags are:

    Force choose bulb
    --choose / -c

    Strategy, see yeelight_atmosphere/const.py
    --strategy / -s

    Force ip address to connect
    --bulb_ip_address / -i

    Bulb search timeout
    --timeout / -t

    Dalay of color change (sec), the less the smoother
    --delay / -d
    
    Size of queue for colors
    The higher the value, the slower the transition
    --queue_size / -q

    The higher the value, the quicker the transition.
    --saturation_factor / -f

    Screenshot will be updated every N delays, 
    where N is ttl and delays from parameter
    --screenshot_ttl / ttl 

# Dependencies:

- Pillow
- sqlalchemy
- yeelight
- colorthief