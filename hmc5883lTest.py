# hmc5883l class by ThreeSixes (https://github.com/ThreeSixes/py-hmc5883l)

from hmc5883l import hmc5883l
from pprint import pprint

# Set up our magnetometer
magSens = hmc5883l()

# Test everything related to config register A.

# Changing register A could be more efficiently achieved using this:
# magSens.setReg(magSens.regCfgA, (magSens.avg1 | magSens.freq15 | magSens.biasNone))
# Test the methods that individually set all register A's settings:
regA = magSens.getReg(magSens.regCfgA)
magSens.setSamplingAverage(magSens.avg1)
magSens.setOutputFreq(magSens.freq15)
magSens.setBias(magSens.biasNone)
print("Reg A:    " + hex(regA) + " -> " + hex(magSens.getReg(magSens.regCfgA)))

# Test everything related to config register B.

# Changing register B could be more efficiently achieved using this:
# magSens.setReg(magSens.regCfgB, magSens.gain230)
# Test the methods that individually set all register B's settings:
regB = magSens.getReg(magSens.regCfgB)
magSens.setGain(magSens.gain230)
print("Reg B:    " + hex(regB) + " -> " + hex(magSens.getReg(magSens.regCfgB)))

# Test everything related to mode register.

# Changing the mode register could be more efficiently achieved using this:
# magSens.setReg(magSens.regMode, magSens.modeCont)
# Test the methods that individually set all register A's settings:
regMode = magSens.getReg(magSens.regMode)
magSens.setMode(magSens.modeCont)
print("Reg Mode: " + hex(regMode) + " -> " + hex(magSens.getReg(magSens.regMode)))

# Status?
print("Status:   " + hex(magSens.getStatus()))

# Read from the magnetometer.
xzy = magSens.getXZY()

pprint(xzy)
print(hex(xzy[0]))
print(hex(xzy[1]))
print(hex(xzy[2]))
