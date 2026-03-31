// Write a program with inputs 00, 01, 10, and 11, find the OR, NOR, XOR, and XNOR output.
// Present all output in tabular form.

#include<iostream>
#include<bits/stdc++.h>
using namespace std;

int main() {

    vector<pair<int, int>> inputs = { {0, 0}, {0, 1}, {1, 0}, {1, 1} };

    for(const auto& pair: inputs ) {
        int a = pair.first;
        int b = pair.second;

        int or_out = a | b;
        int nor_out = !( a | b );
        int xor_out = a ^ b;
        int xnor_out = !( a ^ b );
        
        cout << a << "\t" << b << "\t|\t" 
             << or_out << "\t" 
             << nor_out << "\t" 
             << xor_out << "\t" 
             << xnor_out << endl;
    }

}
