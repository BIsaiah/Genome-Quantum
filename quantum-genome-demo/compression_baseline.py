
import gzip
from pathlib import Path


def read_fasta(filename):
    """Read DNA bases from a FASTA file, ignoring headers."""
    parts = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if line and not line.startswith(">"):
                parts.append(line.upper())

    return "".join(parts)


def test_compression(label, sequence):
    """Compress DNA, decompress it, and measure the result."""
    original = sequence.encode("ascii")
    compressed = gzip.compress(original, mtime=0)
    recovered = gzip.decompress(compressed)

    print(f"\n--- {label} ---")
    print("DNA bases:", len(sequence))
    print("Original size:", len(original), "bytes")
    print("Compressed size:", len(compressed), "bytes")
    print("Recovered correctly:", recovered == original)

    if len(compressed) < len(original):
        saved = 100 * (1 - len(compressed) / len(original))
        print(f"Space saved: {saved:.1f}%")
    else:
        extra = 100 * (len(compressed) / len(original) - 1)
        print(f"Size increase: {extra:.1f}%")


def main():
    sequence = read_fasta("sample.fasta")

    # Test the sequence from your FASTA file.
    test_compression("Original FASTA sequence", sequence)

    # Create a deliberately repetitive test sequence.
    repetitive = sequence * 1000
    test_compression("Repeated sequence", repetitive)


if __name__ == "__main__":
    main()
