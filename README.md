Raspberry Pi Zero 2 based Ghost busters Ecto goggle software

# Ecto goggles v1.1
# Raspberry pi camera
#
# Runs on pygame and python3
#
# Author:			Billy O Sullivan
# Created date:		05 September 2022
# Edited:			25 September 2022
#
# python 3.7
#
# CHANGES MADE
##############
# 
# 1. The script no longer takes a jpeg for the output image
#    It now uses a camera preview
#
# 2. The thermal sensor now has a far better output speed.
#    This involves tuning the datarate of the i2c throuput
#    using the steps mentioned below
#
# INFORMATION ABOUT THERMAL SENSOR
##################################
#
# MLX90640 Thermal Camera Breakout
# https://shop.pimoroni.com/products/mlx90640-thermal-camera-breakout?variant=12536948654163
# thermal sensor has 24*32 pixels
# total is 768 pixels
# sensor will measure temps between -40 to 300 degrees celsius (+/- 2 degrees)
#
# TUNING THE THERMAL SENSOR I2C THROUGHPUT
##########################################
#
# 1. Open the boot config file
#    sudo nano /boot/config.txt
#
# 2. Add the following line (or if there is already a line specifiying the i2c baudrate, edit it)
#	 dtparam=i2c1_baudrate=1000000
#
# 3. Try different values (between 2 and 16) for the refresh value in the line of python code that says 
#    "mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_10_HZ"
#    For example try
#    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
#    or
#    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ
#
#
# REQUIREMENTS
##############
#
# sudo pip3 install adafruit-blinka
# sudo pip3 install adafruit-circuitpython-mlx90640
