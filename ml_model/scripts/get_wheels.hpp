#ifndef get_wheels_hpp
#define get_wheels_hpp

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
// how far off the difference in velocity can be between wheels to determine it's the same wheel
#define VELOCITY_ERROR 1000
// how often (in seconds) data should get sent to the server for comparison
#define SERVER_INTERVAL 10
// dead time, i.e. if the wheel has been sitting in the vector for 
// this long, then we remove it
#define DEAD_INTERVAL 1000
// once the wheel has reached this amount from both sides of the image
// it has made its total path, and we can remove it
#define COMPLETE_MARGIN 10
// max difference in time (TODO: in ms i think) between 2 points that would
// still allow consideration of those 2 points belong to the same wheel
#define TIME_ERROR 200


class WheelPath {
private:
    static int total_id;
public:
    // this represents that another wheelpath was found to form a car
    // in conjunction with this wheelpath
    int other_wheelpath;
    float radius;
    int id;
    WheelPath(float r): radius(r) {
        id = ++total_id;
    }
    // index 0 is x-coordinate
    // index 1 is velocity
    // index 2 is timestamp
    // index 3 is frame number
    std::vector<std::vector<float>> wheel; 
};

class Car {
public:
    WheelPath *left;
    WheelPath *right; 
    Car (): left(NULL), right(NULL) {}
};
class Camera {
private:
    std::vector<WheelPath> all_wheels;
    // current count of previous car detection run
    int count;
    // for wheels that have not found their way to a timeframe of wheels (yet)
    // index 0 is x-coordinate
    // index 1 is radius
    // index 2 is timestamp
    // index 3 is frame number
    std::vector<std::vector<float>> unknown_wheels;
    // TODO: change this back to private
    void clean_data(double cur_time);
public:
    Camera(): count(0) {}
    float get_velocity (float start_x, float start_time, float last_x, float last_time);
    bool find_existing_wheelpoint(float x_coord, float time, int frame);
    bool find_existing_wheelpath(float x_coord, float time, int frame);
    void add_unknown_point(float x_coord, float radius, float timestamp, int frame);
    bool combine_wheelpaths(WheelPath &wheelpath);
    // getting velocity by checking first x coordinate with current x coordinate
    void compare_velocity(float velocity, int &idex);
    // TODO: I should probably check radius of incoming wheel and existing wheel
    //       as an added level of security
    void add_point(float x_coord, float radius, float timestamp, int frame);
    void send_data_to_server(double cur_time);     
    std::vector<WheelPath> get_all_wheels();
    std::vector<std::vector<float>> get_unknown_wheels();
    void find_cars();
    void car_count();
    float get_average_velocity(std::vector<std::vector<float>> &wheelpath);

};
#endif /* end count_cars.hpp */
