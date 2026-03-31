import sys

# ============================================================
# QUESTION 3: 4:1 Multiplexer
# ============================================================
#
# A multiplexer (MUX) selects ONE of many input signals and
# forwards it to the output based on select lines.
#
# 4:1 MUX Structure:
#   - 4 data inputs : D0, D1, D2, D3
#   - 2 select lines: S1 (MSB), S0 (LSB)
#   - 1 enable      : E  (active HIGH — if 0, output forced to 0)
#   - 1 output      : Y
#
# Boolean Expression:
#   Y = D0·S̄1·S̄0  +  D1·S̄1·S0  +  D2·S1·S̄0  +  D3·S1·S0
#
# Selection Table:
#   S1=0, S0=0  →  Y = D0
#   S1=0, S0=1  →  Y = D1
#   S1=1, S0=0  →  Y = D2
#   S1=1, S0=1  →  Y = D3


DIVIDER = "-" * 50


class MUX41:
    def __init__(self, d0, d1, d2, d3, s1, s0, e):
        self.D  = [d0, d1, d2, d3]
        self.S1 = s1
        self.S0 = s0
        self.E  = e

    def evaluate(self):
        print(f"\n[4:1 MUX]")
        print(f"  Data Inputs : D0={self.D[0]}  D1={self.D[1]}  D2={self.D[2]}  D3={self.D[3]}")
        print(f"  Select Lines: S1={self.S1}  S0={self.S0}")
        print(f"  Enable      : E={self.E}")
        print(f"  {DIVIDER}")

        # Condition: all values must be 0 or 1
        checks = {
            "D0": self.D[0], "D1": self.D[1],
            "D2": self.D[2], "D3": self.D[3],
            "S1": self.S1,   "S0": self.S0,
            "E" : self.E
        }
        for name, val in checks.items():
            if val not in (0, 1):
                print(f"  ERROR: {name} = {val} is invalid (must be 0 or 1)")
                return -1

        # Condition: Enable check
        if self.E == 0:
            print("  ✗ Enable is LOW → Output Y = 0 (MUX disabled)")
            return 0

        # Complemented select lines
        s1bar = 1 - self.S1
        s0bar = 1 - self.S0

        # Compute each product term
        term0 = self.D[0] & s1bar & s0bar   # D0 · S̄1 · S̄0
        term1 = self.D[1] & s1bar & self.S0 # D1 · S̄1 · S0
        term2 = self.D[2] & self.S1 & s0bar # D2 · S1  · S̄0
        term3 = self.D[3] & self.S1 & self.S0# D3 · S1  · S0

        Y = term0 | term1 | term2 | term3

        selected_index = self.S1 * 2 + self.S0

        print(f"  Boolean : Y = D0·S̄1·S̄0 + D1·S̄1·S0 + D2·S1·S̄0 + D3·S1·S0")
        print(f"  Expanded: Y = {self.D[0]}·{s1bar}·{s0bar}"
              f" + {self.D[1]}·{s1bar}·{self.S0}"
              f" + {self.D[2]}·{self.S1}·{s0bar}"
              f" + {self.D[3]}·{self.S1}·{self.S0}")
        print(f"          : Y = {term0} + {term1} + {term2} + {term3}")
        print(f"  Select S1S0 = {self.S1}{self.S0} → D{selected_index} is forwarded")
        print(f"  ✓ Output Y = {Y}")
        return Y


def print_truth_table(d):
    print(f"\n  ─── 4:1 MUX Truth Table (D0={d[0]} D1={d[1]} D2={d[2]} D3={d[3]}) ───")
    print("  E  | S1  S0 | Selected | Y")
    print("  " + "─" * 32)
    print("  0  |  X   X |   None   | 0  (disabled)")
    for s in range(4):
        s1 = (s >> 1) & 1
        s0 = s & 1
        s1b = 1 - s1
        s0b = 1 - s0
        y = (d[0] & s1b & s0b) | (d[1] & s1b & s0) | (d[2] & s1 & s0b) | (d[3] & s1 & s0)
        print(f"  1  |  {s1}   {s0}  |    D{s}    | {y}")


def read_bit(label):
    while True:
        try:
            v = int(input(f"  Enter {label} (0 or 1): "))
            if v in (0, 1):
                return v
            print("  Invalid! Must be 0 or 1.")
        except ValueError:
            print("  Invalid input. Please enter 0 or 1.")


def main():

    # Input: Enable
    print("\n── Enable Pin ──")
    e = read_bit("Enable E")

    # Input: Select lines
    print("\n── Select Lines ──")
    s1 = read_bit("S1 (MSB)")
    s0 = read_bit("S0 (LSB)")

    # Input: Data lines
    print("\n── Data Inputs ──")
    d0 = read_bit("D0")
    d1 = read_bit("D1")
    d2 = read_bit("D2")
    d3 = read_bit("D3")

    # Evaluate
    mux = MUX41(d0, d1, d2, d3, s1, s0, e)
    mux.evaluate()

    # Optionally print truth table
    show = input("\nShow full truth table for these data inputs? (1 = yes, 0 = no): ").strip()
    if show == "1":
        print_truth_table([d0, d1, d2, d3])


if __name__ == "__main__":
    main()
