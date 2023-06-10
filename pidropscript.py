#!/usr/bin/env python3
from ST7789 import ST7789, BG_SPI_CS_FRONT
from PIL import Image, ImageDraw, ImageFont
import random
import time
import subprocess
import RPi.GPIO as GPIO
import netifaces
from displayhatmini import DisplayHATMini


# Buttons
BUTTON_A = 5
BUTTON_B = 6
BUTTON_X = 16
BUTTON_Y = 24

# Onboard RGB LED
LED_R = 17
LED_G = 27
LED_B = 22

# General
SPI_PORT = 0
SPI_CS = 1
SPI_DC = 9
BACKLIGHT = 13

# Screen dimensions
WIDTH = 320
HEIGHT = 240

buffer = Image.new("RGB", (WIDTH, HEIGHT))
displayhatmini = DisplayHATMini(buffer)
draw = ImageDraw.Draw(buffer)
font = ImageFont.truetype("DejaVuSans.ttf", 16)
width = DisplayHATMini.WIDTH
height = DisplayHATMini.HEIGHT
draw = ImageDraw.Draw(buffer)
font = ImageFont.load_default()


draw.rectangle((0, 0, 50, 50), (255, 0, 0))
draw.rectangle((320-50, 0, 320, 50), (0, 255, 0))
draw.rectangle((0, 240-50, 50, 240), (0, 0, 255))
draw.rectangle((320-50, 240-50, 320, 240), (255, 255, 0))

display = ST7789(
	port=SPI_PORT,
	cs=SPI_CS,
	dc=SPI_DC,
	backlight=BACKLIGHT,
	width=WIDTH,
	height=HEIGHT,
	rotation=180,
	spi_speed_hz=60 * 1000 * 1000,
)

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_X, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_Y, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(BACKLIGHT, GPIO.OUT)
#GPIO.output(BACKLIGHT, GPIO.LOW)

def check_connections():
	#Code to check current connections to the Raspberry Pi
	print("Checking current connections....")
	output = subprocess.check_output(["sudo ifconfig | grep -E '^(eth|wlan|usb)|inet '"], shell=True).decode("utf-8")
	return output

def renew_ip_address():
	#Code to renew and flush IP address
	print("Renewing and flushing IP addresses....")
	#Execute the command to renew and flush TP addresses
	interfaces = netifaces.interfaces()
	output = "Renewing and flushing IP addresses....\n"
	display_output(output)
	for interface in interfaces:
		if interface.startswith(("eth", "wlan", "usb")):
			result = subprocess.run(['sudo','ifdown', interface, '&&', 'sudo', 'ifup', interface, '&&', 'sudo', 'dhclient', interface], capture_output=True, text=True)
			output += result.stdout
		output +="IP addresses renewed and refreshed\n"
		display_output(output)
	print("IP addresses renews and refreshed")
	return output

def display_output(output):
	buffer.paste((0, 0, 0), (0, 0, WIDTH, HEIGHT))
	draw.text((10, 10), output, font=font, fill=(255, 255, 255))
	display.display(buffer)

def display_image(display, image):
	#Code to display jpg image
	#display.display(image)
	display.display(buffer)

def produce_black_screen():
	#Code to produce a completely black screen using black pixels
	#print("Producing black screen...")
	black_image = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
	buffer.paste(black_image, (0, 0))
	display.display(buffer)

def scroll_text(text, step):
	position = 0
	while True:
		draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(0, 0, 0))
		draw.text((10, 10 - position), text, font=font, fill=(255, 255, 255))
		display.display(buffer)
		time.sleep(0.000001)

		if displayhatmini.read_button(BUTTON_X):
			position -= step
		elif displayhatmini.read_button(BUTTON_Y):
			position += step

while True:
	display.display(buffer)

	if displayhatmini.read_button(BUTTON_A):
		output = check_connections()
		display_output(output)

	if displayhatmini.read_button(BUTTON_B):
		output = renew_ip_address()
		display_output(output)

	if displayhatmini.read_button(BUTTON_X):
		print("Displaying JPG image...")
		image_path = "/opt/pidropimagecovert.jpg"
		image = Image.open(image_path).convert("RGB")
		image.thumbnail((WIDTH, HEIGHT))
		buffer.paste(image, ((WIDTH - image.width) // 2, (HEIGHT - image.height) // 2))
		display.display(buffer)

	if displayhatmini.read_button(BUTTON_Y):
		produce_black_screen()

	display.display(buffer)
	time.sleep(0.1)

