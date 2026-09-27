# Solution to Problem Statement 1: Statevector Simulator

This was fun and hurt my brain sometimes, I still don't really feel how the oracle in Grover's algorithm works, or how the Half Entropy works.

## How I made the functions work:

I've tried my best to make sure the comments reflect my ideas and state of mind at the time of writing the code

### Single-qubit gates: `x, h, z`

All the three gates use essentially the same idea, of tensor multiplication of the $2x2$ identity matrix operating on whichever qubits were unaffected and the necessary matrix on whichever qubit was to be operated on. This is however, very computationally inefficient because this generates a matrix of $4^n$ elements, which is very computationally expensive to operate. This runs in $O(4^n)$ time.

### Two-qubit gates: `cnot, cz`

Building a full matrix for two-qubit gates was less trivial than the previous case, so I thought of this other approach:
Reshape the flat $2^n$-length statevector into an $n$-dimensional array, shape `[2]*n`, one axis per qubit.
Axis `i`, index `0` or `1` corresponds to "qubit i is 0 or 1." This just makes it a problem of slicing for the two bits to operate on, since everything else is left unchanged.

- `cnot`: slice down to the sub-array where the control axis is fixed at index 1 (control qubit = 1), then np.flip that sub-array along the target's axis. Flipping an axis of length 2 just swaps its two entries — swapping the target-qubit-is-0 amplitudes with the target-qubit-is-1 amplitudes, only in the region where control = 1.
- `cz`: same slicing idea, but this time pin both the control axis and the target axis to index 1 at once — that isolates exactly the corner of the tensor where both qubits are 1 — and multiply it by $-1$. No flipping needed here, because Z (and CZ) never move amplitudes around, they only ever multiply a phase onto them.

This is also a lot less computationally intensive, with a time complexity of $O(2^n)$ time, which is a square root of that of the previous operation. Ideally I should do the same neat trick on the single-qubit gates, but I'm lazy that way.

### `grover_2qubit` and `half_entropy`

Well, I don't really feel this deep inside me, either of them, so it was a bit of blind implementation of `half_entropy` and some blind implementation of `grover_2qubit` after reading the OG paper.

## References:
- [A fast quantum mechanical algorithm for database search - Lov K. Grover](https://arxiv.org/pdf/quant-ph/9605043)
- [But what is quantum computing? (Grover's Algorithm) - 3Blue1Brown](https://www.youtube.com/watch?v=RQWpF2Gb-gU)
- [Where my explanation of Grover's algorithm failed - 3Blue1Brown]()
- IBM Quantum lectures:
  - [Lecture 1](https://www.youtube.com/watch?v=3-c4xJa7Flk&list=PLOFEBzvs-VvqKKMXX4vbi4EB1uaErFMSO&index=3)
  - [Lecture 2](https://www.youtube.com/watch?v=DfZZS8Spe7U&list=PLOFEBzvs-VvqKKMXX4vbi4EB1uaErFMSO&index=4)
  - [Lecture 3](https://www.youtube.com/watch?v=30U2DTfIrOU&list=PLOFEBzvs-VvqKKMXX4vbi4EB1uaErFMSO&index=5)

- [Grover's algorithm - Wikipedia](https://en.wikipedia.org/wiki/Grover's_algorithm)

- I think there's more but I didn't document :(

## Acknowledgements:
I thank my dear friend Claude for trying to help me understand Grover's algorithm. I enjoyed thinking about this with 2:30 AM with Kushal.