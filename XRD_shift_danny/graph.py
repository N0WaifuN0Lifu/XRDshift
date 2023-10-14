import numpy as np
from matplotlib import pyplot as plt
from matplotlib_inline.backend_inline import set_matplotlib_formats
set_matplotlib_formats('svg')

baseline = np.loadtxt("data/MOF808.xy", delimiter=' ')
shifted = np.loadtxt("data/79A64-130.xy", delimiter=' ')

# plot baseline and shifted
plt.plot(baseline[:, 0], baseline[:, 1])
plt.plot(shifted[:, 0], shifted[:, 1])
plt.show()
plt.clf()

for datapoint in baseline:
    datapoint[1] = datapoint[1] * (datapoint[0]/baseline.max()) ** 0.6

for datapoint in shifted:
    datapoint[1] = datapoint[1] * (datapoint[0]/shifted.max()) ** 0.6


# normalize baseline and shifted
baseline = baseline / baseline.max()
shifted = shifted / shifted.max()

# print shape
print(baseline.shape)
print(shifted.shape)
print(baseline[1])
baseline_x = []
baseline_y = []
for data in baseline:
    baseline_x.append(data[0])
    baseline_y.append(data[1])

shifted_x = []
shifted_y = []
for data in shifted:
    shifted_x.append(data[0])
    shifted_y.append(data[1])

plt.plot(baseline_x, baseline_y)
plt.plot(shifted_x, shifted_y)

# add a legend
plt.legend(['baseline', 'shifted'], loc='upper right')
plt.show()
plt.clf()

# danny code
sim = (baseline * shifted).sum()
print("Pre-Adjusted multiplicative area is:", f"{sim:.2e}")

x, baseline_values = baseline.T
_x, shifted_values = shifted.T

n = len(baseline_values)

np.pad(baseline_values, (n, n), constant_values=0)
np.pad(shifted_values, (0, 2*n), constant_values=0)


def shift_maximize_multiply():
    for i in range(2*n):
        w = np.roll(shifted_values, i)
        yield i, (baseline_values * w).sum()


i, sim = max(shift_maximize_multiply(), key=lambda x: x[1])

print("Post adjustment multiplacative area is:", f"{sim:.2e}")

print("Adjustment is:", f"{(i/100):.2e}", "Degrees")
x, baseline_values = baseline.T
_x, shifted_values = shifted.T

plt.plot(baseline_values)
plt.plot(np.roll(shifted_values, i))
plt.show()
