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
    lang = None
    config = None
    bridge = None
    def __init__(self, config, lang):
        self.config = config
        self.lang = lang
        bridgeIp = config.get('hue','ip')
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
            except PhueRegistrationException:
                time.sleep(1)
                continue
            except Exception as e:
                return str(e)
            else:
                break
        return bridge if bridge is not None else self._label('error_connect')
    def _label(self, label):
        return self.config.get('lang_'+self.lang, label)
        
    def statusAll(self):
        lights = self.bridge.get_light_objects()
        out = '';
        for light in lights:
            out = out + self._label('lightstate').format(light.name, (self._label('state_on') if light.on else self._label('state_off'))) + " "
        return out.strip()

    def status(self, lightName):
        light = self.__get_light(lightName)
        if light is None:
            return self._label('light_not_found').format(lightName)
        return self._label('lightstate').format(light.name, (self._label('state_on') if light.on else self._label('state_off')))

    def lights_off(self):
        lights = self.bridge.get_light_objects()
        for light in lights:
            self.turn_off(light)
        return self._label('done')

    def lights_on(self):
        lights = self.bridge.get_light_objects()
        for light in lights:
            self.turn_on(light)
        return self._label('done')

    def turn_off(self, lightName):
        return self.turn_onoff(lightName, False)
    def turn_on(self, lightName):
        return self.turn_onoff(lightName, True)

    def turn_onoff(self, lightName, onOrOff):
        light = self.__get_light(lightName) if isinstance(lightName, basestring) else lightName
        if light is None:
            return self._label('light_not_found').format(lightName)
        light.on = onOrOff
        return self._label('done')

    def random(self, lightName):
        light = self.__get_light(lightName)
        if lightName is None:
            return self._label('light_not_found').format(lightName)
        light.on = True
        light.xy = [random.random(),random.random()]
        return self._label('done')

    def darker(self, lightName):
        return self.brightness(lightName, -40)

    def brighter(self, lightName):
        return self.brightness(lightName, 40)
    
    def brightness(self, lightName, change):
        light = self.__get_light(lightName)
        if lightName is None:
            return self._label('light_not_found').format(lightName)
        light.on = True
        light.brightness = light.brightness + change
        return self._label('done')

    def __get_light(self, lightName):
        lights = self.bridge.get_light_objects('name')
        if lightName in lights:
            return lights[lightName]
        return None

    def do_command(self, command, light):
        commands = {
            'status': self.status,
            'statusall': self.statusAll,
            'lightson': self.lights_on,
            'lightsoff': self.lights_off,
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
        x = Hue(config, args.lang);
        print x.do_command(args.command , args.light)
    except Exception as e:
        print e
