import asyncio
from os import read
from bleak import BleakClient
from bleak import BleakScanner

from pynput.keyboard import Key, Controller

gesture_dict = {0:'wait', 1:'swing', 2:'poke', 3:'error3', 4:'error4'}

class KeyboardInput:
    def __init__(self):
        self.keyboard = Controller()

    def inputKey(self, key):
        self.keyboard.press(key)
        self.keyboard.release(key)

    def inputKeyWithShift(self, key):
        with self.keyboard.pressed(Key.shift):
            self.keyboard.press(key)
            self.keyboard.release(key)

    def inputKeyWithControl(self, key):
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press(key)
            self.keyboard.release(key)

    def inputKeyWith(self, with_key, key):
        with self.keyboard.pressed(with_key):
            self.keyboard.press(key)
            self.keyboard.release(key)

    def typeString(self, string):
        self.keyboard.type(string)

address='' # MAC Address
uuids='00000000-0000-0000-0000-000000000021'
kb=KeyboardInput()

async def scan(): # MAC Address Scan
    global address
    devices = await BleakScanner.discover()
    for d in devices:
        if 'NEO_Player' in str(d):
            address=str(d).split(': ')[0]

async def run():
    global address
    async with BleakClient(address) as client:
        print('connected')
        flg=1
        while 1:
            services = await client.get_services()        
            for service in services:
                for characteristic in service.characteristics:
                    if characteristic.uuid==uuids:
                        read_data=await client.read_gatt_char(characteristic)
                        read_data=read_data[0]
                        if read_data==1 and flg:
                            kb.inputKey('j')
                            flg=0
                        elif read_data==2 and flg:
                            kb.inputKey('k')
                            flg=0
                        elif read_data==0:
                            flg=1
                            
    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(scan())
loop.run_until_complete(run())
print('done')