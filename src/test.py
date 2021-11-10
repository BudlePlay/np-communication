import serial
from collections import deque
from pynput.keyboard import Key, Controller
import time

ser = serial.Serial("COM4", 115200, timeout=1)

q = deque(maxlen=15)

import torch

model = torch.load('model.pth', map_location=torch.device('cpu'))
model.eval()

gesture_dict = {0: 'w', 1: 'swing', 2: 'poke', 3: '', 4: ''}


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


kb = KeyboardInput()


class CMemory:
    def __init__(self):
        self.q = deque()
        self.can_add = False

    def add(self, data):
        if self.can_add:
            self.q.append(data)

    def allow_add(self):
        self.can_add = True

    def block_add(self):
        self.can_add = False

    def end_check(self): # swing이나 poke후 다시 wait 인지 확인
        if len(self.q) > 3: # clear된 직후에는 판정 안되게
            for i in range(1, 4):
                if self.q[-1 * i] != 0:
                    return False
        else:
            return False

        self.block_add()
        return True


prev_gesture = 0
prev_time=0
memory = CMemory()
while True:
    data = ser.readline().decode('utf-8').strip()
    data = data.split(',')

    for i in range(6):
        data[i] = float(data[i])

    q.append(data)
    if len(q) >= 15:
        input_tenser = torch.tensor(q)

        accel = input_tenser[:, 0:3]
        gyro = input_tenser[:, 3:7]
        accel = accel
        gyro = gyro

        out = model(accel.unsqueeze(0), gyro.unsqueeze(0))
        gesture = out.argmax().item()

        if prev_gesture != gesture and gesture != 0: # 저번 제스처가 아니면서 wait가 아닐 때
            memory.allow_add()

        memory.add(gesture)

        if memory.end_check():
            print(memory.q)
            if len(memory.q)>=5 and time.time()-prev_time>2: # memory에 충분한 데이터가 쌓여있는지 확인
                if memory.q.count(1)>memory.q.count(2): # swing 인지 poke 인지 판단
                    print('swing')
                    ser.write(bytes(b'1'))
                    # kb.inputKey('j')
                else:
                    print('poke')
                    ser.write(bytes(b'2'))
                    # kb.inputKey('k')
                prev_time=time.time()
            memory.q.clear()

        # print(gesture_dict[gesture])

        prev_gesture = gesture
        # kb.inputKey('J')
