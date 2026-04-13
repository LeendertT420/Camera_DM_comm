#!/usr/bin/python
from MuDMInterface import MuDMInterface,actuator_count,zernikes_count
import numpy
instance = MuDMInterface()
print("Instance Created!")
input("Press Enter to continue...")

instance.connect('0027')
print("Mirror Connected!")
input("Press Enter to continue...")

temp=instance.get_temperature()
print("Temperature Received :"+str(temp))
input("Press Enter to continue...")

test=instance.get_overheat_status()
if test :
    outstr=("Mirror Overheated and Stopped!")
else:
    outstr=("Mirror Working Normally")
print(outstr)
input("Press Enter to continue...")

if not test:
    pos=numpy.zeros(actuator_count())
    pos[0]=100
    instance.move_to_absolute_positions(pos)
    print("Mirror Moved!")
    input("Press Enter to continue...")
    
    zer=numpy.zeros(zernikes_count())
    instance.move_to_zernike_surface(zer,True)
    print("Mirror Moved to Flat Position!")
    input("Press Enter to continue...")
    
    current=instance.get_current_positions()
    print("Current Position Received!")
    print(current)
    input("Press Enter to continue...")
    current

instance.disconnect()
print("Mirror Disonnected!")
input("Press Enter to continue...")

del instance
print("Instance Deleted")
input("Press Enter to continue...")