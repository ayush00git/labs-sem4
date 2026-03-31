#include <iostream>
#include <bitset>
#include <iomanip>
#include <cmath>
#include <cstdint>
using namespace std;

const int BITS = 64;     
const int FRAC_BITS = 8;  

int64_t toFixed(double x) {
    return (int64_t) llround(x * (1LL << FRAC_BITS));
}

double toDouble(int64_t x) {
    return (double)x / (1LL << FRAC_BITS);
}

void printRow(int step, const string& op, int64_t EA, int E, int AVF) {
    cout << left
         << setw(6) << step
         << setw(45) << op
         << setw(70) << bitset<BITS>(EA)
         << setw(6) << E
         << setw(6) << AVF
         << endl;
}

int main() {
    double A_in, B_in;
    char op;
    int step = 1;

    cout << "Enter A: ";
    cin >> A_in;
    cout << "Enter B: ";
    cin >> B_in;
    cout << "Operation (+ or -): ";
    cin >> op;

    int64_t A = toFixed(A_in);
    int64_t B = toFixed(B_in);

    int As = (A < 0);
    int Bs = (B < 0);

    int64_t EA = 0;
    int E = 0;
    int AVF = 0;

    cout << "A = " << A_in << "\nBinary: " << bitset<BITS>(A) << "  As=" << As << endl;
    cout << "B = " << B_in << "\nBinary: " << bitset<BITS>(B) << "  Bs=" << Bs << endl;

    cout << left
         << setw(6) << "Step"
         << setw(45) << "Operation"
         << setw(70) << "EA"
         << setw(6) << "E"
         << setw(6) << "AVF"
         << endl;

    cout << string(135, '-') << endl;

    int xorSign = As ^ Bs;
    printRow(step++, "Compute As XOR Bs = " + to_string(xorSign), 0, 0, 0);

    // ================= ADDITION =================
    if (op == '+') {
        EA = A + B;

        // signed overflow detection
        if ((A >= 0 && B >= 0 && EA < 0) || (A < 0 && B < 0 && EA >= 0))
            AVF = 1;

        printRow(step++, "EA <- A + B", EA, E, AVF);
    }

    // ================= SUBTRACTION =================
    else if (op == '-') {

        if (xorSign == 1) {
            printRow(step++, "As != Bs -> reduce to ADD magnitudes", 0, 0, 0);

            int64_t B_mag = llabs(B);
            EA = A + B_mag;

            printRow(step++, "EA <- A + |B|", EA, E, 0);
        }
        else {
            printRow(step++, "As == Bs -> true subtraction", 0, 0, 0);

            EA = A - B;
            printRow(step++, "EA <- A - B", EA, E, 0);
        }
    }
    else {
        cout << "Invalid operation\n";
        return 0;
    }

    // -------- Final result --------
    double result = toDouble(EA);

    cout << "\n--- FINAL RESULT ---\n";
    cout << "Result (Decimal): " << result << endl;
    cout << "Result (Binary) : " << bitset<BITS>(EA) << endl;
    cout << "Final As        : " << (EA < 0) << endl;

}
