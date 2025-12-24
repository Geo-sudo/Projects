#include <iostream>
#include <vector>
#include <random>
using namespace std;

vector<int> randVec(int size){
    vector<int> vec;
    const int min=1, max=100;

    static random_device rd;
    static mt19937 gen(rd());
    uniform_int_distribution<> distr(min, max);

    for(int i=0; i<size; i++){
        vec.push_back(distr(gen));
    }

    return vec;
}

void Bubbly(vector<int>& vec, int size){
    int swap;
    for(int i=0; i<size-1; i++){
        bool swapped=false;

        for(int j=0; j<size-1-i; j++){
            if(vec[j]>vec[j+1]){
                swap=vec[j];
                vec[j]=vec[j+1];
                vec[j+1]=swap;
                
                swapped=true; 
            }
        }

        if(!swapped){
            break;
        }
    }
}

int main(){
    const int size=10;

    return 0;
}