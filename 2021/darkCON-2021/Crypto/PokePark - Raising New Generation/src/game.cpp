#include <iostream> 
#include <chrono> 
#include <random>
#include <fstream>
using namespace std; 

// compile
// g++ game.cpp -o game -std=c++11 -s -Wall -g -O3

void intro(){
    cout << "\x1b[33m.- .-.. .-../- .... ./-... . ... -/-....-/.-. . -.-- .--.-. -.. .- .-. -.- .- .-. -- -.-- -.--. ..--- ----- ..--- .---- -.--.- \x1b[0m\n\n";
    cout << "\x1b[32m Oak: \x1b[0m Hello, there! Glad to meet you!\n";
    cout << "\x1b[32m Oak: \x1b[0m Welcome to the world of POKéMON! My name is Oak.\n";
    cout << "\x1b[32m Oak: \x1b[0m This world is inhabited far and wide by creatures called POKéMON.\n";
    cout << "\x1b[32m Oak: \x1b[0m For some people, POKéMON are pets. Others use them for fights. Myself...\n\tI study POKéMON as a profession.\n";
    cout << "\x1b[32m Oak: \x1b[0m But first, tell me a little about yourself.\n\n";
    cout << "\x1b[32m Oak: \x1b[0m What is your name?\n\x1b[33m [?]>  \x1b[0m";

    string name;
    cin >> name;

    cout << "\x1b[32m Oak: \x1b[0m Right! So your name is \x1b[36m " << name << "\x1b[0m!\n\n";
    cout << " [ After so many tries \x1b[36m " << name << "\x1b[0m couldn't defeat The Elite Four and decides to get some tips from me ( PROF. Oak ) ]\n\n";
    cout << "\x1b[32m Oak: \x1b[0m I know what you need. Mewtow is held inside this POKé Ball. If you can GUESS the next number then it's yours!!!\n\n";
    cout << "\x1b[33m.- .-.. .-../- .... ./-... . ... -/-....-/.-. . -.-- .--.-. -.. .- .-. -.- .- .-. -- -.-- -.--. ..--- ----- ..--- .---- -.--.- \x1b[0m\n\n";
}

int main(){

    unsigned seed = chrono::system_clock::now().time_since_epoch().count(); 
    
    minstd_rand0 generator (seed);

    intro();
    cout << " ================\n ||  I CHOOSE  ||\n ================\n\n";
    for(int i = 0; i < 10; i++){
        cout << " " << generator() << "\n"; 
    }

    int next = generator();
    int guess;

    cout << "\n\x1b[33m What's Next?\n [?]>  \x1b[0m";
    cin >> guess;

    if(next == guess){
        cout << "\n\x1b[92m ================ !!! CORRECT !!! ================ \x1b[0m \n\n";
        string flag;
        ifstream file("flag.txt");
        while(getline(file, flag)){
            cout << flag << "\n";
        }
        file.close();
        exit(0);
    }
    else{
        cout << "\n\x1b[31m ===== !!! W R O N G !!! =====\n\n      !!! TRY HARDER !!! \x1b[0m";
    }

    return 0;
}
