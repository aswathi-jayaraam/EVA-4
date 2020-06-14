import torch  # Import pytorch library
import torch.nn as nn  # Import neural net module from pytorch
import torch.nn.functional as F  # Import functional interface from pytorch


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        # PREP LAYER
        self.input_layer = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=64, kernel_size=(3, 3), padding=(1, 1), stride=(1, 1), bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU()
        )

        # LAYER 1
        self.layer1 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=(3, 3), padding=(1, 1), stride=(1, 1), bias=False),
            nn.MaxPool2d(2, 2),
            nn.BatchNorm2d(128),
            nn.ReLU()
        )

        # RESNET BLOCK 1
        self.resblock1 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3, 3), padding=(1, 1), stride=(1, 1), bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3, 3), padding=(1, 1), stride=(1, 1), bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU()
        )

        # LAYER 2
        self.layer2 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=(3, 3), padding=(1, 1), stride=(1, 1), bias=False),
            nn.MaxPool2d(2, 2),
            nn.BatchNorm2d(256),
            nn.ReLU()
        )

        # LAYER 3
        self.layer3 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=512, kernel_size=(3, 3), padding=(1, 1), stride=(1, 1), bias=False),
            nn.MaxPool2d(2, 2),
            nn.BatchNorm2d(512),
            nn.ReLU()
        )

        # RESNET BLOCK 2
        self.resblock2 = nn.Sequential(
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=(3, 3), padding=(1, 1), stride=(1, 1), bias=False),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=(3, 3), padding=(1, 1), stride=(1, 1), bias=False),
            nn.BatchNorm2d(512),
            nn.ReLU()
        )

        # MAXPOOL
        self.pool1 = nn.Sequential(
            nn.MaxPool2d(4, 4)
        )

        # OUTPUT
        self.linear = nn.Sequential(
            nn.Linear(in_features=512, out_features=10)
        )

    def forward(self, x):
        # PREP LAYER
        x = self.input_layer(x)

        # LAYER 1
        x = self.layer1(x)

        # RESNET BLOCK 1
        r1 = self.resblock1(x)
        x = x + r1

        # LAYER 2
        x = self.layer2(x)

        # LAYER 2
        x = self.layer3(x)

        # RESNET BLOCK 2
        r2 = self.resblock2(x)
        x = x + r2

        # MAX POOL
        x = self.pool1(x)
        x = torch.flatten(x, 1)

        # LINEAR
        x = self.linear(x)

        return F.log_softmax(x, dim=-1)