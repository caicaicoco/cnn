import os
import time
import torch
import torchvision
from torch import nn, optim
import sys

class LeNet(nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        
        # 输入 1 * 28 * 28
        self.conv = nn.Sequential(
            # 卷积层1
            # 在输入基础上增加了padding，28 * 28 -> 32 * 32
            # 1 * 32 * 32 -> 6 * 28 * 28
            nn.Conv2d(in_channels=1, out_channels=6, kernel_size=5, padding=2), nn.Sigmoid(),
            # 6 * 28 * 28 -> 6 * 14 * 14
            nn.MaxPool2d(kernel_size=2, stride=2), # kernel_size, stride
            # 卷积层2
            # 6 * 14 * 14 -> 16 * 10 * 10 
            nn.Conv2d(in_channels=6, out_channels=16, kernel_size=5), nn.Sigmoid(),
            # 16 * 10 * 10 -> 16 * 5 * 5
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.fc = nn.Sequential(
            # 全连接层1
            nn.Linear(in_features=16 * 5 * 5, out_features=120), nn.Sigmoid(),
            # 全连接层2
            nn.Linear(in_features=120, out_features=84), nn.Sigmoid(),
            nn.Linear(in_features=84, out_features=10)
        )

    def forward(self, img):
        feature = self.conv(img)
        output = self.fc(feature.view(img.shape[0], -1))
        return output

def load_data_fashion_mnist(batch_size, resize=None, root='~/Datasets/FashionMNIST'):
    """Use torchvision.datasets module to download the fashion mnist dataset and then load into memory."""
    trans = []
    if resize:
        trans.append(torchvision.transforms.Resize(size=resize))
    trans.append(torchvision.transforms.ToTensor())
    
    transform = torchvision.transforms.Compose(trans)
    mnist_train = torchvision.datasets.FashionMNIST(root=root, train=True, download=True, transform=transform)
    mnist_test = torchvision.datasets.FashionMNIST(root=root, train=False, download=True, transform=transform)
    if sys.platform.startswith('win'):
        num_workers = 0  
    else:
        num_workers = 4
    train_iter = torch.utils.data.DataLoader(mnist_train, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    test_iter = torch.utils.data.DataLoader(mnist_test, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    return train_iter, test_iter

def evaluate_accuracy(data_iter, net, device=None):
    if device is None and isinstance(net, torch.nn.Module):
        device = list(net.parameters())[0].device
    acc_sum, n = 0.0, 0
    with torch.no_grad():
        for X, y in data_iter:
            if isinstance(net, torch.nn.Module):
                # set the model to evaluation mode (disable dropout)
                net.eval() 
                # get the acc of this batch
                acc_sum += (net(X.to(device)).argmax(dim=1) == y.to(device)).float().sum().cpu().item()
                # change back to train mode
                net.train() 

            n += y.shape[0]
    return acc_sum / n

def try_gpu(i=0):
    if torch.cuda.device_count() >= i + 1:
        return torch.device(f'cuda:{i}')
    return torch.device('cpu')

def train(net, train_iter, test_iter, batch_size, optimizer, num_epochs, device=try_gpu()):
    net = net.to(device)
    print("training on", device)
    loss = torch.nn.CrossEntropyLoss()
    batch_count = 0
    for epoch in range(num_epochs):
        train_l_sum, train_acc_sum, n = 0.0, 0.0, 0
        for X, y in train_iter:
            X = X.to(device)
            y = y.to(device)
            y_hat = net(X)
            l = loss(y_hat, y)
            optimizer.zero_grad()
            l.backward()
            optimizer.step()
            train_l_sum += l.cpu().item()
            train_acc_sum += (y_hat.argmax(dim=1) == y).sum().cpu().item()
            n += y.shape[0]
            batch_count += 1
        test_acc = evaluate_accuracy(test_iter, net)
        if epoch % 10 == 0:
            print(f'epoch {epoch + 1} : loss {train_l_sum / batch_count:.3f}, train acc {train_acc_sum / n:.3f}, test acc {test_acc:.3f}')

def main():

    batch_size = 256
    lr, num_epochs = 0.9, 100

    net = LeNet()
    optimizer = torch.optim.SGD(net.parameters(), lr=lr)
    
    # load data
    train_iter, test_iter = load_data_fashion_mnist(batch_size=batch_size)
    # train
    train(net, train_iter, test_iter, batch_size, optimizer, num_epochs)

if __name__ == '__main__':
    main()