import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class StepMotor:
    Pins = [0, 0, 0, 0]
    
    StepCount = 8
    Seq = [
        [0, 0, 0, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 1]
        ]

    def __init__(self, a1, a2, b1, b2):
        self.Pins [0] = a1
        self.Pins [1] = a2
        self.Pins [2] = b1
        self.Pins [3] = b2

    def setGPIO (self):
        for i in range(4):
            GPIO.setup(self.Pins[i], GPIO.OUT)

    def setStep (self, w1, w2, w3, w4):
        self.setGPIO()
        GPIO.output(self.Pins[0], w1)
        GPIO.output(self.Pins[1], w2)
        GPIO.output(self.Pins[2], w3)
        GPIO.output(self.Pins[3], w4)

    def forward(self, delay, steps):
        for i in range(steps):
            for j in range(self.StepCount):
                self.setStep(self.Seq[j][0], self.Seq[j][1], self.Seq[j][2], self.Seq[j][3])
                time.sleep(delay)
        self.setStep(0, 0, 0, 0)
    
    def backward(self, delay, steps):
        for i in range(steps):
            for j in reversed(range(self.StepCount)):
                self.setStep(self.Seq[j][0], self.Seq[j][1], self.Seq[j][2], self.Seq[j][3])
                time.sleep(delay)
        self.setStep(0, 0, 0, 0)
        
if __name__ == '__main__':
    stepM = StepMotor(12, 16, 20, 21)
    stepM.forward(0.001, 512)
    stepM.backward(0.001, 512)
    GPIO.cleanup()

