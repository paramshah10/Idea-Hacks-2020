import time, os
import pigpio

'''
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

'''

def nextPage(pi):
   big_servo_pin = 18

   #turn big motor for page turn
   pi.set_servo_pulsewidth(big_servo_pin, 1400)

   time.sleep(1.3)

   #turn off big motor
   pi.set_servo_pulsewidth(big_servo_pin, 0)

   small_servo_pin = 23

   #turn small motor for page turn
   pi.set_servo_pulsewidth(small_servo_pin, 810)

   time.sleep(0.5)

   #turn off small motor
   pi.set_servo_pulsewidth(small_servo_pin, 0)

   time.sleep(0.2)

   #turn the big motor the other way
   pi.set_servo_pulsewidth(big_servo_pin, 1700)
   
   time.sleep(2)

   #turn off reverse motion
   pi.set_servo_pulsewidth(big_servo_pin, 0)


#   take_picture()
 #  take_picture()
  # take_picture()
  # take_picture()
   
   #turn small motor the other way
   pi.set_servo_pulsewidth(small_servo_pin, 2300)

   time.sleep(0.5)

   pi.set_servo_pulsewidth(small_servo_pin, 0)
