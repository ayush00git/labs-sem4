// A B Bin values possible - 000 001 010 011 100 101 110 111

#include<iostream>
#include<bits/stdc++.h>
using namespace std;

struct inputSet {
    int a;
    int b;
    int bin;
};

int main() {

    vector<inputSet> inputs;

    for( int a = 0; a <= 1; a++ ) {
        for( int b = 0; b <= 1; b++ ) {
            for( int bin = 0; bin <= 1; bin++ ) {
                inputs.push_back({ a, b, bin });
            }
        }
    }

    for( const auto& it: inputs ) {
        int xor1 = ( it.b ^ it.bin );
        int d = ( it.a ^ xor1 );

        int and1 = (( !it.b ) && ( it.bin ));
        int and2 = (( it.a ) && !( xor1 ));

        int bout = ( and1 || and2 );
        cout << it.a << "\t" << it.b << "\t" << it.bin << "\t|\t" << d << "\t" << bout << endl;

    }
}