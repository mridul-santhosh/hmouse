import mraa
import time
import logging

def scan_i2c():
    """Scan for available I2C devices"""
    i2c = mraa.I2c(1)
    found_devices = []
    
    print("Scanning I2C bus...")
    for addr in range(0x03, 0x77):  # Valid I2C addresses
        try:
            i2c.address(addr)
            result = i2c.readByte()  # Try to read a byte
            found_devices.append(addr)
            print(f"Found device at address: 0x{addr:02X}")
        except:
            pass
    
    if not found_devices:
        print("No I2C devices found!")
    return found_devices

class Sensors:
    # Measurement modes for BH1750
    CONTINUOUS_HIGH_RES_MODE = 0x10
    CONTINUOUS_HIGH_RES_MODE_2 = 0x11
    CONTINUOUS_LOW_RES_MODE = 0x13
    ONE_TIME_HIGH_RES_MODE = 0x20
    ONE_TIME_HIGH_RES_MODE_2 = 0x21
    ONE_TIME_LOW_RES_MODE = 0x23

    # Power commands for BH1750
    POWER_ON = 0x01
    POWER_OFF = 0x00
    RESET = 0x07

    BH1750_DEFAULT_MTREG = 69
    BH1750_CONV_FACTOR = 1.2

    def __init__(self, addr=0x23, debug=False): # Default address is 0x23
        # Setup logging
        self.logger = logging.getLogger('BH1750')
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        
        self.addr = addr
        self.logger.info(f"Initializing BH1750 at address 0x{addr:02X}")
        
        try:
            # Initialize PIR and IR sensors
            self.pir = mraa.Gpio(7)
            self.pir.dir(mraa.DIR_IN)

            self.ir = mraa.Gpio(19)
            self.ir.dir(mraa.DIR_OUT)

            self.i2c = mraa.I2c(1)
            result = self.i2c.address(self.addr)

            self.interrupt_switch = mraa.Gpio(15)
            self.interrupt_switch.dir(mraa.DIR_IN)
            if result != 0:
                self.logger.error(f"Failed to set I2C address 0x{addr:02X}")
                raise IOError(f"Could not set I2C address 0x{addr:02X}")
            self.logger.debug("I2C initialization successful")
        except Exception as e:
            self.logger.error(f"I2C initialization fai2tr(e)}")
            raise
            
        self.mode = None
        self.mtreg = Sensors.BH1750_DEFAULT_MTREG

    def _write_byte_check(self, data, description=""):
        """Helper method to write byte and verify ACK"""
        try:
            result = self.i2c.writeByte(data)
            if result != 0:  # mraa returns 0 on success
                self.logger.error(f"Failed to write {description} (0x{data:02X}): No ACK received")
                raise IOError(f"No ACK received when writing {description}")
            self.logger.debug(f"Successfully wrote {description} (0x{data:02X})")
            return True
        except Exception as e:
            self.logger.error(f"Error writing {description} (0x{data:02X}): {str(e)}")
            raise

    def begin(self, mode):
        self.logger.info(f"Beginning measurement with mode 0x{mode:02X}")
        
        # Try power on sequence first
        try:
            self._write_byte_check(self.POWER_ON, "power on")
            time.sleep(0.01)
            self._write_byte_check(self.RESET, "reset")
            time.sleep(0.01)
        except Exception as e:
            self.logger.error(f"Power on sequence failed: {str(e)}")
            raise
            
        self.configure(mode)
        self.setMTreg(Sensors.BH1750_DEFAULT_MTREG)

    def configure(self, mode):
        valid_modes = [
            Sensors.CONTINUOUS_HIGH_RES_MODE,
            Sensors.CONTINUOUS_HIGH_RES_MODE_2,
            Sensors.CONTINUOUS_LOW_RES_MODE,
            Sensors.ONE_TIME_HIGH_RES_MODE,
            Sensors.ONE_TIME_HIGH_RES_MODE_2,
            Sensors.ONE_TIME_LOW_RES_MODE
        ]
        
        if mode not in valid_modes:
            self.logger.error(f"Invalid mode specified: 0x{mode:02X}")
            raise ValueError("Invalid mode")
            
        self._write_byte_check(mode, "measurement mode")
        self.mode = mode
        time.sleep(0.01)
        self.logger.debug(f"Mode configured: 0x{mode:02X}")

    def setMTreg(self, MTreg):
        self.logger.debug(f"Setting MTreg to {MTreg}")
        
        if MTreg < 31 or MTreg > 254:
            self.logger.error(f"Invalid MTreg value: {MTreg} (must be between 31 and 254)")
            raise ValueError("MTreg out of range")

        # Write high bits
        high_bits = 0b01000 << 3 | (MTreg >> 5)
        self._write_byte_check(high_bits, "MTreg high bits")

        # Write low bits
        low_bits = 0b011 << 5 | (MTreg & 0b11111)
        self._write_byte_check(low_bits, "MTreg low bits")

        # Write mode again
        self._write_byte_check(self.mode, "mode after MTreg")
        
        time.sleep(0.01)
        self.mtreg = MTreg
        self.logger.debug(f"MTreg successfully set to {MTreg}")

    def readLightLevel(self):
        if self.mode is None:
            self.logger.error("Attempt to read before configuration")
            raise RuntimeError("Device is not configured")

        try:
            data = self.i2c.read(2)
            self.logger.debug(f"Raw data read: [0x{data[0]:02X}, 0x{data[1]:02X}]")
            
            level = (data[0] << 8) | data[1]
            self.logger.debug(f"Combined raw value: {level}")
            
            level /= Sensors.BH1750_CONV_FACTOR
            level_adjusted = level
            
            if self.mtreg != Sensors.BH1750_DEFAULT_MTREG:
                level_adjusted *= (Sensors.BH1750_DEFAULT_MTREG / self.mtreg)
                self.logger.debug(f"Adjusted for MTreg: {level_adjusted:.2f}")
                
            if self.mode in [Sensors.ONE_TIME_HIGH_RES_MODE_2, Sensors.CONTINUOUS_HIGH_RES_MODE_2]:
                level_adjusted /= 2
                self.logger.debug(f"Adjusted for high res mode 2: {level_adjusted:.2f}")
                
            self.logger.debug(f"Final light level: {level_adjusted:.2f} lux")
            return level_adjusted
            
        except Exception as e:
            self.logger.error(f"Error reading light level: {str(e)}")
            raise

    def readPir(self):
        val = self.pir.read()
        return val
    
    def writeIr(self,value):
        self.ir.write(value)
    
    def getInterrupt(self):
        return self.interrupt_switch

