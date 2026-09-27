"""
Statevector Simulator - Core Selection Problem Statement 1

Build a statevector simulator for an n-qubit system using NumPy.

Your simulator must support:
    - Single qubit gates: X, H, Z
    - Two qubit gates: CNOT, CZ
    - Half entropy of the system: the von-Neumann entanglement entropy

You may ONLY use NumPy (and the Python standard library). No Qiskit,
no other quantum computing libraries.
"""

import numpy as np


class StatevectorSimulator:
    """A statevector simulator for an n-qubit quantum system."""

    def __init__(self, num_qubits: int):
        """
        Initialize the simulator in the |0...0> state.

        Args:
            num_qubits: Number of qubits n. The statevector must be a
                complex NumPy array of size 2**n.
        """
        self.num_qubits = num_qubits
        # This seems sketchy, what does it mean to set the qubits to a deterministic value
        self.state = None  # initialize to |0...0>
        self.state = np.zeros(2**num_qubits, dtype=complex)
        self.state[0] = 1

    def x(self, qubit: int) -> None:
        """Apply the Pauli-X (NOT) gate to the given qubit."""
        pauli_x = np.array([[0,1],[1,0]], dtype=complex) # NOT
        # For now I'll just make the horribly computationally inefficient tensor product
        U = np.identity(1, dtype=complex)

        # Repeated tensor product that pisses me off because it's mostly I x I x ...
        for i in range(0,self.num_qubits):
            if (i==qubit): U = np.kron(U, pauli_x)
            else: U = np.kron(U, np.identity(2, dtype=complex))

        self.state = U @ self.state
        return None

    def h(self, qubit: int) -> None:
        """Apply the Hadamard gate to the given qubit."""
        # I just copied the x implementation and replaced it with Hadamard :/
        hadamard = np.array([[1/np.sqrt(2),1/np.sqrt(2)],[1/np.sqrt(2),-1/np.sqrt(2)]], dtype=complex) # H
        # For now I'll just make the horribly computationally inefficient tensor product
        U = np.identity(1, dtype=complex)

        # Repeated tensor product that pisses me off because it's mostly I x I x ...
        for i in range(0,self.num_qubits):
            if (i==qubit): U = np.kron(U, hadamard)
            else: U = np.kron(U, np.identity(2, dtype=complex))

        self.state = U @ self.state
        return None

    def z(self, qubit: int) -> None:
        """Apply the Pauli-Z gate to the given qubit."""
        # Same thing as before >:(
        pauli_z = np.array([[1,0],[0,-1]], dtype=complex) # Phase Flip (why phase hmmm)
        # For now I'll just make the horribly computationally inefficient tensor product
        U = np.identity(1, dtype=complex)

        # Repeated tensor product that pisses me off because it's mostly I x I x ...
        for i in range(0,self.num_qubits):
            if (i==qubit): U = np.kron(U, pauli_z)
            else: U = np.kron(U, np.identity(2, dtype=complex))

        self.state = U @ self.state
        return None

    def cnot(self, control: int, target: int) -> None:
        """Apply a CNOT gate with the given control and target qubits."""
        # When control qubit is 1, target bit inverts
        # I'll reshape the statevector into a 2x2x2x...x2 tensor
        # Then it's arranged so that element 0 in that axis corresponds to |0> for that qubit and element 1 to |1>
        # Each qubit sits on an axis where only its values change
        # Converts 1D statevector into nD state_tensor for ease of operations
        # Axis i indexes qubit i's basis states
        # IDEA
        # Go into the index 1 of control and then flip along the axis of the target bit

        state_tensor = np.reshape(self.state, [2]*self.num_qubits)
        # Instruction on how to slice the nD tensor: keeps indexes where control qubit = 1
        indexes = [slice(None)]*self.num_qubits
        indexes[control] = slice(1,2) # This isolates the part where control qubit = 1, maintains array shape

        # Now, to flip along the target axis where control = 1
        state_tensor[tuple(indexes)] = np.flip(state_tensor[tuple(indexes)], axis=target)
        # Stretch back into 1D
        self.state = np.reshape(state_tensor, 2**self.num_qubits)
        return None

    def cz(self, control: int, target: int) -> None:
        """Apply a controlled-Z gate with the given control and target qubits."""
        # I think instead of applying a flip on the sliced array, I do the operation x = -x for the sliced part
        state_tensor = np.reshape(self.state, [2]*self.num_qubits)
        # Instruction on how to slice the nD tensor: keeps indexes where control qubit = 1 AND 
        indexes = [slice(None)]*self.num_qubits
        indexes[target] = indexes[control] = slice(1,2) # Isolates where control = 1 and target = 1
        # Now to apply x = -x
        state_tensor[tuple(indexes)] *= complex(-1.0)
        self.state = np.reshape(state_tensor, 2**self.num_qubits)
        return None

    def half_entropy(self) -> float:
        """
        Compute the entanglement entropy across the half bipartition.

        Returns:
            The half-cut entanglement entropy in bits.
        """
        # First I reshape the statevector into a square matrix, first n/2 qubits and second n/2 qubits
        n = self.num_qubits
        s = self.num_qubits//2
        mat = np.reshape(self.state, [2**s, 2**(n-s)])

        # I just implemented it from the original README, I've got little to no idea on how to "feel" it
        U, lambdas, Vdagger = np.linalg.svd(mat) # SVD
        prob = lambdas**2
        prob = prob[prob > 0]
        S = -np.sum(prob * np.log2(prob))
        return S

    def get_statevector(self) -> np.ndarray:
        """Return the current statevector as a NumPy array."""
        return self.state

    def get_probabilities(self) -> np.ndarray:
        """Return the current probabilities as a Numpy array"""
        return np.conjugate(self.state)*(self.state)

    def reset(self) -> None:
        """Reset the simulator back to the |0...0> state."""
        self.state = np.zeros(2**self.num_qubits, dtype=complex)
        self.state[0] = 1
        return None

    def grover_2qubit(self, marked_state: int) -> None:
        """
        Run Grover's search algorithm on 2 qubits using your simulator.

        The marked state should have probability ~1 after one iteration.

        Args:
            marked_state: Index (0 to 3) of the state the oracle marks.
        """
        # From arXiv/quant-ph/9605043
        # Grover's algorithm makes use of 3 steps:
        # 1. Initialise vector = (2^(-n/2)) of 2^n elements (n=2)
        self.h(0) # Applying H on first qubit
        self.h(1) # Applying H on second qubit

        # 2. The cheaty all knowing oracle -> flips state if equal to marked state
        # Note: I can't think anymore
        if marked_state == 0:
            self.x(0)
            self.x(1)
            self.cz(0,1)
            self.x(0)
            self.x(1)
        elif marked_state == 1:
            self.x(0)
            self.cz(0,1)
            self.x(0)
        elif marked_state == 2:
            self.x(1)
            self.cz(0,1)
            self.x(1)
        elif marked_state == 3:
            self.cz(0,1)
        else:
            print("Boohoo, you don't have a valid key L.")
            return None

        # 3. Invert about mean of all states: U = -I + 2(1/N)_(2^n x 2^n); U = 2qubitH x (2|00><00| - I) x 2qubitH
        # 2 qubit H
        self.h(0)
        self.h(1)

        # 2|00><00| - I = diag(1,-1,-1,-1)
        # Makes 00 -> 11
        self.x(0)
        self.x(1)
        # Makes 11 -> -11
        self.cz(0,1)
        # Makes -11 -> -00
        self.x(0)
        self.x(1)

        # 2 qubit H
        self.h(0)
        self.h(1)

        return None


if __name__ == "__main__":
    # Run 2-qubit Grover search marking the state |11> (index 3).
    simulator = StatevectorSimulator(2)
    marked_state = 3
    simulator.grover_2qubit(marked_state)
    final_state = simulator.get_statevector()
    probabilities = simulator.get_probabilities()

    print("Final statevector:", final_state)
    print("Probabilities:", probabilities)
    print("Measured state:", np.argmax(probabilities))
    print("Half Entropy:",simulator.half_entropy())
