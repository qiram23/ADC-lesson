import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
troykaModule=17
comparator = 4

def decimal2binary(decimal):
    return[int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def num2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac,signal)
    return signal

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(troykaModule, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comparator, GPIO.IN)

signal=0
value=0

try:
    for i in range(bits-1, -1, -1):
        value+=2**i
        signal=num2dac(value)
        print(value, signal)
        voltage=value / levels * maxVoltage
        comparatorValue=GPIO.input(comparator)
        print(comparatorValue)
        time.sleep(0.1)
        if comparatorValue==0:
            value-=2**i
    print("ADC value = {:^3} -> {}, input voltage = {:.2f}".format(value, signal, voltage))

except KeyboardInterrupt:
    print('\nThe program was stopped by the keyboard')
else:
    print('No exceptions')
finally:
    GPIO.output(dac,GPIO.LOW)
    GPIO.cleanup(dac)
    print("GPIO cleanup completed")