import numpy as np

a = np.array([0,1,2,3,4,5,6,7]);
reshaped_a = np.reshape(a, [2]*3)
# for i in range(1):
#     for j in range(1):
#         for k in range(1): print(reshaped_a[i][j][k])
# print(a)
# print(reshaped_a)

# experimental cnot: say i want to use 1 as control and 3 as target
# flip along axes testing -> the number of the axis goes up the deeper you nest
# print(np.flip(reshaped_a, 0))
# print(np.flip(reshaped_a, 1))
# print(np.flip(reshaped_a, 2))
b = np.reshape(np.flip(reshaped_a, 2), 8);

# print(b)

# test run of my algorithm; control bit = 2, target bit = 0, 3 qubits
control = 2
target = 0
n = 3
dec_to_bin = np.vectorize(np.binary_repr)

i = [slice(None)]*n
i[control] = slice(1,2) #slice along axis=control
state = np.arange(2**n)
print(dec_to_bin(state, width=n))

state = np.reshape(state, [2]*n)
print(dec_to_bin(state, width=n))
print(i)
i=tuple(i) # This is necessary, I don't know exactly why, but I had to introduce this as a fix
state[i] = np.flip(state[i], axis=target);
print(dec_to_bin(state,width=n))

# WORKS BEAUTIFULLY :DDDD

a = -a
print(a)
c = [1+1j, 1-1j]
print(c)
c = np.array(c)
c = c * np.conjugate(c)
print(c)