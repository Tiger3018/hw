#include "car/car.hpp"
#include <iostream>
#include <cmath>
#include <boost/format.hpp>
using std :: cout, std :: endl, boost :: format;

void car::run(void)
{
    if(!this -> state_)
    {
        cout << "Car previously stopped! Now position " << format("%6.3lf %6.3lf") % this -> position_x_% this -> position_y_ << endl;
        this -> state_ = true;
        return;
    }
    this -> position_toward_ += this -> velocity_angular_;
    this -> position_x_ += cos(position_toward_) * this -> velocity_linear_;
    this -> position_y_ += sin(position_toward_) * this -> velocity_linear_;
    cout << format("Current position: %6.3lf, %6.3lf\nCurrent velocity: %6.3lf, %6.3lfrad\n") % 
        this -> position_x_% this -> position_y_% this -> velocity_linear_% this -> velocity_angular_;
    return;
}

void car::run(double velocityLinear, double velocityAngular)
{
    this -> set_linear_speed(velocityLinear);
    this -> set_angular_speed(velocityAngular);
    this -> run();
    return;
}
    

void car::stop(void)
{
    this -> state_ = false;
    cout << "Car now stop!" << endl;
    return;
}

bool car::set_linear_speed(double value)
{
    this -> velocity_linear_ = value;
    return true;
}

bool car::set_angular_speed(double value)
{
    this -> velocity_angular_ = value;
    return true;
}
