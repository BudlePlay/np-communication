import asyncio
from bleak import BleakClient
from bleak import BleakScanner
import time

from pynput.keyboard import Key, Controller
from collections import deque
import struct
import torch

model = torch.load('model.pth', map_location=torch.device('cpu'))
model.eval()

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
        q=deque(maxlen=15)
        while 1:
            data=[0,0,0,0,0,0]
            services = await client.get_services()        
            for service in services:
                for characteristic in service.characteristics:
                    cnt=0
                    for i in uuids:
                        if characteristic.uuid==i:
                            data[cnt]=round(struct.unpack('f', await client.read_gatt_char(characteristic))[0],2)
                        cnt+=1
            # print(data)
            q.append(data)

            if len(q)>=15:
                input_tenser = torch.tensor(q)

                accel = input_tenser[:, 0:3]
                gyro = input_tenser[:, 3:7]
                accel = accel.reshape(-1)
                gyro = gyro.reshape(-1)

                out = model(accel.unsqueeze(0), gyro.unsqueeze(0))
                gesture = out.argmax().item()


                print(gesture_dict[gesture])
                

                        
    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(scan())
loop.run_until_complete(run())
print('done')