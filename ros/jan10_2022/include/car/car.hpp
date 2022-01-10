#pragma once
class car
{
    private:
    bool state_ = false;
    double velocity_linear_, velocity_angular_, position_x_ = 0, position_y_ = 0, position_toward_ = 0;
    public:
    explicit car(){};
    explicit car(double a, double b)
        : velocity_linear_(a)
        , velocity_angular_(b)
    {};
    void run(void);
    void run(double velocityLinear, double velocityAngular);
    void stop(void);
    bool set_linear_speed(double value);
    bool set_angular_speed(double value);
};
