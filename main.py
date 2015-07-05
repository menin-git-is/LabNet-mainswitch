#!/usr/bin/python

import sys
import requests
import RPi.GPIO as GPIO
import time

switch_pin = 14
switch_delay = 0.5
prev_input = -1
labnet_url = "http://labnet.lab.flka.de"

GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_pin,GPIO.IN)

def toggle_lab(state):
  if ( state == 0 ):
    print requests.get(labnet_url + "/api/lab/off")
  else:
    print requests.get(labnet_url + "/api/lab/on")
  return

while True:
  input = GPIO.input(switch_pin)  
  if ( prev_input != input ):
    toggle_lab(input)
    prev_input = input
  time.sleep(switch_delay)


