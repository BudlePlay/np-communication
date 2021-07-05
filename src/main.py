import asyncio
from bleak import BleakClient
from bleak import BleakScanner

from pynput.keyboard import Key, Controller

import struct

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
uuids=[
    '00000000-0000-0000-0000-000000000021',
    '00000000-0000-0000-0000-000000000022',
    '00000000-0000-0000-0000-000000000023',
    '00000000-0000-0000-0000-000000000024',
    '00000000-0000-0000-0000-000000000025',
    '00000000-0000-0000-0000-000000000026'
]

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
        data=[0,0,0,0,0,0]
        while 1:
            services = await client.get_services()        
            for service in services:
                for characteristic in service.characteristics:
                    cnt=0
                    for i in uuids:
                        if characteristic.uuid==i:
                            data[cnt]=round(struct.unpack('f', await client.read_gatt_char(characteristic))[0],2) 
                        cnt+=1
                        print(data)
    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(scan())
loop.run_until_complete(run())
print('done')