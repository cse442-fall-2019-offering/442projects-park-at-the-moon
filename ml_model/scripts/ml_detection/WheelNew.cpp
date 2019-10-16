//
//  Wheel.cpp
//  CarWheelVelocities
//
//  Created by tab on 4/27/18.
//  Copyright © 2018 tab. All rights reserved.
//

#include "WheelNew.hpp"

int Wheel::id = -1;
Wheel::Wheel(const cv::Vec3f & circle, const int fr):circle(circle),isTracked(false),index(id++), frame(fr){
}
Wheel::Wheel(){}
// frontBack is true if front wheel
Car::Car(const Wheel& wheel, int new_id, int new_velocity, int new_frontBack): id(new_id), velocity(new_velocity){
    if (new_frontBack != 1 && new_frontBack != 2) {
        std::cout << "frontBack must be 1 (front) or 2 (back) during initialization" << std::endl;
        return;
    }
    if (new_frontBack == 1) {
        front = wheel;
        frontBack = new_frontBack;
    }
    else {
        back = wheel;
        frontBack = new_frontBack;
    }
}
