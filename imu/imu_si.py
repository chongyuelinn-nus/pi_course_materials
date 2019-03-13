#This Python 2 program reads the data from an LSM303D and an L3GD20H which are both attached to the I2C bus of a Raspberry Pi.
#Both can be purchased as a unit from Pololu as their MinIMU-9 v3 Gyro, Accelerometer, and Compass  product.
#
#First follow the procedure to enable I2C on R-Pi.
#1. Add the lines "ic2-bcm2708" and "i2c-dev" to the file /etc/modules
#2. Comment out the line "blacklist ic2-bcm2708" (with a #) in the file /etc/modprobe.d/raspi-blacklist.conf
#3. Install I2C utility (including smbus) with the command "apt-get install python-smbus i2c-tools"
#4. Connect the I2C device to the SDA and SCL pins of the Raspberry Pi and detect it using the command "i2cdetect -y 1".  It should show up as 1D (typically) or 1E (if the jumper is set).
import struct 
import time, math
def swap32(i):
    return int('{:08b}'.format(i)[::-1],2)
#        return struct.unpack("<I", struct.pack(">I", i))[0]

def twos_comp_combine(msb, lsb):
    twos_comp = 256*msb + lsb
    if twos_comp >= 32768:
        return twos_comp - 65536
    else:
        return twos_comp

#def twos_comp_12b(msb, lsb):
def twos_comp_12b(_msb, _lsb):
    '''
    print "msb: ", _msb, " lsb: ", _lsb
    lsb = swap32(_lsb)
    msb = swap32(_msb)
    print "swapped msb: ", msb, " lsb: ", lsb
    '''
    msb = _msb
    lsb = _lsb
    twos_comp = pow(2,4)*msb + lsb
    if twos_comp >= pow(2,11):
        return twos_comp - pow(2,12)
    else:
        return twos_comp

def twos_complement(input_value, num_bits):
	'''Calculates a two's complement integer from the given input value's bits'''
	mask = 2**(num_bits - 1)
	return -(input_value & mask) + (input_value & ~mask)

from smbus import SMBus
busNum = 1
b = SMBus(busNum)

## LSM303D Registers --------------------------------------------------------------
LSM = 0x6b #Device I2C slave address

LSM_WHOAMI_ADDRESS = 0x0F
LSM_WHOAMI_CONTENTS = 0b1001001 #Device self-id

#Control register addresses -- from LSM303D datasheet

LSM_CTRL_0 = 0x1F #General settings
LSM_CTRL_1 = 0x10 #Turns on accelerometer and configures data rate
LSM_CTRL_2 = 0x11 #Self test accelerometer, anti-aliasing accel filter
LSM_CTRL_3 = 0x12 #Interrupts
LSM_CTRL_4 = 0x13 #Interrupts
LSM_CTRL_5 = 0x14 #Turns on temperature sensor
LSM_CTRL_6 = 0x15 #Magnetic resolution selection, data rate config
LSM_CTRL_7 = 0x16 #Turns on magnetometer and adjusts mode

#Registers holding twos-complemented MSB and LSB of magnetometer readings -- from LSM6DS33 datasheet
LSM_MAG_X_LSB = 0x08 # x
LSM_MAG_X_MSB = 0x09
LSM_MAG_Y_LSB = 0x0A # y
LSM_MAG_Y_MSB = 0x0B
LSM_MAG_Z_LSB = 0x0C # z
LSM_MAG_Z_MSB = 0x0D

#Registers holding twos-complemented MSB and LSB of magnetometer readings -- from LSM303D datasheet
LSM_ACC_X_LSB = 0x28 # x
LSM_ACC_X_MSB = 0x29
LSM_ACC_Y_LSB = 0x2A # y
LSM_ACC_Y_MSB = 0x2B
LSM_ACC_Z_LSB = 0x2C # z
LSM_ACC_Z_MSB = 0x2D

LSM_GYRO_X_LSB = 0x22 # x
LSM_GYRO_X_MSB = 0x23
LSM_GYRO_Y_LSB = 0x24 # y
LSM_GYRO_Y_MSB = 0x25
LSM_GYRO_Z_LSB = 0x26 # z
LSM_GYRO_Z_MSB = 0x27


#Registers holding 12-bit right justified, twos-complemented temperature data -- from LSM303D datasheet
LSM_TEMP_MSB = 0x05
LSM_TEMP_LSB = 0x06

# LIS3MDL registers ----------------------------------------------------

LGD = 0x1e #Device I2C slave address
LGD_WHOAMI_ADDRESS = 0x0F
LGD_WHOAMI_CONTENTS = 0b00111101 #Device self-id

LGD_CTRL_1 = 0x20 #turns on magnetometer
LGD_CTRL_2 = 0x21 #can set a high-pass filter for gyro
LGD_CTRL_3 = 0x22
LGD_CTRL_4 = 0x23 #default full scale is 245dps
LGD_CTRL_5 = 0x24

LGD_TEMP_L = 0x2E
LGD_TEMP_H = 0x2F

#Registers holding mag readings
LGD_MAG_X_LSB = 0x28
LGD_MAG_X_MSB = 0x29
LGD_MAG_Y_LSB = 0x2A
LGD_MAG_Y_MSB = 0x2B
LGD_MAG_Z_LSB = 0x2C
LGD_MAG_Z_MSB = 0x2D

#Ensure chip is detected properly on the bus ----------------------


if b.read_byte_data(LSM, LSM_WHOAMI_ADDRESS) == LSM_WHOAMI_CONTENTS:
    print('LSM303D detected successfully on I2C bus '+str(busNum)+'.')
else:
    print('No LSM303D detected on bus on I2C bus '+str(busNum)+'.')

if b.read_byte_data(LGD, LGD_WHOAMI_ADDRESS) == LGD_WHOAMI_CONTENTS:
    print('L3GD20H detected successfully on I2C bus '+str(busNum)+'.')
else:
    print('No L3GD20H detected on bus on I2C bus '+str(busNum)+'.')

#Set up the chips for reading  ----------------------
    
b.write_byte_data(LSM, LSM_CTRL_1, 0b10100011) # enable accelerometer, 50 hz sampling, set +/- 2g full scale
b.write_byte_data(LSM, LSM_CTRL_2, 0x01010010) # gyro settings
#b.write_byte_data(LSM, LSM_CTRL_5, 0b11100100) #high resolution mode, thermometer on, 6.25hz ODR
b.write_byte_data(LSM, LSM_CTRL_5, 0b01100100) #high resolution mode, thermometer off, 6.25hz ODR
b.write_byte_data(LSM, LSM_CTRL_6, 0b00100000) # set +/- 4 gauss full scale
b.write_byte_data(LSM, LSM_CTRL_7, 0x00) #get magnetometer out of low power mode

b.write_byte_data(LGD, LGD_CTRL_1, 0x01011000) #turn on magnetometer and set to normal mode, no temp, 40 Hz

#Read data from the chips ----------------------

while True:
    time.sleep(0.5)
    magx = twos_comp_combine(b.read_byte_data(LGD, LGD_MAG_X_MSB), b.read_byte_data(LGD, LGD_MAG_X_LSB))
    magy = twos_comp_combine(b.read_byte_data(LGD, LGD_MAG_Y_MSB), b.read_byte_data(LGD, LGD_MAG_Y_LSB))
    magz = twos_comp_combine(b.read_byte_data(LGD, LGD_MAG_Z_MSB), b.read_byte_data(LGD, LGD_MAG_Z_LSB))
    #mag_temp = twos_comp_12b(b.read_byte_data(LSM, LSM_TEMP_MSB) , b.read_byte_data(LSM, LSM_TEMP_LSB))
    #mag_temp = twos_comp_12b(b.read_byte_data(LSM, LSM_TEMP_MSB) , b.read_byte_data(LSM, LSM_TEMP_LSB))
    
    accx = twos_comp_combine(b.read_byte_data(LSM, LSM_ACC_X_MSB), b.read_byte_data(LSM, LSM_ACC_X_LSB))
    accy = twos_comp_combine(b.read_byte_data(LSM, LSM_ACC_Y_MSB), b.read_byte_data(LSM, LSM_ACC_Y_LSB))
    accz = twos_comp_combine(b.read_byte_data(LSM, LSM_ACC_Z_MSB), b.read_byte_data(LSM, LSM_ACC_Z_LSB))

    gyrox = twos_comp_combine(b.read_byte_data(LSM, LSM_GYRO_X_MSB), b.read_byte_data(LSM, LSM_GYRO_X_LSB))
    gyroy = twos_comp_combine(b.read_byte_data(LSM, LSM_GYRO_Y_MSB), b.read_byte_data(LSM, LSM_GYRO_Y_LSB))
    gyroz = twos_comp_combine(b.read_byte_data(LSM, LSM_GYRO_Z_MSB), b.read_byte_data(LSM, LSM_GYRO_Z_LSB))

    # compass settings: +/- 4 gauss, 0.160 mgauss/LSB
    mag_factor = 0.160/1000.0
    magx = magx * mag_factor
    magy = magy * mag_factor
    magz = magz * mag_factor
    print("compass (in gauss): x: ", magx, " y: ", magy, " z: ", magz)
    print("Note: 1 tesla = 10,000 gauss\n")

    # temp: 
    # temp_factor = 1.0/8.0
    # mag_temp = mag_temp * temp_factor
    #print "temp (in deg C): ", mag_temp, '\n'

    # acc settings: +/- 2g, 0.061mg/LSB
    acc_factor = 0.061/1000.0
    accx = accx * acc_factor
    accy = accy * acc_factor
    accz = accz * acc_factor
    print("acc (in g): x: ", accx, " y: ", accy, " z: ", accz)
    print("Note: 1 g = 9.8N\n")
    # gyro defaults: range: +/- 245dps conversion factor: 8.75 mdps/digit
    gyro_factor = 8.75 / 1000.0
    gyrox = gyrox * gyro_factor -48
    gyroy = gyroy * gyro_factor -44
    gyroz = gyroz * gyro_factor -32

    print("gryo (in deg per sec): x: ", gyrox, " y: ", gyroy, " z: ", gyroz )
    print("------------------------------------")
 
