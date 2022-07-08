#include<bits/stdc++.h>

using namespace std;

int main(){
int n;
cin>>n;
vector<int> v;
for(int i=0;i<n;i++){
int num;
cin>>num;
v.push_back(num);
}
sort(v.begin(),v.end());
for(int i=0;i<(n-1);i++){
cout<<v[i]<<" ";
}
cout<<v[n-1];

return 0;
}
