#include <iostream>
#include <cmath>
#include <string>
#include <algorithm>

using namespace std;

double binaryToDecimal(string binaryStr) {
    size_t pointPos = binaryStr.find('.');
    string integerPart = "";
    string fractionalPart = "";

    if (pointPos != string::npos) {
        integerPart = binaryStr.substr(0, pointPos);
        fractionalPart = binaryStr.substr(pointPos + 1);
    } else {
        integerPart = binaryStr;
    }

    double decimalValue = 0.0;

    int intPower = 0;
    for (int i = integerPart.length() - 1; i >= 0; i--) {
        if (integerPart[i] == '1') {
            decimalValue += pow(2, intPower);
        }
        intPower++;
    }

    for (int i = 0; i < fractionalPart.length(); i++) {
        if (fractionalPart[i] == '1') {
            decimalValue += pow(2, -(i + 1));
        }
    }

    return decimalValue;
}

// (b) Decimal to Binary
string decimalToBinary(long long n) {
    if (n == 0) return "0";
    string binaryStr = "";
    while (n > 0) {
        binaryStr = (n % 2 == 0 ? "0" : "1") + binaryStr;
        n /= 2;
    }
    return binaryStr;
}

// Helper for Binary to Hex
char fourBitToHex(string chunk) {
    if (chunk == "0000") return '0';
    if (chunk == "0001") return '1';
    if (chunk == "0010") return '2';
    if (chunk == "0011") return '3';
    if (chunk == "0100") return '4';
    if (chunk == "0101") return '5';
    if (chunk == "0110") return '6';
    if (chunk == "0111") return '7';
    if (chunk == "1000") return '8';
    if (chunk == "1001") return '9';
    if (chunk == "1010") return 'A';
    if (chunk == "1011") return 'B';
    if (chunk == "1100") return 'C';
    if (chunk == "1101") return 'D';
    if (chunk == "1110") return 'E';
    if (chunk == "1111") return 'F';
    return '?';
}

// (c) Binary to Hexadecimal (with leading padding)
string binaryToHex(string binaryStr) {
    while (binaryStr.length() % 4 != 0) {
        binaryStr = "0" + binaryStr; // Leading zeros
    }
    string hexStr = "";
    for (int i = 0; i < binaryStr.length(); i += 4) {
        hexStr += fourBitToHex(binaryStr.substr(i, 4));
    }
    return hexStr;
}

// (d) Hexadecimal digit to 4-bit Binary
string hexToBinary(char hexDigit) {
    hexDigit = toupper(hexDigit);
    switch (hexDigit) {
        case '0': return "0000"; 
        case '1': return "0001";
        case '2': return "0010"; 
        case '3': return "0011";
        case '4': return "0100"; 
        case '5': return "0101";
        case '6': return "0110"; 
        case '7': return "0111";
        case '8': return "1000"; 
        case '9': return "1001";
        case 'A': return "1010"; 
        case 'B': return "1011";
        case 'C': return "1100"; 
        case 'D': return "1101";
        case 'E': return "1110"; 
        case 'F': return "1111";
        default: return "Invalid";
    }
}

// (e) Hexadecimal to Decimal
long long hexToDecimal(string hexStr) {
    long long decimalValue = 0;
    for (char digit : hexStr) {
        digit = toupper(digit);
        int value = (digit >= '0' && digit <= '9') ? (digit - '0') : (digit - 'A' + 10);
        decimalValue = (decimalValue * 16) + value;
    }
    return decimalValue;
}

// (f) Decimal to Signed Magnitude
string decimalToSignedMagnitude(int n, int totalBits = 8) {
    char signBit = (n < 0) ? '1' : '0';
    string magnitudeBin = decimalToBinary(abs(n));
    if (magnitudeBin.length() > (totalBits - 1)) return "Overflow for " + to_string(totalBits) + " bits";
    while (magnitudeBin.length() < (totalBits - 1)) magnitudeBin = "0" + magnitudeBin;
    return signBit + magnitudeBin;
}
int main() {
    int choice;
    string inputStr;
    long long inputNum;

    do {
        cout << "\n1. Binary to Decimal";
        cout << "\n2. Decimal to Binary";
        cout << "\n3. Binary to Hexadecimal";
        cout << "\n4. Hex Digit to 4-bit Binary";
        cout << "\n5. Hexadecimal to Decimal";
        cout << "\n6. Decimal to Signed Magnitude";
        cout << "\n0. Exit";
        cout << "\nEnter choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "Enter Binary string: "; cin >> inputStr;
                cout << "Result (Decimal): " << binaryToDecimal(inputStr) << endl;
                break;
            case 2:
                cout << "Enter Decimal number: "; cin >> inputNum;
                cout << "Result (Binary): " << decimalToBinary(inputNum) << endl;
                break;
            case 3:
                cout << "Enter Binary string: "; cin >> inputStr;
                cout << "Result (Hex): " << binaryToHex(inputStr) << endl;
                break;
            case 4:
                char hexCh;
                cout << "Enter Hex digit: "; cin >> hexCh;
                cout << "Result (4-bit Binary): " << hexToBinary(hexCh) << endl;
                break;
            case 5:
                cout << "Enter Hex string: "; cin >> inputStr;
                cout << "Result (Decimal): " << hexToDecimal(inputStr) << endl;
                break;
            case 6:
                int sNum, bits;
                cout << "Enter Decimal number: "; cin >> sNum;
                cout << "Enter total bit length (e.g., 8): "; cin >> bits;
                cout << "Result (Signed Magnitude): " << decimalToSignedMagnitude(sNum, bits) << endl;
                break;
            case 0:
                cout << "Exiting..." << endl;
                break;
            default:
                cout << "Invalid selection!" << endl;
        }
    } while (choice != 0);

}