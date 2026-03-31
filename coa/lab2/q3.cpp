#include<iostream>
#include<cmath>
#include<bitset>

using namespace std;

template <class T>
void printInfo(string label, T val, int bits) {
    if (bits == 8) {
        cout << bitset<8>(val) << endl;
    } else {
        cout << bitset<16>(val) << endl;
    }
}

void SignExtension(int8_t num) {
    cout << "\n--- (a) Sign extension ---" << endl;
    printInfo("Original (8-bit)", num, 8);
    
    int16_t extended = (int16_t)num;
    
    printInfo("Extended (16-bit)", extended, 16);
    
    if (num == extended) {
        cout << ">> Result: Value preserved correctly." << endl;
    }
}


void LeftShift(int8_t num, int k) {
    cout << "\n--- (b) Left Shift by " << k << " (Multiply by " << pow(2, k) << ") ---" << endl;
    printInfo("Original", num, 8);
    
    int8_t shifted = num << k;
    
    printInfo("Shifted ", shifted, 8);
    
    int expected = num * (int)pow(2, k);
    if (shifted == (int8_t)expected) {
        cout << ">> Verify: " << (int)num << " * " << pow(2, k) << " = " << (int)shifted << endl;
    } else {
        cout << ">> Warning: Overflow occurred (common in fixed 8-bit systems)." << endl;
    }
}

void RightShift(int8_t num, int k) {
    cout << "\n--- (c) Right Shift by " << k << " (Divide by " << pow(2, k) << ") ---" << endl;
    printInfo("Original", num, 8);
    
    int8_t shifted;
    int8_t sign_mask = 0;
    if (num < 0) {
        sign_mask = ~(0xFF >> k); 
        shifted = (num >> k) | sign_mask;
    } else {
        shifted = num >> k;
    }
    
    printInfo("Shifted ", shifted, 8);
    cout << ">> Verify: " << (int)num << " / " << pow(2, k) << " (floor) = " << (int)shifted << endl;
}

int main() {
    int n;
    cout << "Input to verify sign extension: ";
    cin>>n;

    SignExtension(n);

    int b, a;
    cout << "Input a: ";
    cin >> a;
    cout << "Input b: ";
    cin >> b;
    LeftShift(a, b); 
    
    int x, y;
    cout << "Input x: ";
    cin >> x;
    cout << "Input y: ";
    cin >> y;
    RightShift(x, y);
    
}