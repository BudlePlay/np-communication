import torch
import torch.nn as nn


class GestureClassifier(nn.Module):
    def __init__(self, input_size=20*3):
        super(GestureClassifier, self).__init__()
        self.input_size = input_size

        self.relu = nn.ReLU()

        self.accel_fc1 = nn.Linear(input_size, 64)
        self.gyro_fc1 = nn.Linear(input_size, 64)

        self.fc2 = nn.Linear(64*2, 32)
        self.fc3 = nn.Linear(32, 5)

    def forward(self, accel, gyro):
        accel_x = self.accel_fc1(accel)
        gyro_x = self.gyro_fc1(gyro)
        accel_x = self.relu(accel_x)
        gyro_x = self.relu(gyro_x)

        x = torch.cat((accel_x, gyro_x), dim=1)

        x = self.fc2(x)
        x = self.relu(x)

        return self.fc3(x)