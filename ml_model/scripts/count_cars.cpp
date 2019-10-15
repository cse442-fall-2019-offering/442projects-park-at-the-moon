#include <iostream>
#include <vector>
#include <cstdlib>

/* TODO: update these values */
// frames per second of the video
#define FRAMES_SECOND 400
// distance (mm) from left side of image to right side of image (relative to road)
#define DISTANCE 15000
// total pixels for a single row in image
#define PIXELS_DISTANCE 840
#define VELOCITY_ERROR .5


class Wheel {
public:
    float radius;
    
    // index 0 is x-coordinate
    // index 1 is velocity
    // index 2 is timestamp
    // index 3 is frame number
    std::vector<std::vector<float>> wheel;
    
};

static std::vector<Wheel> all_wheels;

// for wheels that have not found their way to a timeframe of wheels (yet)
//
// index 0 is x-coordinate
// index 1 is radius
// index 2 is timestamp
// index 3 is frame number
static std::vector<std::vector<float>> unknown_wheels;

// TODO: every 10 seconds or so, I should send the data to the server, and then clean vectors.
// By clean, I mean look for wheels that have been in the dataset for more than 10 seconds or so
// and remove them. 
// 

// TODO: should the velocity be between the last and current point, or from the start and current point?
// for now I'll do from the starting xpoint
float get_velocity (float start_x, float start_time, float last_x, float last_time) {

    // TODO: how many digits should we allow for time?
    float distance = last_x - start_x;
    float time = last_time - star_time;

    return distance / time;

}
void find_closest_unknown(float xCoord, vector<float> *closest_wheel, float &min_distance) {
    float temp_distance;
    float last_x;
    float last_velocity;
    for (auto &wheel : unknown_wheels) {
        // get the xCoord of the last added point
        last_x = wheel->wheel.back().front();
        if (temp_distance < min_distance){
            min_distance = temp_distance;
            closest_wheel = &wheel;
        } // if wheel is moving to the left
       else if (abs(temp_distance) < min_distance) {
                min_distance = temp_distance;
                closest_wheel = &wheel;
            }
    }
}
void find_closest_known(float xCoord, Wheel *closest_wheel, float &min_distance) {

    float temp_distance;
    float last_x;
    float last_velocity;
    for (auto &wheel : all_wheels) {
        // get the xCoord of the last added point
        last_x = wheel.back().front();
        last_velocity = wheel.back()[1];
        temp_distance = x_coord - last_x;
        // if wheel is moving to the right
        if (temp_distance > 0 && velocity > 0) {
            if (temp_distance < abs(min_distance)){
                min_distance = temp_distance;
                closest_wheel = &*wheel;
            }
        } // if wheel is moving to the left
        else if (temp_distance < 0 && velocity < 0) {
                    
                if (abs(temp_distance) < abs(min_distance)) {
                    min_distance = temp_distance;
                    closest_wheel = &*wheel;
                }
            } 
    } 
}
void compare_velocities_unknown(float velocity) {


}
void compare_velocities_known(float velocity) {


}
// TODO: I should probably check radius of incoming wheel and existing wheel
//       as an added level of security
void add_point(float x_coord, float radius, float timestamp, int frame) {

    std::vector<float> *closest_wheel_unknown = NULL;
    Wheel *closest_wheel_known = NULL;
    float min_distance_unknown = INT_MAX;
    float min_distance_known = INT_MAX;

    // find closest wheel
    find_closest_unknown(x_coord, closest_wheel_unknown, min_distance_unknown);
    find_closest_known(x_coord, closest_wheel_known, min_distance_known);
    
    float min_distance = abs(min_distance_unknown) <= abs(min_distance_known) ? min_distance_unknown : min_distance_known;

    // basically if there are no wheels yet (should be NULL), we make a new wheel
    if (closest_wheel_unknown == closest_wheel_known) {
        std::vector<float> unknown;
        unknown.push_back(x_coord);
        unkown.push_back(radius);
        unknown.push_back(timestamp);
        unknown.push_back(frame);
        unknown_wheels.push_back(unknown); 
        
    }
    else if (min_distance == min_distance_unknown) {   // if unknown has a closer wheel
            
            float velocity = get_velocity (closest_wheel_unknown[0], closest_wheel_unknown[2], x_coord, timestamp);
            Wheel wheel;
            wheel.radius = radius;
            closest_wheel_unknown[1] = velocity;
            wheel.wheel.push_back(closest_wheel_unknown);
            std::vectoe<float> known;
            known.push_back(x_coord);
            known.push_back(velocity);
            known.push_back(timestamp);
            known.push_back(frame);
            
        }
        else {                                              // if the closest is a known wheel

        }


}
void calculate_distance(Wheel& wheel1, Wheel& wheel2

void find_cars(std::vector<Wheel> &c1) {



}


int count_cars(std::vector<std::vector<Wheel>> c1, std::vector<std::vector<Wheel>> c2) {



}
