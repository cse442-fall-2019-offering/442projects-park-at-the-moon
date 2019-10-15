#ifndef count_cars_hpp
#define count_cars_hpp

#include <iostream>
#include <vector>
#include <cmath>

/* TODO: update these values */
// frames per second of the video
#define FRAMES_SECOND 400
// distance (mm) from left side of image to right side of image (relative to road)
#define DISTANCE 15000
// total pixels for a single row in image
#define PIXELS_DISTANCE 840
#define VELOCITY_ERROR 1


class Wheel {
private:
    static int total_id;
public:
    float radius;
    int id;
    Wheel(float r): radius(r) {
        id = total_id++;
    }
    // index 0 is x-coordinate
    // index 1 is velocity
    // index 2 is timestamp
    // index 3 is frame number
    std::vector<std::vector<float>> wheel;
    
};

class Cars {
private:
    std::vector<Wheel> all_wheels;
    // for wheels that have not found their way to a timeframe of wheels (yet)
    // index 0 is x-coordinate
    // index 1 is radius
    // index 2 is timestamp
    // index 3 is frame number
    std::vector<std::vector<float>> unknown_wheels;
public:
    float get_velocity (float start_x, float start_time, float last_x, float last_time);
    void find_closest_unknown(float x_coord, int &index, float &min_distance);
    void find_closest_known(float x_coord, int &index, float &min_distance);
    // getting velocity by checking first x coordinate with current x coordinate
    void compare_velocity(float velocity, int &idex);
    // TODO: I should probably check radius of incoming wheel and existing wheel
    //       as an added level of security
    void add_point(float x_coord, float radius, float timestamp, int frame);
     
    std::vector<Wheel> get_all_wheels();
    std::vector<std::vector<float>> get_unknown_wheels();
};
#endif /* end count_cars.hpp */
