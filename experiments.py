import numpy as np

a = np.array([0,1,2,3,4,5,6,7]);
reshaped_a = np.reshape(a, [2]*3)
for i in range(1):
    for j in range(1):
        for k in range(1): print(reshaped_a[i][j][k])
print(a)
print(reshaped_a)

# experimental cnot: say i want to use 1 as control and 3 as target
# flip along axes testing -> the number of the axis goes up the deeper you nest
print(np.flip(reshaped_a, 0))
print(np.flip(reshaped_a, 1))
print(np.flip(reshaped_a, 2))
b = np.reshape(np.flip(reshaped_a, 2), 8);

print(b)