#include<bits/stdc++.h>
using namespace std;

int n, m;
int alloc[10][10], maxm[10][10], avail[10], need[10][10];

void calculateNeed(){
    for(int i=0;i<n;i++)
        for(int j=0;j<m;j++)
            need[i][j] = maxm[i][j] - alloc[i][j];
}

bool isSafe(){
    bool finish[n];
    int work[m], safeSeq[n];
    for(int j=0;j<m;j++) work[j] = avail[j];

    int count = 0;
    while(count < n){
        bool found = false;
        for(int i=0;i<n;i++){
            if(!finish[i]){
                bool canRun = true;
                for(int j=0;j<m;j++)
                    if(need[i][j] > work[j]){ canRun=false; break; }

                if(canRun){
                    for(int j=0;j<m;j++) work[j] += alloc[i][j];
                    safeSeq[count++] = i;
                    finish[i] = true;
                    found = true;
                }
            }
        }
        if(!found){ cout<<"Unsafe state!\n"; return false; }
    }

    cout<<"Safe sequence: ";
    for(int i=0;i<n;i++) cout<<"P"<<safeSeq[i]<<" ";
    cout<<"\n";
    return true;
}

void input(){
    cout<<"Enter processes and resources: ";
    cin>>n>>m;

    cout<<"Allocation matrix:\n";
    for(int i=0;i<n;i++)
        for(int j=0;j<m;j++) cin>>alloc[i][j];

    cout<<"Max matrix:\n";
    for(int i=0;i<n;i++)
        for(int j=0;j<m;j++) cin>>maxm[i][j];

    cout<<"Available:\n";
    for(int j=0;j<m;j++) cin>>avail[j];
}

int main(){
    input();
    calculateNeed();
    isSafe();
}