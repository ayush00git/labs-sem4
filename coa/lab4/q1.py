class Division:
    def run(self):
        n = int(input("Enter register size (n): "))
        mask = (1 << n) - 1
        
        dividend_total = int(input(f"Enter Dividend Magnitude: "))
        divisor_mag = int(input(f"Enter Divisor Magnitude (B): "))
        as_bit = int(input("Enter Dividend Sign (As) [0 for +, 1 for -]: "))
        bs_bit = int(input("Enter Divisor Sign (Bs) [0 for +, 1 for -]: "))

        A = (dividend_total >> n) & mask  
        Q = dividend_total & mask         
        B = divisor_mag & mask
        As, Bs = as_bit, bs_bit
        
        Qs = As ^ Bs
        SC = n - 1
        E = 0
        DVF = 0
        
        print(f"\n[STEP: XOR] Qs (Sign of Quotient) = {As} XOR {Bs} = {Qs}")
        print(f"[STEP: INIT] SC = {SC} | Registers: A:{A:0{n}b} Q:{Q:0{n}b} B:{B:0{n}b}")

        b_comp = (~B & mask) + 1
        sum_val = A + b_comp
        E = 1 if sum_val > mask else 0
        A_temp = sum_val & mask
        
        print(f"[STEP: CHECK] EA <- A + B' + 1 Result: E={E}, A={A_temp:0{n}b}")

        if E == 1:
            A = (A_temp + B) & mask
            DVF = 1
            print(f"[STEP: A >= B] EA <- A + B | DVF <- {DVF}")
            print(f"[END] Divide Overflow detected. Process terminated.")
            return
        else:
            A = (A_temp + B) & mask
            DVF = 0
            print(f"[STEP: NO OVERFLOW] EA <- A + B | DVF <- {DVF}")
            print(f"[LOOP] Entering main division cycles...")

        # Main Loop
        while SC >= 0:
            print(f"\n--- Sequence Counter (SC) = {SC} ---")
            
            # shl EAQ
            combined = ((A << n) | Q) << 1
            E = 1 if (combined >> (2 * n)) & 1 else 0
            A = (combined >> n) & mask
            Q = combined & mask
            print(f"STEP: shl EAQ -> E:{E}, A:{A:0{n}b}, Q:{Q:0{n}b}")

            if E == 0:
                sum_val = A + b_comp
                E = 1 if sum_val > mask else 0
                A = sum_val & mask
                print(f"STEP: EA <- A+B'+1 -> E:{E}, A:{A:0{n}b}")
                
                if E == 1:
                    Q |= 1
                    print("PATH: E=1 (A >= B), Setting Q0 = 1")
                else:
                    A = (A + B) & mask
                    print("PATH: E=0 (A < B), Restoring A (EA <- A+B)")
            else:
                A = (A + b_comp) & mask
                Q |= 1
                print(f"PATH: E=1 (from shift), A <- A+B'+1, Setting Q0 = 1")

            SC -= 1

        print("\n" + "="*40)
        print(f"ALGORITHM END")
        print(f"Final Quotient (Q):  {'-' if Qs else '+'}{Q} ({Q:0{n}b})")
        print(f"Final Remainder (R): {'-' if As else '+'}{A} ({A:0{n}b})")
        print("="*40)

if __name__ == "__main__":
    Division().run()