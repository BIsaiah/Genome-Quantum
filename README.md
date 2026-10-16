# Genome-Quantum
Uap assignment
## Grover DNA Pattern Search

### Objective

This experiment explores how Grover's quantum search algorithm can increase the probability of finding a specific DNA pattern in a small search space. It is a learning demonstration, not a real-world genome search benchmark.

### Experimental Setup

- **Search space:** All 16 possible DNA patterns of length two, using A, C, G, and T.
- **Target pattern:** `GT`
- **Encoding:** Each DNA base is represented by two bits, requiring four qubits to represent a two-base pattern.
- **Algorithm:** Grover's search algorithm, using three iterations of the oracle and diffuser.
- **Simulator:** Qiskit Aer.
- **Measurements:** The circuit was tested with different shot counts, up to 5,000 shots.

### Results

With 1,000 measurement shots, the target `GT` appeared 947 times, giving an observed target measurement rate of **94.7%**. The ideal theoretical success probability for this setup is approximately 96.1%.

Additional tests used different shot counts to observe how the measured success rate varied. The recorded results should be included alongside this section or in a results table.

### Interpretation

The results demonstrate probability amplification in a small, controlled quantum search. Grover's algorithm makes the target more likely to appear when the circuit is measured.

Increasing the number of shots provides more measurements for estimating the success probability, but it does not automatically increase the probability of success in each individual measurement.

### Limitations

- This experiment searches 16 possible two-base patterns, not a real genome or sequencing dataset.
- The target pattern is built into the oracle, which marks the desired result.
- The experiment uses a simulator rather than a physical quantum computer.
- The classical comparison count and Grover iteration count are not directly equivalent measures of computational cost.
- These results do not demonstrate a practical quantum speedup for genome searching or an improvement in DNA compression.

The experiment is intended to demonstrate a quantum computing concept and explore its potential relevance to genomic data processing, not to establish real-world performance advantages.
