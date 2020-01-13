import time, os, pigpio
import RPi.GPIO as GPIO
from page_flip import nextPage
from shutil import copyfile


#BUTTON CALLBACKS
def button1_pressed(channel):
    #Start to read current page
    #Take Picture
    print("Button 1 pressed")
    cleanup()
    os.system('sudo raspistill -w 3280 -h 2464 -o /home/pi/main/images/image.jpg')
    copyfile('/home/pi/main/images/image.jpg', '/home/pi/main/images/image' + str(time.time()) + '.jpg')
    print("Image captured")
    os.system('sudo python3 /home/pi/main/vision_API.py')


def button2_pressed(channel):
    #start repeated
    print("Button 2 pressed")
    cleanup()
    while True:
        os.system('sudo raspistill -w 3280 -h 2464 -o /home/pi/main/images/image.jpg')
        print("Image captured")
        #os.system('sudo python3 /home/pi/main/page_flip.py')
        nextPage(pi)
        os.system('sudo python3 /home/pi/main/vision_API.py')


def button3_pressed(channel):
    #Next page
    print("Button 3 pressed")
    cleanup()
    #os.system('sudo python3 /home/pi/main/page_flip.py')
    nextPage(pi)

def button4_pressed(channel):
    #stop and end
    print("Button 4 pressed")
    pi.set_servo_pulsewidth(23, 0)
    pi.set_servo_pulsewidth(18, 0)

def cleanup():
    #define later
    print("Cleanup called")
    pi.set_servo_pulsewidth(23, 0)
    pi.set_servo_pulsewidth(18, 0)

def setup():

   global pi
   pi = pigpio.pi()              # use defaults

   if not pi.connected:
      print("pi not connected")
      pi.stop()
      exit()

   print("connected")

   pi.set_mode(18, pigpio.OUTPUT)
   pi.set_mode(23, pigpio.OUTPUT)

   #BUTTON SETUP
   button1_pin = 31
   button2_pin = 33
   button3_pin = 35
   button4_pin = 37

   GPIO.setmode(GPIO.BOARD)

   GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(button3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(button4_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


   GPIO.add_event_detect(button1_pin, GPIO.FALLING, callback=button1_pressed, bouncetime=200)

   GPIO.add_event_detect(button2_pin, GPIO.FALLING, callback=button2_pressed, bouncetime=200)
   GPIO.add_event_detect(button3_pin, GPIO.FALLING, callback=button3_pressed, bouncetime=200)
   GPIO.add_event_detect(button4_pin, GPIO.FALLING, callback=button4_pressed, bouncetime=200)


setup()
while True:

    x = int(input("Enter virtual button number: "))

    if x == 1:
        button1_pressed(31)
    elif x == 2:
        button2_pressed(33)
    elif x == 3:
        button3_pressed(35)
    elif x == 4:
        button4_pressed(37)

    if GPIO.event_detected(37):
        processes = os.popen('ps -ax | grep vision_API.py').read()

        i = 0
        process_id = ""

        while(processes[i] == ' '):
            i += 1

        while(processes[i].isdigit()):
            process_id += processes[i]
            i += 1

        #print("process that we need to kill: ", end="")
        #print(process_id)
        os.system('sudo kill -2 ' + str(process_id))
        print("Process " + str(process_id) + " killed")
