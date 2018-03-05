import json
import lifxlan
import os
import time
import RPi.GPIO as GPIO

def init():
    '''This function initializes lights and pins'''
    # pull the list of all lights on the network from the file created by discover_lights.py
    lightpath = os.path.join(os.path.dirname(__file__), 'lights.json')
    with open(lightpath) as lightfile:
        lights = json.load(lightfile)
    
    # Set up the GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Set up lights and assign to pins
    office_lights = [make_light(lights['Office Light 1']), make_light(lights['Office Light 2'])]
    GPIO.add_event_detect(18, GPIO.RISING, callback=lambda x: toggle(office_lights), bouncetime=2000)

def make_light(net: dict) -> lifxlan.Light:
    '''This function builds a lifx light object from a dict containing the mac and ip address of a light'''
    return lifxlan.Light(net['mac'], net['ip'])

def toggle(lights):
    '''This function gets the current state of all lights that are passed in, and the flips their state'''
    off = True
    try:
        for light in lights:
            if light.get_power():
                # If a single light is on we treat them all as on
                # this means if the lights are in a mixed state they will all turn off on the first toggle
                off = False

        if off:
            [x.set_power(True, 1000) for x in lights]
        else:
            [x.set_power(False, 1000) for x in lights]

    except lifxlan.errors.WorkflowException:
        print("Light not responding")

def main():
    init()
    # do nothing while we wait for gpio callbacks
    while True:
        time.sleep(0.1)


if __name__ == '__main__':
    main()
