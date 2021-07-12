import torch
import torch.nn as nn


class GestureClassifier(nn.Module):
    def __init__(self, input_size=20 * 3):
        super(GestureClassifier, self).__init__()
        self.input_size = input_size

        self.relu = nn.ReLU()

        self.cnn_1 = nn.Conv1d(6, 32, kernel_size=3)
        self.cnn_2 = nn.Conv1d(32, 32, kernel_size=3)
        self.cnn_3 = nn.Conv1d(32, 32, kernel_size=3)
        self.fc_1 = nn.Linear(288, 288)
        self.fc_2 = nn.Linear(288, 5)


    def forward(self, accel, gyro):
        x = torch.cat((accel, gyro), dim=2)
        x = x.permute(0, 2, 1)
        x = self.cnn_1(x)
        x = self.cnn_2(x)
        x = self.cnn_3(x)
        x = x.view(x.shape[0], -1)
        x = self.fc_1(x)
        x = self.relu(x)
        x = self.fc_2(x)

        return x