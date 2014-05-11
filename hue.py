#!/usr/bin/python

from phue import Bridge
from multiprocessing import Process
import math
import time

b = Bridge('10.0.0.16')
lights = b.lights

def pulse(light=b.lights[-1], period=5.0, update_frequency=10.0):
	f = 1./(period)
	while 1:
		for i in range(0,100):
		    x = (float(i)/100.0)*math.pi*2.0
		    o = math.sin(x*f)*128.0 + 128.0
		    light.transitiontime = 1
		    light.brightness = int(o)
		    print o
		    time.sleep(1./update_frequency)


