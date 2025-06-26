import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
try:
    from qiskit_aer import Aer
    backend = Aer.get_backend('qasm_simulator')
except Exception:
    from qiskit import Aer
    backend = Aer.get_backend('qasm_simulator')


def _prepare_vector(vec: np.ndarray) -> tuple[np.ndarray, int]:
    """Normalize and resize input vector to length 2**n."""
    vector = np.asarray(vec, dtype=complex)
    if vector.ndim != 1:
        raise ValueError("Input vector must be one-dimensional")
    norm = np.linalg.norm(vector)
    if norm == 0:
        raise ValueError("Input vector must be non-zero")
    vector = vector / norm
    length = len(vector)
    n = int(np.ceil(np.log2(length)))
    size = 2 ** n
    if length < size:
        padded = np.zeros(size, dtype=complex)
        padded[:length] = vector
        vector = padded
    elif length > size:
        vector = vector[:size]
        vector = vector / np.linalg.norm(vector)
    return vector, n


def run_qpca(vector: np.ndarray) -> dict:
    """Run a mock QPCA using QFT on the given vector.

    Parameters
    ----------
    vector : np.ndarray
        Input vector of amplitudes.

    Returns
    -------
    dict
        Measurement counts from the simulator.
    """
    state, n_qubits = _prepare_vector(vector)

    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.initialize(state.tolist(), qc.qubits)
    qc.append(QFT(n_qubits), qc.qubits)
    qc.measure(qc.qubits, qc.clbits)

    compiled = transpile(qc, backend)
    job = backend.run(compiled, shots=1024)
    result = job.result()
    return result.get_counts(qc)