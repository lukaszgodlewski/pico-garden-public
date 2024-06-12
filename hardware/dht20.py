from machine import I2C
from utime import sleep_ms

class DHT20:   
    def __init__(self, address: int, i2c: I2C):
        self._address = address
        self._i2c = i2c
        sleep_ms(100)
        
        if not self.is_ready:
            self._initialize()
            sleep_ms(100)
            
            if not self.is_ready:
                raise RuntimeError("Could not initialize the DHT20.")
        
    @property
    def is_ready(self) -> bool:
        self._i2c.writeto(self._address, bytearray(b'\x71'))
        return self._i2c.readfrom(self._address, 1)[0] == 0x18
    
    def _initialize(self):
        buffer = bytearray(b'\x00\x00')
        self._i2c.writeto_mem(self._address, 0x1B, buffer)
        self._i2c.writeto_mem(self._address, 0x1C, buffer)
        self._i2c.writeto_mem(self._address, 0x1E, buffer)
    
    def _trigger_measurements(self):
        self._i2c.writeto_mem(self._address, 0xAC, bytearray(b'\x33\x00'))
        
    def _read_measurements(self):
        buffer = self._i2c.readfrom(self._address, 7)
        return buffer, buffer[0] & 0x80 == 0
    
    def _crc_check(self, input_bitstring: str, check_value: str) -> bool:       
        polynomial_bitstring = "100110001"
        len_input = len(input_bitstring)
        initial_padding = check_value
        input_padded_array = list(input_bitstring + initial_padding)
        
        while '1' in input_padded_array[:len_input]:
            cur_shift = input_padded_array.index('1')
            
            for i in range(len(polynomial_bitstring)):
                input_padded_array[cur_shift + i] = \
                    str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
                
        return '1' not in ''.join(input_padded_array)[len_input:]
        
    @property
    def measurements(self) -> dict:
        self._trigger_measurements()
        sleep_ms(50)
        
        data = self._read_measurements()
        retry = 3
        
        while not data[1]:
            if not retry:
                raise RuntimeError("Could not read measurements from the DHT20.")
            
            sleep_ms(10)
            data = self._read_measurements()
            retry -= 1
            
        buffer = data[0]
        s_rh = buffer[1] << 12 | buffer[2] << 4 | buffer[3] >> 4
        s_t = (buffer[3] << 16 | buffer[4] << 8 | buffer[5]) & 0xfffff
        rh = (s_rh / 2 ** 20) * 100
        t = ((s_t / 2 ** 20) * 200) - 50
        crc_ok = self._crc_check(
            f"{buffer[0] ^ 0xFF:08b}{buffer[1]:08b}{buffer[2]:08b}{buffer[3]:08b}{buffer[4]:08b}{buffer[5]:08b}",
            f"{buffer[6]:08b}")
        
        return {
            't': t,
            'rh': rh
        }