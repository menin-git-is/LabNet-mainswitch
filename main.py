#!/usr/bin/python

import time
import logging
import requests

import RPi.GPIO as GPIO

LOG_FILENAME = "/var/log/labnet_mainswitch.log"
SWITCH_PIN = 14
PEN_SWITCH_PIN = 15
BUZZER_PIN = 18
LABNET_URL = "http://192.168.1.6"
STATE_API_URL = "http://192.168.1.6:3000"
STATE_API_HEADERS = {'clientId': 'supersecret'}


class DebouncedInput:
    """Represents a GPIO input that is debounced"""

    def __init__(self, pin):
        self.pin = pin
        self.current_value = -1
        self.input_counter = 0
        self.needed_inputs_to_change = 5

        GPIO.setup(SWITCH_PIN, GPIO.IN)

    def has_changed(self):
        """Returns True if the button state has changed"""

        result = False
        new_value = GPIO.input(self.pin)

        if self.current_value != new_value:
            self.input_counter += 1
            if self.input_counter > self.needed_inputs_to_change:
                result = True
                self.current_value = new_value
        else:
            self.input_counter = 0

        return result

class Main:
    """Main handles in- and output signals for the LabSwitch installation."""

    def __init__(self):
        self.switch_delay = 0.5
        self.prev_input = -1
        self.input_counter = 0
        self.needed_inputs_to_change = 5

        self.switch_input = DebouncedInput(SWITCH_PIN)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PEN_SWITCH_PIN, GPIO.IN)
        GPIO.setup(BUZZER_PIN, GPIO.OUT)

        logging.basicConfig(
            filename=LOG_FILENAME,
            format='%(asctime)s %(message)s',
            level=logging.DEBUG)

    def send_update(self, state):
        """send a state update to the API."""

        try:
            requests.get(LABNET_URL + "/api/" + state)

            if state == "lab/on":
                requests.post(STATE_API_URL, json={"is_open": True}, headers=STATE_API_HEADERS)
            else:
                requests.post(STATE_API_URL, json={"is_open": False}, headers=STATE_API_HEADERS)
        except requests.exceptions.RequestException as ex:
            logging.info("http request failed:")
            logging.error(ex)
        else:
            logging.info("http request succeeded: " + state)

    def toggle_lab(self, state):
        """Toggle the state lab/on -> lab/off or lab/off -> lab/on."""

        if state == 0:
            self.send_update("lab/off")
        else:
            self.send_update("lab/on")

    def run(self):
        """Starts the main loop."""

        logging.info("daemon started")

        while True:
            if self.switch_input.has_changed():
                self.toggle_lab(self.switch_input.current_value)

            time.sleep(self.switch_delay)


if __name__ == "__main__":
    Main().run()
