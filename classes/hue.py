#!/usr/bin/python
#-*- coding:Utf-8 -*-
from phue import Bridge
from phue import PhueRegistrationException
import time
import random
import argparse
import os 
import ConfigParser

class Hue:
    bridge = None
    def __init__(self, bridgeIp):
        bridge = self._register_with_bridge(bridgeIp)
        if isinstance(bridge, basestring):
            raise ValueError(bridge)
        else:
            self.bridge = bridge

    def _register_with_bridge(self, ip):
        i = 0
        while i < 5:
            bridge = None
            i = i + 1
            try:
                bridge = Bridge(ip)
            except PhueRegistrationException as pe:
                time.sleep(1)
                continue
            except Exception as e:
                return str(e)
            else:
                break
        return bridge if bridge is not None else "Verbindung zur Bridge fehlgeschlagen. Drücke den Link Button!"
#        return bridge if bridge is not None else "Connection to bridge failed. Press link button!"
    
    
    
    def statusAll(self):
        lights = self.bridge.get_light_objects()
        out = '';
        for light in lights:
            out = out + "Die Leuchte " + light.name + " ist " + ("an" if light.on else "aus") +". "
        return out.strip()

    def status(self, lightName):
        light = self.__get_light(lightName)
        if lightName is None:
            return "Light "+lightName+" not found"
        return "Die Leuchte " + light.name + " ist " + ("an" if light.on else "aus")
    def turn_off(self, lightName):
        return self.turn_onoff(lightName, False)
    def turn_on(self, lightName):
        return self.turn_onoff(lightName, True)

    def turn_onoff(self, lightName, onOrOff):
        light = self.__get_light(lightName)
        if lightName is None:
            return "Light "+lightName+" not found"
        light.on = onOrOff

    def random(self, lightName):
        light = self.__get_light(lightName)
        if lightName is None:
            return "Light "+lightName+" not found"
        light.on = True
        light.xy = [random.random(),random.random()]

    def darker(self, lightName):
        return self.brightness(lightName, -40)
    def brighter(self, lightName):
        return self.brightness(lightName, 40)
    def brightness(self, lightName, change):
        light = self.__get_light(lightName)
        if lightName is None:
            return "Light "+lightName+" not found"
        light.on = True
        light.brightness = light.brightness + change
        return light.brightness
    def __get_light(self, lightName):
        lights = self.bridge.get_light_objects('name')
        if lightName in lights:
            return lights[lightName]
        return None
    def do_command(self, command, light):
        commands = {
            'status': self.status,
            'statusall': self.statusAll,
            'turnon': self.turn_on,
            'turnoff': self.turn_off,
            'random': self.random,
            'brighter': self.brighter,
            'darker': self.darker,
        }
        if light is None:
            return commands[command]()
        else:
            return commands[command](light)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('lang', help='lang help')
    parser.add_argument('command', help='command help')
    parser.add_argument('-light', help='light help')
    args = parser.parse_args()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser.ConfigParser()
    config.read(dir_path + '/../config.ini')
    try:
        x = Hue(config.get('hue','ip'));
        print x.do_command(args.command , args.light)
    except Exception as e:
        print e
