from Lightning import Lightning
import asyncio
import socket

class ECU:
    """
    Sets up the entire lighting control system  and creates the clients to communicate with BLE and IVI

    Methods:
        __init__(self):
            Initializes the Lighting Control System
        
        start(self):
            Main point of entry. Starts the program
    """

    def __init__(self) -> None:
        '''
        Constructor \n
        Initializes lighting \n
        Sets flashing to false \n
        Init curr state to empty byte array

        @params: self
        '''
        self.__light = Lightning()
        self.__light.bread_set()
        self.__flashing = False
        self.__req = bytearray(33)
        self.__c_state = bytearray(33)
        return

    #
    # BLE Connection
    #
    
    async def __run_ble_server(self):
        '''
        Sets Up a sever to connect to the ble client on the port 6789 \n
        Runs asynchronously in a perpetual loop \n
        Runs handle_ble when a connection is made and returns to the loop

        @param: self
        @return: none
        ''' 
         
        ble_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ble_server.bind(('localhost', 6789))
        ble_server.listen(1)
        ble_server.setblocking(False)
        
        loop = asyncio.get_event_loop()
        
        while True:
            client, _ = await loop.sock_accept(ble_server)
            await self.__handle_ble(client)

    async def __handle_ble(self, client):
        '''
        Runs when the BLE client connects to port 6789 to send a request \n
        Receives the request and closes the connection so that the port can wait for the next connection \n
        Calls the update function

        @params: self
        @params: client: The Instance of BLE client socket
        @returns: none
        '''
        loop = asyncio.get_event_loop()
        data = await loop.sock_recv(client, 33)
        self.__req = data
        client.close()

        await self.__update(request=data)
        return
        
    #
    # IVI Connectionindex

    async def __run_ivi_server(self):
        '''
        Sets Up a sever to connect to the IVI client on the port 65432 through the network \n
        Runs asynchronously in a perpetual loop \n
        Runs handle_ivi when a connection is made and returns to the loop

        @param: self
        @return: none
        ''' 

        ivi_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ivi_server.bind(('', 65432))
        ivi_server.listen(1)
        ivi_server.setblocking(False)
        
        loop = asyncio.get_event_loop()
        
        while True:
            client, _ = await loop.sock_accept(ivi_server)
            await self.__handle_ivi(client)

    async def __handle_ivi(self, client):
        '''
        Runs when the IVI client connects to port 65432 to send a request \n
        Receives the request and closes the connection so that the port can wait for the next connection \n
        Calls the update function

        @params: self
        @params: client: The Instance of IVI client socket
        @returns: none
        '''

        loop = asyncio.get_event_loop()
        data = await loop.sock_recv(client, 33)
        self.__req =data
        client.close()

        await self.__update(request=data)
        return

    #
    # Update Sequence
    #

    async def __update(self, request: bytearray):
        '''
        Update the Ligthing controls according to the given request \n
        Converts the byte array to be readble and updates according to the 
        appropriate status index \n
        Returns update to BLE and then to IVI

        @params: self
        @params: request: The request byte array
        @returns: none
        '''

        converted_data = list(request)
        status_index = converted_data[0]
        self.__c_state = request

        if status_index == 0:
            ##
            ## Do Nothing
            ## No request from either IVI or Phone
            return

        elif status_index == 16 or status_index == 1 or status_index == 48:
            ##
            ## Continue the request as normal
            ## Nothing additional to be done
            pass

        elif status_index == 32:
            ##
            ## Flashing
            ## Handled by the other RaspBerry Pi
            pass


        elif status_index == 64:
            ##
            ## Turn everything off
            ## Set status index of the encoding to 0x00
            self.__c_state = bytearray(33)

        elif status_index == 80:
            ##
            ## Turn everything off
            ## Set status byte to 0x10 
            self.__c_state = bytearray(33)
            self.__c_state[0] = 16

        elif status_index == 96:
            ##
            ## Set all to max brightness and all white
            ## Set status byte to 0x10
            zero = bytearray([16])
            pattern = bytearray([100, 255, 255, 255])
            zero.extend(pattern * 8)
            self.__c_state = zero

        # Send curr State to Both, Brian and BLE
        # await self.__update_ble(curr_state)
        # await self.__update_ivi(curr_state)
    
    async def __update_ble(self):
        '''
        Update the BLE regarding the change  \n
        Connect to Port 9876, send data, then close connection

        @params: self
        @params: data: The current state of the lighting
        @returns: none
        '''
        loop = asyncio.get_event_loop()
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        await loop.sock_connect(client,('localhost', 9876))
        await loop.sock_sendall(client, self.__c_state)
    
        client.close()
        return

    async def __update_ivi(self):
        '''
        Update the IVI regarding the change \n
        Connect to Port [To Be Decided], send data, then close connection

        @params: self
        @params: data: The current state of the lighting
        @returns: none
        '''
        loop = asyncio.get_event_loop()
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #
        # Need to change Port Number
        #
        await loop.sock_connect(client,('', 65432))
        await loop.sock_sendall(client, self.__c_state)
    
        client.close()
        return

    #
    # Startup and Init Sequence
    #

    async def __routine(self):
        '''
        Handles the flashing functionality \n
        Do nothing if not flashing

        @params: self
        @returns: none
        '''
        while True:
            if not self.__flashing:
                await asyncio.sleep(1)
                continue

            self.__light.decode(self.__req)
            curr_state = self.__light.encode()
            curr_state[0] = 32
            await asyncio.sleep(0.5)

            self.__light.decode(bytearray(33))
            curr_state = self.__light.encode()
            curr_state[0] = 32

            await asyncio.sleep(0.5)

    async def start(self):
        '''
        Main point of entry for this program \n
        Adds run_ble_server and run_ivi_server 
        to the list of async tasks

        @params: none
        @returns: none
        '''

        await asyncio.gather(self.__run_ble_server())
        # await asyncio.gather(self.__routine(), self.__run_ble_server(),self.__run_ivi_server())
   

def main():
    ecu = ECU()
    asyncio.run(ecu.start())


if __name__ == "__main__":
    main()
