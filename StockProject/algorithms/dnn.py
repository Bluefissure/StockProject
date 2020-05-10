import torch
import torch.nn.functional as F
import codecs
import numpy as np
import matplotlib.pyplot as plt

class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, n_hidden)
        self.predict = torch.nn.Linear(n_hidden, n_output)

    def forward(self, x):
        x = F.relu(self.hidden(x))
        x = self.predict(x)
        return x

def load_data():
    x = []
    with codecs.open("data", "r", "utf8") as f:
        lines = f.readlines()
        for line in lines:
            if not line: continue
            d = line.split('\t')
            x.append(d)
    x = np.array(x, dtype='float32')
    y = x[1:, 0]
    x = x[:-1]
    print("x.shape:{}".format(x.shape))
    print("y.shape:{}".format(y.shape))
    return x, y



if __name__ == '__main__':
    net = Net(n_feature=4, n_hidden=30, n_output=1)

    x, y = load_data()
    x = torch.from_numpy(x)
    y = torch.from_numpy(y)

    optimizer = torch.optim.Adam(net.parameters(), lr=0.05)
    loss_func = torch.nn.MSELoss()

    plt.scatter(range(x.shape[0]), y.data.numpy())
    plt.show()

    for t in range(100000):
        prediction = net(x)

        loss = loss_func(prediction, y)
        print("step: {}\tloss:{}".format(t, loss))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if t % 20000 == 0:
            # plot and show learning process
            plt.cla()
            plt.scatter(range(x.shape[0]), y.data.numpy())
            plt.plot(range(1, x.shape[0]+1), prediction.data.numpy(), 'r-', lw=5)
            plt.text(0.5, 0, 'Loss=%.4f' % loss.data.numpy(), fontdict={'size': 20, 'color':  'red'})
            print(prediction)
            plt.show()

