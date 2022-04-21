#!/usr/bin/python

import sys
import csv
from datetime import datetime
import io         # used to create file streams
import fcntl      # used to access I2C parameters like addresses

import time       # used for sleep delay and timestamps
import string     # helps parse strings
import matplotlib.pyplot as plt

class AtlasI2C:
    long_timeout = 1.5         	# the timeout needed to query readings and calibrations
    short_timeout = .5         	# timeout for regular commands
    default_bus = 1         	# the default bus for I2C on the newer Raspberry Pis, certain older boards use bus 0
    default_address = 102     	# the default address for the sensor

    def __init__(self, address=default_address, bus=default_bus):
        # open two file streams, one for reading and one for writing
        # the specific I2C channel is selected with bus
        # it is usually 1, except for older revisions where its 0
        # wb and rb indicate binary read and write
        self.file_read = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
        self.file_write = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

        # initializes I2C to either a user specified or default address
        self.set_i2c_address(address)

    def set_i2c_address(self, addr):
        # set the I2C communications to the slave specified by the address
        # The commands for I2C dev using the ioctl functions are specified in
        # the i2c-dev.h file from i2c-tools
        I2C_SLAVE = 0x703
        fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
        fcntl.ioctl(self.file_write, I2C_SLAVE, addr)

    def write(self, cmd):
        # appends the null character and sends the string over I2C
        cmd += "\00"
        self.file_write.write(cmd)

    def read(self, num_of_bytes=31):
        # reads a specified number of bytes from I2C, then parses and displays the result
        res = self.file_read.read(num_of_bytes)         # read from the board
        response = filter(lambda x: x != '\x00', res)     # remove the null characters to get the response
        if ord(response[0]) == 1:             # if the response isn't an error
            # change MSB to 0 for all received characters except the first and get a list of characters
            char_list = map(lambda x: chr(ord(x) & ~0x80), list(response[1:]))
            # NOTE: having to change the MSB to 0 is a glitch in the raspberry pi, and you shouldn't have to do this!
            return ''.join(char_list)    # convert the char list to a string and returns it
        else:
            return "Error " + str(ord(response[0]))

    def query(self, string):
        # write a command to the board, wait the correct timeout, and read the response
        self.write(string)

        # the read and calibration commands require a longer timeout
        if((string.upper().startswith("R")) or
           (string.upper().startswith("CAL"))):
            time.sleep(self.long_timeout)
        elif string.upper().startswith("SLEEP"):
            return "sleep mode"
        else:
            time.sleep(self.short_timeout)

        return self.read()

    def close(self):
        self.file_read.close()
        self.file_write.close()


def main():
    t0 = 0.0
    t1 = 0.0
    device_0 = AtlasI2C(100) 	# creates the I2C port object, specify the address or bus if necessary
    device_1 = AtlasI2C(102) 	# creates the I2C port object, specify the address or bus if necessary

    # continuous polling command automatically polls the board
    if len(sys.argv) < 2:
        print("Usage: t_loop delaytime (with delaytime > 1.5sec)")
        sys.exit(0)

    delaytime = int(sys.argv[1])
#    print('delaytime: {}'.format(delaytime))

    # set plot
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)
    
    ax1.set_xlabel('time')
    ax1.set_ylabel('temperature')
    ax2.set_xlabel('time')
    ax2.set_ylabel('salinity')
    plt.show(block=False)
    
    temps_list = []
    t0_list = []
    t1_list = []

    # main loop
    while True:

        # check for polling time being too short, change it to the minimum timeout if too short
        if delaytime < AtlasI2C.long_timeout:
            print("Polling time is shorter than timeout, setting polling time to %0.2f" % AtlasI2C.long_timeout)
            delaytime = AtlasI2C.long_timeout

        # get the information of the board you're polling
        info_0 = string.split(device_0.query("I"), ",")[1]
        info_1 = string.split(device_1.query("I"), ",")[1]

        try:
            while True:
                # Date and Time acquisition and format
                temps = datetime.now()
                temps = '{}-{}-{} {}:{}:{}'.format(temps.day, temps.month,temps.year, temps.hour, temps.minute, temps.second)

                # Temperature acquisition RTD 1000 t0 and t1
                t0 = device_0.query("R")
                #time.sleep(2 - AtlasI2C.long_timeout) # Minimum Delay between 2 measurments
                t1 = device_1.query("R")
                print('{};{};{}'.format(temps, t0, t1))

                # Saving data in files
                fcsv = open('/home/public/data_all.csv', 'a')
                fcsv.write('{};{};{}\n'.format(temps, t0, t1))
                fcsv.close()
                fcsv = open('/home/public/data_one.csv', 'w')
                fcsv.write('{};{};{}\n'.format(temps, t0, t1))
                fcsv.close()

                # plot data
                temps_list.append(time)
                t0_list.append(t0)
                t1_list.append(t1)
                ax1.scatter(temps,t0)
                ax2.scatter(temps,t1)
                plt.show(block=False)

                # Delay between 2 acquistions
                time.sleep(delaytime - AtlasI2C.long_timeout)

        except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
            print("Continuous polling stopped")
            sys.exit(0)



if __name__ == '__main__':
    main()
