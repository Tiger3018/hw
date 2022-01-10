#include"car/car.hpp"
#include<iostream>
using namespace std;

car mycar(10, 1);

int main()
{
    char opera;
    double a, b;
    cout << "car program" << endl;
    while(cin >> opera) // exit when EOF(^D)
    {
        switch(opera)
        {
            case '1': // only run
            mycar.run();
            break;

            case '2': // run with new vel
            cin >> a >> b;
            mycar.run(a, b);
            break;

            case '3': // linear vel
            cin >> a;
            mycar.set_linear_speed(a);
            break;

            case '4': // algebra vel
            cin >> a;
            mycar.set_angular_speed(a);
            break;

            case '5': // stop
            mycar.stop();
            break;
        }
    }
    return 0;
}
