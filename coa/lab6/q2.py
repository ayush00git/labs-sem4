import sys

class Decoder:
    def __init__(self, n):
        self.n = n
        self.lines = 1 << n   # 2^n

    def decode(self, inputs, enable):
        outputs = [0] * self.lines

        print(f"\n[{self.n}-to-{self.lines} Decoder]")
        print(f"  Enable = {enable}")
        print(f"  Inputs (MSB → LSB): {inputs}")

        # Condition: Enable check
        if not enable:
            print("  ✗ Enable is LOW → All outputs = 0 (decoder inactive)")
            return outputs

        # Condition: input count must equal n
        if len(inputs) != self.n:
            print(f"  ERROR: Expected {self.n} input bits, got {len(inputs)}")
            return outputs

        # Condition: each input must be binary (0 or 1)
        for i, v in enumerate(inputs):
            if v not in (0, 1):
                print(f"  ERROR: Input[{i}] = {v} is invalid (must be 0 or 1)")
                return outputs

        # Convert input bit array to decimal index (MSB first)
        index = 0
        for bit in inputs:
            index = index * 2 + bit

        # Activate exactly one output line
        outputs[index] = 1

        print(f"  Binary input  → Decimal index = {index}")
        print("  Output lines:")
        for i in range(self.lines):
            marker = "  ← ACTIVE ✓" if outputs[i] == 1 else ""
            print(f"    D{i:<2} = {outputs[i]}{marker}")

        return outputs


def print_truth_table(n):
    lines = 1 << n
    print(f"\n  ─── {n}-to-{lines} Decoder Truth Table ───")

    # Header
    header = "  E  |"
    for i in range(n - 1, -1, -1):
        header += f" A{i}"
    header += " |"
    for i in range(lines):
        header += f" D{i:<2}"
    print(header)
    print("  " + "─" * (6 + n * 3 + lines * 4))

    # Enable=0 row
    row = "  0  |"
    for _ in range(n):
        row += "  X"
    row += " |"
    for _ in range(lines):
        row += "  0 "
    print(row)

    # All enabled input combinations
    for r in range(lines):
        row = "  1  |"
        for bit in range(n - 1, -1, -1):
            row += f"  {(r >> bit) & 1}"
        row += " |"
        for col in range(lines):
            row += "  1 " if col == r else "  0 "
        print(row)


def main():
    # Input: value of n
    try:
        n = int(input("\nEnter number of input bits (n): "))
    except ValueError:
        print("Invalid input. Exiting.")
        sys.exit(1)

    if n <= 0 or n > 8:
        print("Invalid n. Please enter a value between 1 and 8.")
        sys.exit(1)

    dec = Decoder(n)
    print(f"Decoder created: {n}-to-{dec.lines}")

    # Input: enable pin
    try:
        enable_int = int(input("Enter Enable (1 = active, 0 = disabled): "))
    except ValueError:
        print("Invalid input. Exiting.")
        sys.exit(1)

    if enable_int not in (0, 1):
        print("Invalid Enable value. Must be 0 or 1.")
        sys.exit(1)

    enable = (enable_int == 1)

    # Input: n bits
    try:
        raw = input(f"Enter {n} input bits (MSB to LSB), space-separated: ")
        inputs = list(map(int, raw.strip().split()))
    except ValueError:
        print("Invalid bits entered. Exiting.")
        sys.exit(1)

    if len(inputs) != n:
        print(f"Expected {n} bits, got {len(inputs)}. Exiting.")
        sys.exit(1)

    for i, v in enumerate(inputs):
        if v not in (0, 1):
            print(f"Invalid bit at position {i}: must be 0 or 1")
            sys.exit(1)

    # Run decoder
    dec.decode(inputs, enable)

    # Optionally print truth table
    show = input("\nShow full truth table? (1 = yes, 0 = no): ").strip()
    if show == "1":
        print_truth_table(n)


if __name__ == "__main__":
    main()
