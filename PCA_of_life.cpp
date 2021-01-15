#include <iostream>
#include <vector>
#include <string>
#include <random>
#include <fstream>
using namespace std;
const int windowX = 20;
const int windowY = 10;
vector <vector<int>> statespace, syncspace;
default_random_engine generator;

int previous_states[3]={0,0,0};

void sync(){
    for (int y=0;y<windowY;y++){
        for (int x=0;x<windowX;x++){
            if (y==0 || y==windowY-1 || x==0 || x==windowX-1){
                syncspace[y][x] = 0;
            }
            statespace[y][x] = syncspace[y][x];
        }
    }
}

int random_state(vector<float> weights){
    double result[3];
    for (int index=0;index<3;index++){
        result[index] = (double)(weights[index]*10);
    }
    
    discrete_distribution<int> distribution {result[0],result[1],result[2]};
    int number = distribution(generator);
    return number;

}

vector<float> majority_transmatrix(int majoritystate, int currentstate, float p, float q, float z){
    vector< vector< vector<float> > > TRANSMATRIX  {
        {{1-q,q,0},
         {1-q,q,0},
         {1,0,0}},
        
        {{p,1-p,0},
         {p,1-p,0},
         {1,0,0}},
        
        {{1,0,0},
         {0,1-z,z},
         {1,0,0}}};
    return TRANSMATRIX [majoritystate][currentstate];
}

float check_stable(){
    int states[3] = {0,0,0};
    for (int y = 1; y<windowY-1;y++){
        for (int x = 1; x<windowX-1;x++){
            states[statespace[y][x]]++;
        }
    }
    if(states[0] >0.8*(windowX-2)*(windowY-2)){
        cout<<states[0]<<endl;
        return 0.0;
    }
    else if(states[1] >0.8*(windowX-2)*(windowY-2)){
        cout<<states[1]<<endl;
        return 1.0;
    }
    else if (states[2]>60){
        return 2.0;
    }
    return -1.0;
}

int majority_cell_state(int y , int x, string rule){
    vector <int> numofstatecells {0,0,0};
    if (rule =="Moore" && x != 0 && x!=windowX-1 && y !=0 && y != windowY-1){
        numofstatecells[statespace[y-1][x]]+=1;
        numofstatecells[statespace[y-1][x+1]]+=1;
        numofstatecells[statespace[y][x+1]]+=1;
        numofstatecells[statespace[y+1][x+1]]+=1;
        numofstatecells[statespace[y+1][x]]+=1;
        numofstatecells[statespace[y+1][x-1]]+=1;
        numofstatecells[statespace[y][x-1]]+=1;
        numofstatecells[statespace[y-1][x-1]]+=1;
        numofstatecells[statespace[y][x]]+=1;
    }
    else if (rule == "Neu" && x != 0 && x!=windowX-1 && y !=0 && y != windowY-1){
        numofstatecells[statespace[y-1][x]]+=1;
        numofstatecells[statespace[y][x+1]] +=1;
        numofstatecells[statespace[y+1][x]] +=1;
        numofstatecells[statespace[y][x-1]]+=1;
        numofstatecells[statespace[y][x]]+=1;
    }

    else if (rule == "NEC" && x != 0 && x!=windowX-1 && y !=0 && y != windowY-1){
        numofstatecells[statespace[y-1][x]]+=1;
        numofstatecells[statespace[y][x+1]]+=1;
        numofstatecells[statespace[y][x]]+=1;
    }
    if (numofstatecells[2]>0){
        return 2;
    }
    vector <int> majoritycellstate {0,0};
    for (int stateindex = 0; stateindex < numofstatecells.size(); stateindex++){
        if (numofstatecells[stateindex] > majoritycellstate[0]){
            majoritycellstate[1] = stateindex;
            majoritycellstate[0] = numofstatecells[stateindex];
        }
    }
    
    return majoritycellstate[1];
}

void print_state(){
    for (int y=0;y<windowY;y++){
        for (int x=0;x<windowX;x++){
            cout<< (int) statespace[y][x];
        }
        cout << endl;
    }
}

void update_state (int y, int x, string rule, float p, float q, float z){
    if (x!=0 && x!=windowX-1 && y !=0 && y != windowY-1){
        int majoritycellstate = majority_cell_state(y,x,rule);
        int futurecellstate = random_state(majority_transmatrix(majoritycellstate, statespace[y][x],p,q,z));
        syncspace[y][x] = futurecellstate;
    }
}

void init_conditions(){
    for (int y =0;y<windowY;y++){
        for (int x=0;x<windowX;x++){
            syncspace[y][x] = 0;
        }
    }
    for (int x =0;x<100;x++){
        uniform_int_distribution<int> distributionY (1,windowY-2);
        uniform_int_distribution<int> distributionX(1,windowX-2);
        int randomX = distributionX(generator);
        int randomY = distributionY(generator);
        syncspace [randomY][randomX] = 1;
    }
    //syncspace[windowY-2][windowX-2] =2;
    //syncspace[windowY-3][windowX-2]=1;
    //syncspace[windowY-2][windowX-3]=1;

    sync();
    print_state();
}

int game_loop(){
    vector<vector<float>>output_to_file {};
    float p=0.0;
    for (int piter=0;piter<99;piter++){
        p+=0.01;
        float q=0;
        for (int qiter=0;qiter<99;qiter++){
            q+=0.01;
            float z=0;
            //for (int ziter=0;ziter<9;ziter++){
            //    z+=0.1;
            bool end = false;
            float iterations= 0;
            init_conditions();
            while (end ==false){
                iterations+=1;
                for (int y =0;y<windowY;y++){
                    for (int x=0;x<windowX;x++){
                        update_state(y,x,"Moore",p,q,z);
                    }
                }
                sync();
                float stable_config = check_stable();
                if ( stable_config != -1){
                    print_state();
                    cout<< "p = "<<p<<" q = "<<q<<" z = "<<z<<" iterations = "<<iterations<<endl;
                    vector<float> temp = {p,q,z,stable_config, iterations};
                    output_to_file.push_back(temp);
                    end = true;
                }
                if (iterations>300){
                    end = true;
                    cout<<"stable configuration was never reached"<<endl;
                    print_state();
                    cout<< "p = "<<p<<" q = "<<q<<" z = "<<z<<" iterations = "<<iterations<<endl;
                    vector<float> temp = {p,q,z,stable_config, iterations};
                    output_to_file.push_back(temp);
                 //   }
                }
            }
        }
    }
    ofstream data_file;
    data_file.open("data_output.txt");
    for (int index=0;index<output_to_file.size();index++){
        data_file<<output_to_file[index][0]<<" "<<output_to_file[index][1]<<" "<<output_to_file[index][2]<<" "<<output_to_file[index][3]<<" "<<output_to_file[index][4]<<endl;
    }
    data_file.close();
    return 0;
}

void setup(){
    for (int y=0;y<windowY;y++){
        statespace.push_back({});
        syncspace.push_back({});
       for (int x=0;x<windowX;x++){
            statespace[y].push_back(0);
            syncspace[y].push_back(0);
        }
    }
}

int main() {
    setup();
    game_loop();
    int hi;
    cin>>hi;
    return 0;
}