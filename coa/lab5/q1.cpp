#include <iostream>
using namespace std;

int main()
{
    double m1, m2;
    int e1, e2;
    int choice;
    int bias;
    int sign = 1;
    cout << "Choose Precision\n";
    cout << "1. Single Precision\n";
    cout << "2. Double Precision\n";
    cout << "Enter choice: ";
    cin >> choice;
    if (choice == 1)
        bias = 127;
    else
        bias = 1023;
    cout << "\nEnter mantissa of multiplicand: ";
    cin >> m1;
    cout << "Enter exponent of multiplicand: ";
    cin >> e1;

    cout << "Enter mantissa of multiplier: ";
    cin >> m2;
    cout << "Enter exponent of multiplier: ";
    cin >> e2;
    if (m1 < 0) { sign *= -1; m1 = -m1; }
    if (m2 < 0) { sign *= -1; m2 = -m2; }
    cout << "\n===== FLOATING POINT MULTIPLICATION STEPS =====\n";
    cout << "\nStep 1: Check for Zero\n";
    if (m1 == 0 || m2 == 0) {
        cout << "One of the operands is zero.\n";
        cout << "Result = 0\n";
        return 0;
    }
    cout << "Both operands are non-zero.\n";
    cout << "\nStep 2: Add the Exponents\n";
    int b = e1 + bias;
    int q = e2 + bias;
    cout << "Modified exponent of multiplicand (b) = " << e1 << " + " << bias << " = " << b << endl;
    cout << "Modified exponent of multiplier (q) = " << e2 << " + " << bias << " = " << q << endl;
    int a = b + q - bias;
    cout << "Result exponent (a) = b + q - bias = " << b << " + " << q << " - " << bias << " = " << a << endl;
    cout << "\nStep 3: Multiply the Mantissas\n";
    double mantissa = m1 * m2;
    cout << "Mantissa = " << m1 << " * " << m2 << " = " << mantissa << endl;
    cout << "\nStep 4: Normalize the Result\n";
    while (mantissa >= 1) {
        mantissa /= 10;
        a++;
        cout << "Shift Right -> Mantissa = " << mantissa << ", Exponent = " << a << endl;
    }
    while (mantissa < 0.1) {
        mantissa *= 10;
        a--;
        cout << "Shift Left -> Mantissa = " << mantissa << ", Exponent = " << a << endl;
    }
    if (sign < 0) mantissa = -mantissa;
    cout << "\n===== FINAL RESULT =====\n";
    cout << "Normalized Result = " << mantissa << " x 10^" << a << endl;
    return 0;
}
