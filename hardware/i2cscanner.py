from machine import Pin, SoftI2C
i2c = SoftI2C(sda=Pin(20), scl=Pin(21), freq=200000)

#sda = machine.Pin(0)
#scl = machine.Pin(1)
#i2c=machine.I2C(0,sda=sda, scl=scl, freq=200000)

print(i2c)
print('Scan i2c bus...')
devices = i2c.scan()
print(devices)

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))
 
  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))
    
    