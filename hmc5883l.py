# hmc5883l class by ThreeSixes (https://github.com/ThreeSixes/py-hmc5883l)

###########
# Imports #
###########

import quick2wire.i2c as qI2c
from pprint import pprint

##################
# hmc5883L class #
##################

class hmc5883l:
    """
    hmc5883l is a class that supports communication with an I2C-connected Honeywell HMC5883L 3-axis magenetometer/compass. The constructor for this class accepts one argement:

    hmc5883lAddr: The I2C address of the sensor, but will default to 0x1e if it's not specified.
    """

    # The magnetometer config variables are based on the HMC5883L datasheet
    # http://www51.honeywell.com/aero/common/documents/myaerospacecatalog-documents/Defense_Brochures-documents/HMC5883L_3-Axis_Digital_Compass_IC.pdf

    def __init__(self, hmc5883lAddr = 0x1e):
        # I2C set up class-wide I2C bus
        self.__i2c = qI2c
        self.__i2cMaster = qI2c.I2CMaster()
        
        # Set global address var
        self.__addr = hmc5883lAddr
        
        # Confiuration registers
        self.regCfgA =  0x00
        self.regCfgB =  0x01
        self.regMode =  0x02
        self.regXMSB =  0x03
        self.regXLSB =  0x04
        self.regZMSB =  0x05
        self.regZLSB =  0x06
        self.regYMSB =  0x07
        self.regYLSB =  0x08
        self.regStat =  0x09
        self.regIDA  =  0x0a
        self.regIDB  =  0x0b
        self.regIDC  =  0x0c
        
        # Config Register A bits
        self.__regACR7  = 0x80 # Reserved. Should be set to zero always.
        self.__regAMA1  = 0x40 # Sampling average bit 1
        self.__regAMA0  = 0x20 # Sampling average bit 0
        self.__regADO2  = 0x10 # Data output rate bit 2
        self.__regADO1  = 0x08 # Data output rate bit 1
        self.__regADO0  = 0x04 # Data output rate bit 0
        self.__regAMS1  = 0x02 # Measurement bias config bit 1
        self.__regAMS0  = 0x01 # Measurement bias config bit 0
        
        # Config Register B bits
        self.__regBGN2  = 0x80 # Gain bit 2
        self.__regBGN1  = 0x40 # Gain bit 1
        self.__regBGN0  = 0x20 # Gain bit 0
        
        # Mode Register bits
        self.__regMHS   = 0x80 # High speed register bit (this is set by the HS pin)
        self.__regMMD1  = 0x02 # Operating mode bit 1
        self.__regMMD0  = 0x01 # Operating mode but 0
        
        # Status register bits
        self.statRdy  = 0x01 # Ready bit
        self.statLock = 0x02 # Status lock bit
        
        
        # Register A settings
        # Sample averaging
        self.avg1     = 0x00 # Don't average samples (default)
        self.avg2     = self.__regAMA0 # Average two samples.
        self.avg4     = self.__regAMA1 # 4 samples.
        self.avg8     = self.__regAMA0 | self.__regAMA1 # 8 samples
        
        # Output rate
        self.freq_75  = 0x00 # Output rate of 0.75 HZ
        self.freq1_5  = self.__regADO0 # Output rate of 1.5 HZ
        self.freq3    = self.__regADO1 # Output rate of 3.0 HZ
        self.freq7    = self.__regADO0 | self.__regADO1 # Output rate of 7.0 HZ
        self.freq15   = self.__regADO2 # Output rate of 15 HZ (Default)
        self.freq30   = self.__regADO0 | self.__regADO2 # Output rate of 30 HZ
        self.freq75   = self.__regADO1 | self.__regADO2 # Output rate of 75 HZ
        
        # Measurement mode
        self.biasNone = 0x00 # Normal mode. No bias applied to axis. (Default)
        self.biasPos  = self.__regAMS0 # Positive bias across X, Y, Z axis.
        self.biasNeg  = self.__regAMS1 # Netative bias across X, Y, Z axis.
        
        # Register B settings
        # Sensor gain
        self.gain1370 = 0x00 # Gain for 1370 mG/LSB
        self.gain1390 = self.__regBGN0 # 1390 mG/LSB (default)
        self.gain830  = self.__regBGN1 # 830 mG/LSB
        self.gain660  = self.__regBGN0 | self.__regBGN1 # 660 mG/LSB
        self.gain440  = self.__regBGN0 | self.__regBGN2 # 440 mG/LSB
        self.gain390  = self.__regBGN0 | self.__regBGN2 # 390 mG/LSB
        self.gain330  = self.__regBGN1 | self.__regBGN2 # 330 mG/LSB
        self.gain230  = self.__regBGN0 | self.__regBGN1 | self.__regBGN2 # 230 mG/LSB
        
        # Mode register settings
        self.modeCont = 0x00 # Continuous sampling mode
        self.modeSngl = self.__regMMD0 # Single-measurement mode (default)
        self.modeIdlA = self.__regMMD1 # Idle mode A?
        self.modeIdlB = self.__regMMD0 | self.__regMMD1 # Idle mode B?
    
    def __readReg(self, register):
        """
        __readReg(register)
        
        Read a given register from the HMC5883L.
        """
        
        data = 0
        
        try:
            # Read the specific register.
            res = self.__i2cMaster.transaction(self.__i2c.writing_bytes(self.__addr, register), self.__i2c.reading(self.__addr, 1))
            data = ord(res[0])
            
        except IOError:
            print("hmc5883l IO Error: Failed to read HMC5883L sensor on I2C bus.")
            
        return data
    
    def __readRegRange(self, regStart, regEnd):
        """
        __readRegRange(regStart, regEnd)
        
        Reads a continuous range of registers from regStart to regEnd. Returns an array of integers.
        """
        
        regRange = ""
        
        # Figure out how many bytes we'll be reading.
        regCount = (regEnd - regStart) + 1
        
        print(regCount)
        
        # Read a range of registers.
        regRange = self.__i2cMaster.transaction(self.__i2c.writing_bytes(self.__addr, regStart), self.__i2c.reading(self.__addr, regCount))
        
        # Convert returned data to byte array.
        regRange = bytearray(regRange[0])
        
        pprint(regRange)
        
        return regRange
    
    def __writeReg(self, register, byte):
        """
        __writeReg(register, byte)
        
        Write a given byte to a given register to the HMC5883L
        """
        
        try:
            self.__i2cMaster.transaction(self.__i2c.writing_bytes(self.__addr, register, byte))
        except IOError:
            print("hmc5883l IO Error: Failed to write to HMC5883L sensor on I2C bus.")

    def __regMask(self, part):
        """
        regMask(part)
        
        Computes the register mask for modifying a portion of a register, preserving the original bits in place. Returns an int.
        """
        
        return (0xff - part)
    
    def __getSigned(self, unsigned):
        """
        __getSigned(number)
        
        Converts the reading from the magnetometer to a signed int. This is required because python doesn't see the AND'd values as a two's compliment signed binary number. Also supports returning 4096 in the event an axis is saturated.
        """
        
        signednum = 0
        
        # If our axis is reporting saturated
        if unsigned == 4096:
            signednum = unsigned
        # Else, keep going.
        elif unsigned > 2047:
            signednum = unsigned - 65535
        # No need to change sign number is already positive.
        else:
            signednum = unsigned
        
        # Return the unsigned int.
        return signednum
    
    def getIDInfo(self):
        """
        getIDInfo()
        
        Gets the contents of the ID registers, returns an array of three integers.
        """
        idInfo = []
        
        idInfo = self.__readRegRange(self.regIDA, self.regIDC)
        
        return idInfo
    
    def getStatus(self):
        """
        getStatus()
        
        Gets the status register's contents. Returns an integer.
        """
        
        return self.__readReg(self.regStat)
    
    def getXZY(self):
        """
        getXZY()
        
        Checks the status register to make sure the I2C data is ready, then reads the magnetometer data for the X, Z, and Y axis. Returns an array with three ints in the read order ([0] = X... [2] = Y).
        """
        
        rawXZY = []
        retVal = [0, 0, 0]
        
        if (self.__readReg(self.regStat) | self.statLock) == self.statLock:
            raise IOError("HMC5883L data not ready.")
        else:
           
            # Get the desired register values.
            rawXZY = self.__readRegRange(self.regXMSB, self.regYLSB)
            
            # And the MSB and LSB for each value together to yield our raw values.
            retVal[0] = self.__getSigned((rawXZY[0] << 8) | rawXZY[1])
            retVal[1] = self.__getSigned((rawXZY[2] << 8) | rawXZY[3])
            retVal[2] = self.__getSigned((rawXZY[4] << 8) | rawXZY[5])
        
        return retVal
    
    def getReg(self, register):
        """
        getReg(register)
        
        Gets the value of a given register. Returns an integer.
        """
        
        return self.__readReg(register)
    
    def setSamplingAverage(self, avg):
        """
        setSamplingAverage(avg)
        
        Sets sample averaging amount
        """
        
        # Compute the byte mask to preserve original register settings, minus the ones we want to set.
        mask = self.__regMask(self.__regAMA0 | self.__regAMA1)
        
        # Get the current register contents
        regContents = self.__readReg(self.regCfgA)
        
        # Clear the bits for the register using the mask
        newContents = (regContents & mask) | avg
        
        self.__writeReg(self.regCfgA, newContents)
    
    def setOutputFreq(self, freq):
        """
        setOutputFreq(freq)
        
        Set the HMC5883L's output frequency.
        """
        
        # Compute the byte mask to preserve original register settings, minus the ones we want to set.
        mask = self.__regMask(self.__regADO0 | self.__regADO1 | self.__regADO2)
        
        # Get the current register contents
        regContents = self.__readReg(self.regCfgA)
        
        # Clear the bits for the register using the mask
        newContents = (regContents & mask) | freq
        
        self.__writeReg(self.regCfgA, newContents)
    
    def setBias(self, bias):
        """
        setBias(bias)
        
        Set the HMC5883L's measurement bias mode
        """
        
        # Compute the byte mask to preserve original register settings, minus the ones we want to set.
        mask = self.__regMask(self.__regAMS0 | self.__regAMS1)
        
        # Get the current register contents
        regContents = self.__readReg(self.regCfgA)
        
        # Clear the bits for the register using the mask
        newContents = (regContents & mask) | bias
        
        self.__writeReg(self.regCfgA, newContents)
    
    def setGain(self, gain):
        """
        setGain(gain)
        
        Set the HMC883L's gain.
        """
        
        # Compute the byte mask to preserve original register settings, minus the ones we want to set.
        mask = self.__regMask(self.__regBGN0 | self.__regBGN1 | self.__regBGN2)
        
        # Get the current register contents
        regContents = self.__readReg(self.regCfgB)
        
        # Clear the bits for the register using the mask
        newContents = (regContents & mask) | gain
        
        self.__writeReg(self.regCfgB, newContents)
        
    def setMode(self, mode):
        """
        setGain(mode)
        
        Set the HMC5883L's operating mode.
        """
        
        # Compute the byte mask to preserve original register settings, minus the ones we want to set.
        mask = self.__regMask(self.__regMMD0 | self.__regMMD1)
        
        # Get the current register contents
        regContents = self.__readReg(self.regMode)
        
        # Clear the bits for the register using the mask
        newContents = (regContents & mask) | mode
        
        self.__writeReg(self.regMode, newContents)
    
    def setReg(self, register, value):
        """
        setReg(register, value)
        
        Manuall set the value of a given register. The writable registers on this chip are regCfgA (0x00), regCfgB (0x01), and regMode (0x02).
        """
        
        # Make sure we're trying to write to a R/W register
        if (register >= self.regCfgA) and (register <= self.regMode):
            self.__writeReg(register, value)
        else:
            raise ValueError("HMC5883L register must be writable to set it.")
    
