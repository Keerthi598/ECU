from time import sleep
from gpiozero import LED, PWMLED


'''
# GPIO Pins to be tested again
# Lots of error for now
# Looks like the LEDS cannot do stuff for too long
'''


class BreadBoard:
    """
    The individual BreadBoard Class that controls one specific BreadBoard
    
    Methods:
        __init__(self, uid, rGPIO, gGPIO, bGPIO):
            Initialize this BreadBoard and set all lights off
        
        get_uid(self):
            Get the uid of this BreadBoard

        curr_state(self):
            Get the current state of this BreadBoard in a List[R, G, B, Brightness]
        
        set_state(self, red, green, blue, brightness):
            Set the new state, then update the BreadBoard
    """

    def __init__(self, uid: int, rGPIO: int, gGPIO: int, bGPIO: int):
        '''
        Initialize the gpio pins, and set everything else to 0 \n

        @params: self
        @params: uid: The uid of this breadboard
        @params: rGPIO: The GPIO pin number of red
        @params: gGPIO: The GPIO pin number of green
        @params: bGPIO: The GPIO pin number of blue
        '''

        self.__uid = uid
        self.__red = 0
        self.__blue = 0
        self.__green = 0
        self.__brightness = 0
        
        self.__red_led = PWMLED(rGPIO, active_high=True)
        self.__green_led = PWMLED(gGPIO, active_high=True)
        self.__blue_led = PWMLED(bGPIO, active_high=True)

        # Testing
        #self.__red_led.value = 1
        #self.__green_led.value = 1
        #self.__blue_led.value = 1  

    def get_uid(self):
        '''
        Get the UID of this BreadBoard

        @params: self
        @returns: uid: The UID of this BreadBoard
        '''

        return self.__uid
    
    def curr_state(self):
        '''
        Returns the current state of this BreadBoard's Red, Green, Blue and Brightness values

        @params: self
        @returns: List[Red, Green, Blue, Brightness]
        '''

        return self.__red, self.__green, self.__blue, self.__brightness
    
    def set_state(self, red: int, green: int, blue: int, brightness: int):
        '''
        Sets the current state of this BreadBoard \n
        Calls update function

        @params: self
        @params: red: The Red Value
        @params: green: The Green Value
        @params: blue: The Blue Value
        @params: brightness: The Brightness Value
        @returns: None
        '''
        self.__red = red
        self.__green = green
        self.__blue = blue
        self.__brightness = brightness

        # Update current breadboard to be done
        self.__update_board()
        
    def __update_board(self):
        '''
        Updates the GPIO pins based on the value of rgb and brightness \n
        Called By Set State

        @params: self
        @returns: None
        '''
        temp_r = self.__red / 255
        temp_r = temp_r * self.__brightness / 100
        self.__red_led.value = temp_r if temp_r <= 1 else 1
        
        temp_g = self.__green / 255
        temp_g = temp_g * self.__brightness / 100
        self.__green_led.value = temp_g if temp_g <= 1 else 1
        
        temp_b = self.__blue / 255
        temp_b = temp_b * self.__brightness / 100
        self.__blue_led.value = temp_b if temp_b <= 1 else 1
        
        return

'''
Test Pins
red_pin = 17
green_pin = 27
blue_pin = 22
'''

def main():
    # Try Pins Far Away
    test = BreadBoard(1, 17, 12, 26)
    print("Test Started")
    
    test.set_state(255, 0, 0, 100)
    sleep(2)
    test.set_state(0, 255, 0, 100)
    sleep(2)
    test.set_state(0, 0, 255, 100)
    sleep(2)
    test.set_state(0, 0, 0, 0)
    
    sleep(5)
    print("Test Completed")

if __name__ == "__main__":
    main()
