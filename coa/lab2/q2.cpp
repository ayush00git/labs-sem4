#include<iostream>
#include<algorithm>

using namespace std;

string inverseBits(string binaryStr) {
    string compliment = "";
    for(char bit: binaryStr) {
        compliment += (bit == '0' ? '1' : '0');
    }
    return compliment;
}

pair<string, int> addBinary(string a, string b) {
    string sum = "";
    int carry = 0;
    int n = a.length();

    for(int i = n - 1; i >= 0; i--) {
        int bitA = a[i] - '0';
        int bitB = b[i] - '0';

        int total = bitA + bitB + carry;
        sum += to_string(total % 2);
        carry = total / 2;
    }
    reverse(sum.begin(), sum.end());
    return {sum, carry};
}

string subtractUsingOneS(string a, string b) {
    string bComp = inverseBits(b);

    pair<string, int> addAandBComp = addBinary(a, bComp);
    string sum = addAandBComp.first;
    int carry = addAandBComp.second;

    if (carry == 1) {
        string carryString = string(a.length() - 1, '0') + "1";
        pair<string, int> finalAdd = addBinary(sum, carryString);
        return finalAdd.first;
    } else {
        return sum;
    }
}

int main() {
string a, b;
   
    cout << "Enter a: ";
    cin >> a;
    
    cout << "Enter b: ";
    cin >> b;

    cout << "Result: " << subtractUsingOneS(a, b) << endl;

    return 0;
}