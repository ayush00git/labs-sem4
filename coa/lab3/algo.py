class SignedMagnitudeALU32:
    def __init__(self):
        self.n = 32
        self.mask = 0xFFFFFFFF

    def print_step(self, step, A, As, B, Bs, E, AVF):
        a_bin = f"{A:032b}"
        b_bin = f"{B:032b}"
        print(f"\n[{step.upper()}]")
        print(f"  Registers -> E:{E} | AVF:{AVF}")
        print(f"  A: (S:{As}) {a_bin}")
        print(f"  B: (S:{Bs}) {b_bin}")

    def execute(self):
        a_sgn = int(input("Enter Sign bit A (0 for +, 1 for -): "))
        a_mag_str = input("Enter Magnitude A (binary): ").strip()
        b_sgn = int(input("Enter Sign bit B (0 for +, 1 for -): "))
        b_mag_str = input("Enter Magnitude B (binary): ").strip()
        op = input("Enter operation (+ or -): ").strip()

        A = int(a_mag_str, 2) & self.mask
        B = int(b_mag_str, 2) & self.mask
        As, Bs = a_sgn, b_sgn
        E, AVF = 0, 0

        if op == '-':
            Bs = 1 - Bs
            print(f"\n[SUBTRACTION MODE] Sign of B toggled to {Bs}")

        self.print_step("Initial State", A, As, B, Bs, E, AVF)

        if (As ^ Bs) == 0:
            sum_val = A + B
            E = 1 if sum_val > self.mask else 0
            A = sum_val & self.mask
            self.print_step("EA <- A + B", A, As, B, Bs, E, AVF)

            AVF = E
            self.print_step("AVF <- E", A, As, B, Bs, E, AVF)
        else:
            B_comp = (~B & self.mask) + 1
            sum_val = A + B_comp
            E = 1 if sum_val > self.mask else 0
            A = sum_val & self.mask
            self.print_step("EA <- A + B' + 1", A, As, B, Bs, E, AVF)

            if E == 1:
                if A == 0:
                    As = 0
                    self.print_step("A = 0: As <- 0", A, As, B, Bs, E, AVF)
                else:
                    self.print_step("A >= B: End", A, As, B, Bs, E, AVF)
            else:
                A = (~A & self.mask) + 1
                As = 1 - As
                self.print_step("A < B: A <- A'+1, As <- As'", A, As, B, Bs, E, AVF)

        print("\n" + "="*50)
        print(f"FINAL RESULT: {'-' if As else '+'}{A:032b}")
        print("="*50)

if __name__ == "__main__":
    alu = SignedMagnitudeALU32()
    alu.execute()
