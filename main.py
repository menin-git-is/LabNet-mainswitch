#!/usr/bin/python

import sys
import requests
import RPi.GPIO as GPIO
import time
import logging

switch_pin = 14
switch_delay = 0.5
prev_input = -1
input_counter = 0
needed_inputs_to_change = 5
labnet_url = "http://192.168.1.6"
state_api_url = "http://192.168.1.6:3000"
LOG_FILENAME = "/var/log/labnet_mainswitch.log"

GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_pin,GPIO.IN)

logging.basicConfig(filename=LOG_FILENAME, format='%(asctime)s %(message)s', level=logging.DEBUG)

def query_api(arg):
  try:
    requests.get(labnet_url + "/api/" + arg)

    if arg == "lab/on":
      requests.post(state_api_url, json={"is_open":True}, headers={'clientId':'supersecret'})
    else:
      requests.post(state_api_url, json={"is_open":False}, headers={'clientId':'supersecret'})
  except requests.exceptions.RequestException as e:
    logging.info("http request failed:")
    print e
  else:
    logging.info("http request succeeded: " + arg)
  return

def toggle_lab(state):
  if ( state == 0 ):
    query_api("lab/off")
  else:
    query_api("lab/on")
  return

logging.info("daemon started")

while True:
  input = GPIO.input(switch_pin)  
  if ( prev_input != input ):
    if(input_counter++ > needed_inputs_to_change):
      toggle_lab(input)
      prev_input = input
  else:
    input_counter = 0
  time.sleep(switch_delay)


