# Imports
import os
import time
from RPi import GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(4, GPIO.OUT)

# on eteint la led au demarrage

print('Start program')

while True:
 bouton= GPIO.input(17)
 if(bouton==True):
   GPIO.output(4,GPIO.HIGH)
   bashCommand ="python cdt-ok.py 60"
   os.system(bashCommand)
 else:
   GPIO.output(4,GPIO.LOW)
