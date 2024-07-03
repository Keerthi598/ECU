from time import sleep
from gpiozero import LED, PWMLED

class BreadBoard:
    def __init__(self, uid: int, rGPIO: int, gGPIO: int, bGPIO: int):
        self.__uid = uid
        self.__red = 0
        self.__blue = 0
        self.__green = 0
        self.__brightness = 0
        self.__rGPIO = rGPIO
        self.__gGPIO = gGPIO
        self.__bGPIO = bGPIO
        
        self.__red_led = PWMLED(rGPIO, active_high=True)
        self.__green_led = PWMLED(gGPIO, active_high=True)
        self.__blue_led = PWMLED(bGPIO, active_high=True)
        
    def get_uid(self):
        return self.__uid
    
    def curr_state(self):
        return self.__red, self.__blue, self.__green, self.__brightness
    
    def set_state(self, red: int, blue: int, green: int, brightness: int):
        self.__red = red
        self.__blue = blue
        self.__green = green
        self.__brightness = brightness
        # Update current breadboard to be done
        self.update_board()
        
    def update_board(self):
        # Update the board
        # Flashing Not Implemented Yet
        temp_r = self.__red / 255
        temp_r = temp_r * self.__brightness / 100
        self.__red_led.value = temp_r if temp_r <= 1 else 1
        
        temp_g = self.__green / 255
        temp_g = temp_g * self.__brightness / 100
        self.__green_led.value = temp_g if temp_g <= 1 else 1
        
        temp_b = self.__blue / 255
        temp_b = temp_b * self.__brightness / 100
        self.__blue_led.value = temp_b if temp_b <= 1 else 1
        pass

'''
Test Pins
red_pin = 26
green_pin = 13
blue_pin = 19
'''

def main():
    test = BreadBoard(1,26,13,19)
    test.set_state(255, 0, 0, 100)
    sleep(2)
    test.set_state(0, 255, 0, 100)
    sleep(2)
    test.set_state(0, 0, 255, 100)
    sleep(2)
    test.set_state(0, 0, 0, 0)

    print("Hello World")

if __name__ == "__main__":
    main()
