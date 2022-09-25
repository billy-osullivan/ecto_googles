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


from picamera import PiCamera
import time
import board
import busio
import adafruit_mlx90640
import pygame

# define screen size
SCREEN_WIDTH = 615
SCREEN_HEIGHT = 285

# define colours
pink = [255,0,255]
purple = [191,0,255]
blue = [0,0,255]
light_blue = [0,102,255]
very_light_blue = [153,204,255]
white = [255,255,255]
light_grey = [217,217,217]
red = [255,0,0]
dark_red = [179,0,0]
black = [0,0,0]
light_green = [204, 255,204]
green = [0,255,0]
dark_green = [0,128,0]

# set up i2c bus
i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_10_HZ

#set up pygame
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
# set up the screen and its size
screen = pygame.display.set_mode(size)
pygame.init()
screen.fill(black)
pygame.mouse.set_visible(False)

# print temps and colours to screen
font = pygame.font.SysFont(None, 30)
temp1 = font.render('<27', True, white)
temp2 = font.render('29', True, light_grey)
temp3 = font.render('31', True, very_light_blue)
temp4 = font.render('33', True, blue)
temp5 = font.render('35', True, purple)
temp6 = font.render('37', True, pink)
temp7 = font.render('39', True, red)
temp8 = font.render('40>', True, dark_red)
temp9 = font.render('<0', True, dark_green)
temp10 = font.render('<5', True, green)
temp11 = font.render('<10', True, light_green)
screen.blit(temp1, (10, 180))
screen.blit(temp2, (50, 180))
screen.blit(temp3, (80, 180))
screen.blit(temp4, (110, 180))
screen.blit(temp5, (140, 180))
screen.blit(temp6, (170, 180))
screen.blit(temp7, (200, 180))
screen.blit(temp8, (230, 180))
screen.blit(temp9, (10, 205))
screen.blit(temp10, (50, 205))
screen.blit(temp11, (90, 205))

# ghost advice text
font = pygame.font.SysFont(None, 30)
adv1 = font.render('Living People: ', True, white)
adv2 = font.render('33 to 37 degrees', True, white)
screen.blit(adv1, (400, 180))
screen.blit(adv2, (400, 205))

# set up the camera, but no preview
camera = PiCamera()
#camera.resolution = (214, 160)
camera.framerate = 15
# windo functions are (x, y, width, height)
camera.start_preview(fullscreen=False, window=(400,100,214,160))
time.sleep(.5)

#define the frame size for the thermal sensor
frame = [0] * 768
rect_width = 7
rect_height = 7

while True:
	
	try:
		mlx.getFrame(frame)
	except ValueError:
		continue
	row = 1
	column = 1
	for row in range(24):
		row_pos = int((row * 10) * 0.67)
		for column in range(32):
			temp = frame[row * 32 + column]
			
			col_pos = 214 - (int((column * 10) * 0.67))
			
			if temp < 27:
				pygame.draw.rect(screen, white, pygame.Rect(col_pos, row_pos , rect_width, rect_height))
			elif temp < 29:
				pygame.draw.rect(screen, light_grey, pygame.Rect(col_pos, row_pos , rect_width, rect_height))
			elif temp < 31:
				pygame.draw.rect(screen, very_light_blue, pygame.Rect(col_pos, row_pos , rect_width, rect_height))
			elif temp < 33:
				pygame.draw.rect(screen, blue, pygame.Rect(col_pos, row_pos , rect_width, rect_height))
			elif temp < 35:
				pygame.draw.rect(screen, purple, pygame.Rect(col_pos, row_pos , rect_width, rect_height))
			elif temp < 37:
				pygame.draw.rect(screen, pink, pygame.Rect(col_pos, row_pos , rect_width, rect_height))
			elif temp < 39:
				pygame.draw.rect(screen, red, pygame.Rect(col_pos, row_pos , rect_width, rect_height))
			elif temp > 38:
				pygame.draw.rect(screen, dark_red, pygame.Rect(col_pos, row_pos , rect_width, rect_height))
			
			pygame.display.update(pygame.Rect(col_pos,row_pos,7,7))
	pygame.display.flip()
	

