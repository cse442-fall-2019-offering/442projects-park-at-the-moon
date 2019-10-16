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
#include <map>

class Wheel{
public:
//    use an static auto increase for to allocate index for each wheel
    static int id;
    Wheel();
    Wheel(const cv::Vec3f & circle, int frame);
    cv::Vec3f circle;
    std::vector<float> xPosVec;
//    a flag to mark whether the wheel is tracked in current frame
    bool isTracked;
//    index for tracking
    int index;

    int frame;
};

class Car
{
public:
    Car(const Wheel& wheel, int id, int velocity, int frontBack);
    Wheel front;
    Wheel back;
    // 1 for front, 2 for back, 3 for both
    int frontBack;
    float velocity;
    int id;
    
};

struct Camera 
{
    std::vector<Car> partialCars;
    // should be sorted by x coordinates
    std::vector<Car> cars;
//  key is the frame number, value is a vector of all the x points at that frame
    std::map<int, std::vector<float>> xPoints;
    int carCount;
    // x value splitting between left and right region of image
    float splitRegion;
};

#endif /* Wheel_hpp */
