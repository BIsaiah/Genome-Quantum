
from itertools import product

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


DNA_TO_BITS = {
    "A": "00",
    "C": "01",
    "G": "10",
    "T": "11",
}

TARGET = "GT"
SHOTS = 500


def apply_oracle(circuit, target_bits):
    """Flip the phase of exactly the target computational-basis state."""
    n = len(target_bits)

    # Qiskit displays measured bits from highest index to lowest.
    # Flip qubits where the target contains a 0.
    for qubit in range(n):
        if target_bits[n - 1 - qubit] == "0":
            circuit.x(qubit)

    # Multi-controlled Z: mark the all-ones state with a phase flip.
    circuit.h(n - 1)
    circuit.mcx(list(range(n - 1)), n - 1)
    circuit.h(n - 1)

    # Undo the temporary X gates.
    for qubit in range(n):
        if target_bits[n - 1 - qubit] == "0":
            circuit.x(qubit)


def apply_diffuser(circuit, n):
    """Amplify the marked state's measurement probability."""
    circuit.h(range(n))
    circuit.x(range(n))

    circuit.h(n - 1)
    circuit.mcx(list(range(n - 1)), n - 1)
    circuit.h(n - 1)

    circuit.x(range(n))
    circuit.h(range(n))


def main():
    # Generate every possible two-base DNA pattern.
    candidates = [
        "".join(pair)
        for pair in product("ACGT", repeat=2)
    ]

    # Classical baseline: check candidates one at a time.
    comparisons = 0
    for candidate in candidates:
        comparisons += 1
        if candidate == TARGET:
            break

    print("Number of possible patterns:", len(candidates))
    print("Target DNA pattern:", TARGET)
    print("Classical comparisons needed:", comparisons)

    # Encode the target as four bits, requiring four qubits.
    target_bits = "".join(DNA_TO_BITS[base] for base in TARGET)
    n = len(target_bits)

    circuit = QuantumCircuit(n, n)

    # Create an equal superposition of all 16 bitstrings.
    circuit.h(range(n))

    # For 16 possibilities and one target, use 3 Grover iterations.
    iterations = 3

    for _ in range(iterations):
        apply_oracle(circuit, target_bits)
        apply_diffuser(circuit, n)

    circuit.measure(range(n), range(n))

    simulator = AerSimulator()
    result = simulator.run(circuit, shots=SHOTS).result()
    counts = result.get_counts()

    # Convert measured bitstrings back into DNA patterns.
    bits_to_dna = {
        bits: base for base, bits in DNA_TO_BITS.items()
    }

    target_count = counts.get(target_bits, 0)

    print("Target encoding:", target_bits)
    print("Qubits used:", n)
    print("Grover iterations:", iterations)
    print("Measurement shots:", SHOTS)
    print("Target found:", target_count, "times")
    print("Target measurement rate:",
          f"{100 * target_count / SHOTS:.1f}%")

    print("\nMeasured DNA patterns:")
    for bits, count in sorted(
        counts.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        pattern = (
            bits_to_dna[bits[:2]]
            + bits_to_dna[bits[2:]]
        )
        print(f"{pattern}: {count}")

    print("\nCircuit:")
    print(circuit.draw(output="text"))


if __name__ == "__main__":
    main()
