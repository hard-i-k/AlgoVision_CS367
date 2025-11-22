import numpy as np
import matplotlib.pyplot as plt


class HopfieldNet:

    def __init__(self, n_units):
        # total number of neurons in the network
        self.n = n_units
        # weight matrix for storing pattern associations
        self.wt = np.zeros((n_units, n_units))

    def learn(self, patt_list):
        # stores each pattern using Hebbian learning
        for p in patt_list:
            p = p.reshape(self.n, 1)
            self.wt += (p @ p.T) / self.n      # weight update rule
        # remove self-connections
        np.fill_diagonal(self.wt, 0)

    def update(self, vec, iters=6):
        # performs iterative recall to recover the stored pattern
        out = vec.copy()
        for _ in range(iters):
            out = np.sign(self.wt @ out)        # compute next state
            out[out == 0] = 1                   # ensure no zero values
        return out


def convert_to_binary(mat):
    # convert a 0/1 matrix into -1/+1 vector suitable for Hopfield network
    arr = np.array(mat)
    return np.where(arr == 0, -1, 1).reshape(-1)


def inject_noise(vec, ratio=0.25):
    # flips a selected percentage of pattern bits to add noise
    noisy = vec.copy()
    num = int(ratio * len(vec))
    idx = np.random.permutation(len(vec))[:num]
    noisy[idx] *= -1
    return noisy


def show(img, title=""):
    # displays a 10x10 pattern as an image
    plt.imshow(img.reshape(10, 10), cmap="gray_r")
    plt.title(title)
    plt.show()


# create a Hopfield network with 100 neurons
model = HopfieldNet(100)

# sample 10x10 pattern to store
P1 = convert_to_binary([
    [0,1,1,1,1,1,1,1,1,0],
    [1,1,0,0,0,0,0,0,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,1,1,1,0,0,1],
    [1,0,0,1,0,0,1,0,0,1],
    [1,0,0,1,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,0,0,0,0,0,0,1,1],
    [0,1,1,1,1,1,1,1,1,0],
    [0,0,0,1,1,1,1,0,0,0]
])

# create two random patterns
P2 = convert_to_binary(np.random.randint(0, 2, (10, 10)))
P3 = convert_to_binary(np.random.randint(0, 2, (10, 10)))

# store all patterns in the network
model.learn([P1, P2, P3])

# generate noisy version of the first pattern
noisy = inject_noise(P1, ratio=0.25)

# display patterns
show(P1, "Original Pattern")
show(noisy, "Noisy Version")
restored = model.update(noisy, iters=7)
show(restored, "Recovered Pattern")


def capacity_test(n=100, trials=15):
    # estimates the number of patterns that can be stored reliably
    for count in range(1, 60):
        success = 0

        for _ in range(trials):
            # generate a set of random bipolar patterns
            patt = [np.where(np.random.rand(n) > 0.45, 1, -1) for _ in range(count)]
            net = HopfieldNet(n)
            net.learn(patt)

            # test recall performance
            orig = patt[0]
            noisy = inject_noise(orig, ratio=0.20)
            rec = net.update(noisy, iters=6)

            if np.array_equal(orig, rec):
                success += 1

        # success threshold for reliable capacity
        if success / trials < 0.70:
            return count - 1

    return count


cap = capacity_test()
print("Estimated Pattern Capacity for 100 Neurons =", cap)
