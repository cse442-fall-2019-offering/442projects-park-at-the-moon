//
//  Wheel.hpp
//  CarWheelVelocities
//
//  Created by tab on 4/27/18.
//  Copyright © 2018 tab. All rights reserved.
//

#ifndef Wheel_hpp
#define Wheel_hpp

#include <stdio.h>
#include <vector>
#include <opencv2/opencv.hpp>
#include "../get_wheels.hpp"

class Wheel{
public:
//    use an static auto increase for to allocate index for each wheel
    static int id;
    Wheel(const cv::Vec3f & circle);
    cv::Vec3f circle;
    std::vector<float> xPosVec;
//    index for tracking
    int index;
};

#endif /* Wheel_hpp */
