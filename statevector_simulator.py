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

    def x(self, qubit: int) -> None:
        """Apply the Pauli-X (NOT) gate to the given qubit."""
        pauli_x = np.array([[0,1],[1,0]], dtype=complex) # NOT
        # For now I'll just make the horribly computationally inefficient tensor product
        U = np.identity(1, dtype=complex)

        # Repeated tensor product that pisses me off because it's mostly I x I x ...
        for i in range(0,self.num_qubits):
            if (i==qubit): U = np.kron(U, pauli_x)
            else: U = np.kron(U, np.identity(2))

        self.state = U @ self.state
        return None
        # raise NotImplementedError

    def h(self, qubit: int) -> None:
        """Apply the Hadamard gate to the given qubit."""
        # I just copied the x implementation and replaced it with Hadamard :/
        hadamard = np.array([[1/np.sqrt(2),1/np.sqrt(2)],[1/np.sqrt(2),-1/np.sqrt(2)]], dtype=complex) # H
        # For now I'll just make the horribly computationally inefficient tensor product
        U = np.identity(1, dtype=complex)

        # Repeated tensor product that pisses me off because it's mostly I x I x ...
        for i in range(0,self.num_qubits):
            if (i==qubit): U = np.kron(U, hadamard)
            else: U = np.kron(U, np.identity(2))

        self.state = U @ self.state
        return None
        # raise NotImplementedError

    def z(self, qubit: int) -> None:
        """Apply the Pauli-Z gate to the given qubit."""
        # Same thing as before >:(
        pauli_z = np.array([[1,0],[0,-1]], dtype=complex) # Phase Flip (why phase hmmm)
        # For now I'll just make the horribly computationally inefficient tensor product
        U = np.identity(1, dtype=complex)

        # Repeated tensor product that pisses me off because it's mostly I x I x ...
        for i in range(0,self.num_qubits):
            if (i==qubit): U = np.kron(U, pauli_z)
            else: U = np.kron(U, np.identity(2))

        self.state = U @ self.state
        return None
        # raise NotImplementedError

    def cnot(self, control: int, target: int) -> None:
        """Apply a CNOT gate with the given control and target qubits."""
        # when control qubit is 1, target bit inverts
        # I'll reshape the statevector into a 2x2x2x...x2 tensor
        # Then it's arranged so that element 0 in that axis corresponds to |0> for that qubit and element 1 to |1>
        # Each qubit sits on an axis where only its values change

        # Converts 1D statevector into nD state_tensor for ease of operations
        # Axis i indexes qubit i's basis states
        state_tensor = np.reshape(self.state, [2]*self.num_qubits)
        # Might be worthwhile to flip entirely if control index is larger than target index, might reduce time complexity
        if (control > target): state_tensor = np.flip(state_tensor); # Reverses order, will need to reverse again during final reshape
        # ! IDEA: I will make sure control is "higher" priority than target,
        # ! then go into the index 1 of control and then flip along the axis of the target bit
        # ! only within that subarray of control being 1.

        # ! Actually, it might be worthwhile just keeping control at bit 1 and target at bit 2
        # ! but I'm not sure

        # Stretch back into 1D
        state_tensor = np.reshape(state_tensor, 2**self.num_qubits);
        # raise NotImplementedError

    def cz(self, control: int, target: int) -> None:
        """Apply a controlled-Z gate with the given control and target qubits."""
        raise NotImplementedError

    def half_entropy(self) -> float:
        """
        Compute the entanglement entropy across the half bipartition.

        Returns:
            The half-cut entanglement entropy in bits.
        """
        raise NotImplementedError

    def get_statevector(self) -> np.ndarray:
        """Return the current statevector as a NumPy array."""
        raise NotImplementedError

    def get_probabilities(self) -> np.ndarray:
        """Return the current probabilities as a Numpy array"""
        raise NotImplementedError

    def reset(self) -> None:
        """Reset the simulator back to the |0...0> state."""
        raise NotImplementedError

    def grover_2qubit(self, marked_state: int) -> None:
        """
        Run Grover's search algorithm on 2 qubits using your simulator.

        The marked state should have probability ~1 after one iteration.

        Args:
            marked_state: Index (0 to 3) of the state the oracle marks.
        """
        raise NotImplementedError


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
