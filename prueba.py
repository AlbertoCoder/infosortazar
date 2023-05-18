import RPi.GPIO as GPIO
import time

# Set up GPIO pins
RS = 26 # Register select pin
E = 19  # Enable pin
D4 = 13  # Data pin 4
D5 = 6  # Data pin 5
D6 = 5  # Data pin 6
D7 = 11  # Data pin 7

# Define LCD constants
LCD_WIDTH = 16  # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005  # Pulse duration for enable pin
E_DELAY = 0.0005  # Delay between operations

def lcd_init():
    # Configure GPIO pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RS, GPIO.OUT)
    GPIO.setup(E, GPIO.OUT)
    GPIO.setup(D4, GPIO.OUT)
    GPIO.setup(D5, GPIO.OUT)
    GPIO.setup(D6, GPIO.OUT)
    GPIO.setup(D7, GPIO.OUT)
    
    # Initialize display
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialize
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialize
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command
    
    GPIO.output(RS, mode)  # RS
    
    # High bits
    GPIO.output(D4, False)
    GPIO.output(D5, False)
    GPIO.output(D6, False)
    GPIO.output(D7, False)
    
    if bits & 0x10 == 0x10:
        GPIO.output(D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(D7, True)
    
    # Toggle 'Enable' pin
    lcd_toggle_enable()
    
    # Low bits
    GPIO.output(D4, False)
    GPIO.output(D5, False)
    GPIO.output(D6, False)
    GPIO.output(D7, False)
    
    if bits & 0x01 == 0x01:
        GPIO.output(D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(D7,


