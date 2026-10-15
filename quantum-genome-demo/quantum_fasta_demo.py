
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

DNA_TO_BITS = {
    "A": "00",
    "C": "01",
    "G": "10",
    "T": "11",
}

BITS_TO_DNA = {
    bits: base for base, bits in DNA_TO_BITS.items()
}


def read_fasta(filename):
    """Read and validate a DNA sequence from a FASTA file."""
    parts = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith(">"):
                continue

            parts.append(line.upper())

    sequence = "".join(parts)

    if not sequence:
        raise ValueError("No DNA sequence found in FASTA file.")

    invalid = set(sequence) - set(DNA_TO_BITS)
    if invalid:
        raise ValueError(f"Invalid DNA characters: {invalid}")

    return sequence


def encode_dna(sequence):
    """Represent each DNA base using two classical bits."""
    return "".join(DNA_TO_BITS[base] for base in sequence)


def decode_dna(bits):
    """Convert each pair of bits back into a DNA base."""
    if len(bits) % 2:
        raise ValueError("Bitstring must contain an even number of bits.")

    return "".join(
        BITS_TO_DNA[bits[i:i + 2]]
        for i in range(0, len(bits), 2)
    )


def run_quantum_demo(bits):
    """Prepare a basis state, then measure it on a simulator."""
    circuit = QuantumCircuit(len(bits), len(bits))

    # Reverse bit order to match Qiskit's displayed measurement order.
    for qubit, bit in enumerate(reversed(bits)):
        if bit == "1":
            circuit.x(qubit)

    circuit.measure(range(len(bits)), range(len(bits)))

    simulator = AerSimulator()
    result = simulator.run(circuit, shots=1).result()

    measured_bits = next(iter(result.get_counts()))
    return measured_bits, circuit


def main():
    sequence = read_fasta("sample.fasta")
    encoded = encode_dna(sequence)

    measured, circuit = run_quantum_demo(encoded)
    recovered = decode_dna(measured)

    print("Original DNA:        ", sequence)
    print("Classical encoding:  ", encoded)
    print("Quantum measurement:", measured)
    print("Recovered DNA:       ", recovered)
    print("Number of bases:     ", len(sequence))
    print("Number of qubits:    ", len(encoded))
    print("\nCircuit:")
    print(circuit.draw(output="text"))
    print("\nSuccessful recovery:", recovered == sequence)


if __name__ == "__main__":
    main()
