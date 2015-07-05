# Temporary Main Switch for FabLab Karlsruhe
## run
````
sudo modprobe i2c-dev
sudo apt-get install python-request
sudo cp start.sh /etc/init.d/labnet-mainswitch
sudo chmod +x /etc/init.d/labnet-mainswitch
sudo update-rc.d labnet-mainswitch defaults

````

## circuit diagram
````
5V ____/ _____GPIO 14 (PIN 8)
          |
          |_
          | |10k
          |_|
          |
          o GND
````
