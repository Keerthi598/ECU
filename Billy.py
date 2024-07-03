import asyncio, socket

from bless import BlessServer, BlessGATTCharacteristic
from bless import GATTCharacteristicProperties, GATTAttributePermissions

# Set Up GATT Servver
class Billy:
    
    def __read_request(characteristic: BlessGATTCharacteristic, **kwargs) -> bytearray:
        return characteristic.value

    def __write_request(characteristic: BlessGATTCharacteristic, value: bytes, **kwargs):
        characteristic.value = value

    def __init__(self) -> None:
        # Init 2 uuids
        self.__s_uuid = "A07498CA-AD5B-474E-940D-16F1FBE7E8CD"
        self.__char_req_uuid = "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B"
        self.__char_cur_uuid = "97493F10-52D8-4F50-962D-B546CC16D1D6"

        self.__server =  None
        self.__prev_value = bytearray(33)
        return

    async def init_billy(self, loop):
        # Inititialized by parent
        self.__server =  BlessServer(name="MyBilly", loop=loop)

        self.__server.read_request_func = self.__read_request
        self.__server.write_request_func = self.__write_request


        await self.__server.add_new_service(self.__s_uuid)

        # Request Characteristic
        await self.__server.add_new_characteristic(self.__s_uuid,
                self.__char_req_uuid, (
                GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write
                | GATTCharacteristicProperties.indicate
                ),bytearray(33), (
                GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable
                ))
        
        # Current Characteristic
        await self.__server.add_new_characteristic(self.__s_uuid,
                self.__char_cur_uuid, (
                GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write
                | GATTCharacteristicProperties.indicate
                ),bytearray(33), (
                GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable
                ))
        
        await self.__server.start()
        
        # await asyncio.gather(self.check_phone(), self.check_ecu())

        await asyncio.sleep(5)
        print("Hello")

        await self.__server.stop()
        
    async def check_phone(self):
        # Check For changes from Phone
        while True:
            current = self.__server.get_characteristic(self.__char_req_uuid).value

            if current == self.__prev_value:
                await asyncio.sleep(1)

            else:
                await self.update_ecu(current)
                await asyncio.sleep(2)
              
    async def update_ecu(self, data: bytearray):
        # Send request data to the ECU
        # Connect to Socket 6789
        # Return
        loop = asyncio.get_event_loop()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        await loop.sock_connect(client,('localhost', 6789))
        await loop.sock_sendall(client, data)
    
        client.close()
        
        return  


    async def check_ecu(self):
        # Check for changes from Ecu
        # Listen to socket 9876
        # Update phone
        ecu_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ecu_conn.bind(('localhost', 9876))
        ecu_conn.listen(1)
        ecu_conn.setblocking(False)
        
        loop = asyncio.get_event_loop()
        
        while True:
            client, _ = await loop.sock_accept(ecu_conn)
            await self.update_phone(client)
        
    async def update_phone(self, client):
        # Update the current state to the phone
        # Change The characteristic of gatt server
        # Update the prev_state
        loop = asyncio.get_event_loop()
        data = await loop.sock_recv(client, 33)
        client.close()

        self.__prev_value = data
        self.__server.get_characteristic(self.__char_cur_uuid).value = data
        
        return
    



def main():
    test = Billy()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test.init_billy(loop))



if __name__ == "__main__":
    main()
