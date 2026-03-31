import struct
import sys

DIVIDER = "  " + "-" * 50

def float_to_bits32(f):
    """Pack float32 into its raw 32-bit integer representation."""
    return struct.unpack('I', struct.pack('f', f))[0]

def bits_to_float32(bits):
    """Unpack 32-bit integer into float32."""
    return struct.unpack('f', struct.pack('I', bits & 0xFFFFFFFF))[0]

def decompose32(f):
    """Extract sign, unbiased exponent, and mantissa (with implicit 1) from float32."""
    bits = float_to_bits32(f)
    sign     = (bits >> 31) & 1
    biased   = (bits >> 23) & 0xFF
    frac     = bits & 0x7FFFFF
    exponent = biased - 127
    mantissa = frac | (1 << 23)   # restore implicit leading 1
    return sign, exponent, mantissa

def compose32(sign, exponent, mantissa):
    """Reconstruct float32 from sign, unbiased exponent, and mantissa."""
    if mantissa == 0:
        return 0.0
    biased = exponent + 127
    bits = (sign << 31) | (biased << 23) | (mantissa & 0x7FFFFF)
    return bits_to_float32(bits)

def fp_add_sub32(a, b, subtract):
    op = "-" if subtract else "+"
    print(f"\n[Single Precision]  {a:.6f}  {op}  {b:.6f}")
    print(DIVIDER)

    # STEP 1: Check for zeros
    print("  Step 1: Check for zeros")
    if a == 0.0 and b == 0.0:
        print("  → Both AC and BR are zero. Result = 0")
        return 0.0
    if a == 0.0:
        print(f"  → AC is zero. Result = {'−' if subtract else ''}BR = {-b if subtract else b:.6f}")
        return -b if subtract else b
    if b == 0.0:
        print(f"  → BR is zero. Result = AC = {a:.6f}")
        return a
    print("  → Neither operand is zero. Proceeding...")

    if subtract:
        b = -b

    sign_a, exp_a, mant_a = decompose32(a)
    sign_b, exp_b, mant_b = decompose32(b)

    print(f"\n  A: sign={sign_a}, exp={exp_a}, mantissa=0x{mant_a:06X}  ({mant_a:024b})")
    print(f"  B: sign={sign_b}, exp={exp_b}, mantissa=0x{mant_b:06X}  ({mant_b:024b})")

    # STEP 2: Align mantissas
    print("\n  Step 2: Align mantissas (shift smaller exponent right)")
    while exp_a > exp_b:
        mant_b >>= 1
        exp_b += 1
        print(f"  → Shifted B right,  exp_B now {exp_b},  mant_B = {mant_b:024b}")
    while exp_b > exp_a:
        mant_a >>= 1
        exp_a += 1
        print(f"  → Shifted A right,  exp_A now {exp_a},  mant_A = {mant_a:024b}")
    print(f"  → Exponents aligned at {exp_a}.")
    result_exp = exp_a

    # STEP 3: Add or subtract mantissas
    print("\n  Step 3: Add / subtract mantissas")
    m_a = -mant_a if sign_a else mant_a
    m_b = -mant_b if sign_b else mant_b
    print(f"  AC mantissa (signed) = {m_a}")
    print(f"  BR mantissa (signed) = {m_b}")
    result_mant = m_a + m_b
    print(f"  Sum = {m_a} + ({m_b}) = {result_mant}")

    result_sign = 0
    if result_mant < 0:
        result_sign = 1
        result_mant = -result_mant
        print(f"  Result is negative → sign=1, magnitude={result_mant}")
    else:
        print(f"  Result is non-negative → sign=0")

    if result_mant == 0:
        print("  → Mantissas cancelled completely. Result = 0")
        return 0.0

    print(f"  Result mantissa = {result_mant}  =  {result_mant:025b}")

    # STEP 4: Normalize
    print("\n  Step 4: Normalize the result")

    # Overflow: carry bit (bit-24) set → SHR + increment exponent
    if result_mant > (1 << 24) - 1:
        print(" Overflow detected (mantissa > 24 bits) → SHR (shift right)")
        while result_mant > (1 << 24) - 1:
            result_mant >>= 1
            result_exp += 1
            print(f"    SHR: mant={result_mant:024b}  exp={result_exp}")
    else:
        print("    No overflow.")

    # Underflow: MSB (bit-23) not set → SHL + decrement exponent
    if result_mant != 0 and not (result_mant & (1 << 23)):
        print("  ⚠ Underflow detected (MSB=0) → SHL (shift left)")
        while result_mant != 0 and not (result_mant & (1 << 23)):
            result_mant <<= 1
            result_exp -= 1
            print(f"    SHL: mant={result_mant:024b}  exp={result_exp}")
    else:
        print("    No underflow.")

    result = compose32(result_sign, result_exp, result_mant)
    print(f"\n    Final Result = {result:.6f}")
    return result

def float_to_bits64(f):
    return struct.unpack('Q', struct.pack('d', f))[0]

def bits_to_float64(bits):
    return struct.unpack('d', struct.pack('Q', bits & 0xFFFFFFFFFFFFFFFF))[0]

def decompose64(f):
    bits = float_to_bits64(f)
    sign     = (bits >> 63) & 1
    biased   = (bits >> 52) & 0x7FF
    frac     = bits & 0x000FFFFFFFFFFFFF
    exponent = biased - 1023
    mantissa = frac | (1 << 52)
    return sign, exponent, mantissa

def compose64(sign, exponent, mantissa):
    if mantissa == 0:
        return 0.0
    biased = exponent + 1023
    bits = (sign << 63) | (biased << 52) | (mantissa & 0x000FFFFFFFFFFFFF)
    return bits_to_float64(bits)

def fp_add_sub64(a, b, subtract):
    op = "-" if subtract else "+"
    print(f"\n[Double Precision]  {a:.10f}  {op}  {b:.10f}")
    print(DIVIDER)

    # STEP 1: Check for zeros
    print("  Step 1: Check for zeros")
    if a == 0.0 and b == 0.0:
        print("  → Both AC and BR are zero. Result = 0")
        return 0.0
    if a == 0.0:
        print(f"  → AC is zero. Result = {'−' if subtract else ''}BR = {-b if subtract else b:.10f}")
        return -b if subtract else b
    if b == 0.0:
        print(f"  → BR is zero. Result = AC = {a:.10f}")
        return a
    print("  → Neither operand is zero. Proceeding...")

    if subtract:
        b = -b

    sign_a, exp_a, mant_a = decompose64(a)
    sign_b, exp_b, mant_b = decompose64(b)

    print(f"\n  A: sign={sign_a}, exp={exp_a}, mantissa={mant_a}")
    print(f"  B: sign={sign_b}, exp={exp_b}, mantissa={mant_b}")

    # STEP 2: Align mantissas
    print("\n  Step 2: Align mantissas (shift smaller exponent right)")
    while exp_a > exp_b:
        mant_b >>= 1
        exp_b += 1
        print(f"  → Shifted B right,  exp_B now {exp_b}")
    while exp_b > exp_a:
        mant_a >>= 1
        exp_a += 1
        print(f"  → Shifted A right,  exp_A now {exp_a}")
    print(f"  → Exponents aligned at {exp_a}.")
    result_exp = exp_a

    # STEP 3: Add or subtract mantissas
    print("\n  Step 3: Add / subtract mantissas")
    m_a = -mant_a if sign_a else mant_a
    m_b = -mant_b if sign_b else mant_b
    print(f"  AC mantissa (signed) = {m_a}")
    print(f"  BR mantissa (signed) = {m_b}")
    result_mant = m_a + m_b
    print(f"  Sum = {m_a} + ({m_b}) = {result_mant}")

    result_sign = 0
    if result_mant < 0:
        result_sign = 1
        result_mant = -result_mant
        print(f"  Result is negative → sign=1, magnitude={result_mant}")
    else:
        print("  Result is non-negative → sign=0")

    if result_mant == 0:
        print("  → Mantissas cancelled completely. Result = 0")
        return 0.0

    print(f"  Result mantissa = {result_mant}")

    # STEP 4: Normalize
    print("\n  Step 4: Normalize the result")

    if result_mant > (1 << 53) - 1:
        print("  ⚠ Overflow detected → SHR (shift right)")
        while result_mant > (1 << 53) - 1:
            result_mant >>= 1
            result_exp += 1
            print(f"    SHR: mant={result_mant}  exp={result_exp}")
    else:
        print("    No overflow.")

    if result_mant != 0 and not (result_mant & (1 << 52)):
        print("  ⚠ Underflow detected (MSB=0) → SHL (shift left)")
        while result_mant != 0 and not (result_mant & (1 << 52)):
            result_mant <<= 1
            result_exp -= 1
            print(f"    SHL: mant={result_mant}  exp={result_exp}")
    else:
        print("   No underflow.")

    result = compose64(result_sign, result_exp, result_mant)
    print(f"\n   Final Result = {result:.10f}")
    return result

def main():
    # Choose precision
    print("\nSelect precision:")
    print("  1. Single Precision (float32)")
    print("  2. Double Precision (float64)")
    prec = input("Enter choice (1 or 2): ").strip()
    if prec not in ("1", "2"):
        print("Invalid choice. Exiting.")
        sys.exit(1)

    # Choose operation
    print("\nSelect operation:")
    print("  1. Addition   (A + B)")
    print("  2. Subtraction (A - B)")
    op = input("Enter choice (1 or 2): ").strip()
    if op not in ("1", "2"):
        print("Invalid choice. Exiting.")
        sys.exit(1)

    subtract = (op == "2")

    # Read operands
    try:
        a = float(input("\nEnter first operand  A: "))
        b = float(input("Enter second operand B: "))
    except ValueError:
        print("Invalid number entered. Exiting.")
        sys.exit(1)

    if prec == "1":
        # Clamp to float32 range
        a = struct.unpack('f', struct.pack('f', a))[0]
        b = struct.unpack('f', struct.pack('f', b))[0]
        fp_add_sub32(a, b, subtract)
    else:
        fp_add_sub64(a, b, subtract)


if __name__ == "__main__":
    main()
