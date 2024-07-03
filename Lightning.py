from time import sleep
from BreadBoard import BreadBoard

class Lightning:
    '''
    Control the entire BreadBoard System

    Methods:
        __init__(self):
            Initializes the BreadBoards
        
        start(self):
            Main point of entry. Starts the program
    '''
    def __init__(self):
        '''
        Initializes the list for BreadBoards

        @params: self
        '''
        self.__breadboards = []
        
    def bread_set(self):
        '''
        Creates the BreadBoards with their respective GPIO pins

        @params: self
        @returns: None
        '''
        #GPIO pins to be checked and verified - most likely to be changed
        
        b1 = BreadBoard(0,26,19,13)
        self.__breadboards.append(b1)
        '''
        b2 = BreadBoard(1,24,11,17)
        self.__breadboards.append(b2)
        b3 = BreadBoard(2,2,3,4)
        self.__breadboards.append(b3)
        b4 = BreadBoard(3,27,22,10)
        self.__breadboards.append(b4)
        b5 = BreadBoard(4, 5,6,9)
        self.__breadboards.append(b5)
        b6 = BreadBoard(5,16,20,21)
        self.__breadboards.append(b6)
        '''
        
    def decode(self, request: bytearray):
        '''
        Decode and process the request bytearray

        @params: self
        @params: request: The ByteArray to be processed
        @return: None
        '''

        converted_list = list(request)
        
        if len(converted_list) != 33:
            return

        # Index 0 handled by ECU
        index = 1

        for bread_board in self.__breadboards:
            bread_board.set_state(converted_list[index + 1], converted_list[index + 2], converted_list[index + 3], converted_list[index])
            index += 4

        return

    def encode(self):
        '''
        Encodes the current state into a byte array and returns it

        @params: self
        @returns: ByteArray: The encoded ByteArray containing the current state
        '''
        demand = [0 for i in range(33)]  # Don't judge the variable name
        i = 1

        for bread_board in self.__breadboards:
            r,g,b,brightness = bread_board.curr_state()
            demand[i] = brightness
            demand[i+1] = r
            demand[i+2] = g
            demand[i+3] = b
            i +=4
        
        return bytearray(demand)

'''
Test Pins
red_pin = 26
green_pin = 13
blue_pin = 19
'''

def main():
    # test = Lightning()
    # test.bread_set()
    # test.decode(bytearray([0, 100, 255, 255, 255]))
    # sleep(4)
    # print("")
    
    z = bytearray([0,10,20,48,64,80,96])
    #d = list(z)
    for i in z:
        print(i)
    
    # print(list(test.encode()))


if __name__ == "__main__":
    main()



