#include <iostream>
#include <vector>
#include <random>
#include <SFML/Graphics.hpp>
#include <thread>
#include <mutex>
#include <atomic>
using namespace std;
using namespace sf;

struct VisData{
    vector<int> vec;
    mutex mtx;
    int activeIdx1=-1;
    int activeIdx2=-1;
    atomic<bool> isRunning{true};
};

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

void Bubbly(VisData& data){
    int size= data.vec.size();

    for(int i=0; i<size-1; i++){
        bool swapped=false;

        for(int j=0; j<size-1-i; j++){
            if(!data.isRunning){return;}
            
            data.activeIdx1=j;
            data.activeIdx2=j+1;

            {
            lock_guard<mutex> lock(data.mtx);
            if(data.vec[j]>data.vec[j+1]){
                swap(data.vec[j],data.vec[j+1]);
                swapped=true; 
            }
            }
            
            sleep(milliseconds(50));
        }

        if(!swapped){
            break;
        }
    }

    data.activeIdx1=-1;
    data.activeIdx2=-1;
}

int main(){
    const int dataSize=30;
    const int windowWidth=800, windowHeight=600;

    VisData data;
    data.vec = randVec(dataSize);

    RenderWindow window(VideoMode({windowWidth, windowHeight}), "Algorithm Visualizer");
    thread sortingThread(Bubbly, ref(data));

    while(window.isOpen()){
        while(const optional event = window.pollEvent()){
            if(event->is<Event::Closed>()){
                data.isRunning = false;
                window.close();
            }
        }

        window.clear();

        {
            lock_guard<mutex> lock(data.mtx);
            float barWidth = (float)windowWidth/dataSize; //Add a +2 in the denominator?
            
            for(int i=0; i<dataSize;i++){
                float barHeight = data.vec[i]*5.0f;
                RectangleShape bar(Vector2f(barWidth-2, barHeight));

                bar.setPosition(Vector2f(barWidth*i, windowHeight-barHeight));

                if(i==data.activeIdx1){
                    bar.setFillColor(Color::Green);
                }
                else if(i==data.activeIdx2){
                    bar.setFillColor(Color::Red);
                }
                else{
                    bar.setFillColor(Color::White);
                }

                window.draw(bar);
            }
        
        }
        window.display();
    }

    if(sortingThread.joinable()){
        sortingThread.join();
    }

    return 0;
}