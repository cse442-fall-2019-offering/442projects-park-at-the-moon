#include "get_wheels.hpp"
#include <set>

#define XCOORDINATE 0
#define VELOCITY 1
#define TIMESTAMP 2
#define FRAME 3

int WheelPath::total_id = 0;
// TODO: every 10 seconds or so, I should send the data to the server, and then clean vectors.
// By clean, I mean look for wheels that have been in the dataset for more than 10 seconds or so
// and remove them. 
// TODO: should the velocity be between the last and current point, or from the start and current point?
// for now I'll do from the starting xpoint
float  Camera::get_velocity (float start_x, float start_time, float last_x, float last_time) {
    float distance = last_x - start_x;
    float time = last_time - start_time;
     return time == 0.0 ? 0.0 : distance / time;
}

void  Camera::find_closest_unknown(float x_coord, int &index, float &min_distance, float radius) {

    float temp_distance;
    float last_x;
    for (auto iter = unknown_wheels.begin(); iter != unknown_wheels.end(); ++iter) {
        // get the xCoord of the last added point
        last_x = (*iter)[XCOORDINATE];
        temp_distance = x_coord - last_x;
        // if moving to the right
        if (temp_distance >= 0 && temp_distance < min_distance && temp_distance <= radius){
            min_distance = temp_distance;
            index = std::distance(unknown_wheels.begin(), iter);
        } // if wheel is moving to the left
        else if (temp_distance < 0 && abs(temp_distance) < min_distance && abs(temp_distance) <= radius) {
            min_distance = abs(temp_distance);
            index = std::distance(unknown_wheels.begin(), iter);
        }
    }
}

void  Camera::find_closest_known(float x_coord,int &index, float &min_distance, float radius) {

    float temp_distance;
    float last_x;
    float last_velocity;
    for (auto iter = all_wheels.begin(); iter != all_wheels.end(); ++iter) {
        // get the xCoord of the last added point
        last_x = iter->wheel.back().front();
        last_velocity = iter->wheel.back()[VELOCITY];
        temp_distance = x_coord - last_x;
        // if wheel is moving to the right
        if (temp_distance > 0 && last_velocity > 0 && temp_distance <= radius) {
            if (temp_distance < abs(min_distance)){
                min_distance = temp_distance;
                index = std::distance(all_wheels.begin(), iter);
            }
        } // if wheel is moving to the left
        else if (temp_distance < 0 && last_velocity < 0 && abs(temp_distance) <= radius) {
                
                if (abs(temp_distance) < min_distance) {
                    min_distance = abs(temp_distance);
                    index = std::distance(all_wheels.begin(), iter);
                }
            } 
    } 
}

// getting velocity by checking first x coordinate with current x coordinate
void  Camera::compare_velocity(float velocity, int &index) {
    int min_vel_diff = INT_MAX;
    int cur_vel_diff;

    for (auto iter = all_wheels.begin(); iter != all_wheels.end(); ++iter) {
        float existing_velocity = iter->wheel.front()[VELOCITY];
        if ((existing_velocity > 0 && velocity > 0) ||
            (existing_velocity < 0 && velocity < 0)) {
            cur_vel_diff = abs(existing_velocity - velocity);
            if ((cur_vel_diff < VELOCITY_ERROR) && (cur_vel_diff < min_vel_diff)) {
                min_vel_diff = cur_vel_diff;
                index = std::distance(all_wheels.begin(), iter);
            }
        }
    }
}
// TODO: I should probably check radius of incoming wheel and existing wheel
//       as an added level of security
void Camera::add_point(float x_coord, float radius, float timestamp, int frame) {

    int index_unknown = -1;
    int index_known = -1;
    float min_distance_unknown = INT_MAX;
    float min_distance_known = INT_MAX;

    // find closest wheel
    find_closest_unknown(x_coord, index_unknown, min_distance_unknown, radius);
    find_closest_known(x_coord, index_known, min_distance_known, radius);
    //std::cout << "unknown min distance: " << min_distance_unknown << std::endl;
    //std::cout << "known min distance: " << min_distance_unknown << std::endl;
    float min_distance = min_distance_unknown <= min_distance_known ? min_distance_unknown : min_distance_known;

    // basically if there are no wheels yet (should be NULL), we make a new wheel
    // TODO: kind of ignoring the fact that I should be comparing by radius
    // this wheel is the first of its kind
    if (index_unknown == -1 && index_known == -1) {
        //std::cout << "new unknown wheel" << std::endl;
        std::vector<float> unknown;
        unknown.push_back(x_coord);
        unknown.push_back(radius);
        unknown.push_back(timestamp);
        unknown.push_back(frame);
        unknown_wheels.push_back(unknown); 
        
    }
    else if (min_distance == min_distance_unknown) {   // if unknown has a closer wheel
            //std::cout << "adding to existing wheel" << std::endl;
            float x = unknown_wheels[index_unknown][XCOORDINATE];
            float old_time = unknown_wheels[index_unknown][TIMESTAMP];
            float velocity = get_velocity (x, old_time, x_coord, timestamp);
            WheelPath wheel(radius);
            unknown_wheels[index_unknown][VELOCITY] = velocity;
            wheel.wheel.push_back(unknown_wheels[index_unknown]);
            std::vector<float> known;
            known.push_back(x_coord);
            known.push_back(velocity);
            known.push_back(timestamp);
            known.push_back(frame);
            wheel.wheel.push_back(known);

            // now we have to check if the velocity is the same in known wheels (then we add it) 
            int index_vel = -1;
            compare_velocity(velocity, index_vel);
            // found pair of points in existing wheel need to add new points to it
            if (index_vel != -1) {
                // add previous 2 unknown wheels to a timeframe of existing wheels
                all_wheels[index_vel].wheel.insert(all_wheels[index_vel].wheel.end(), wheel.wheel.begin(), wheel.wheel.end());
                // need to remove the existing wheel in unknown_wheel
                
            }
            else {
                // a new wheel was created
                all_wheels.push_back(wheel);
            }
            // in any case, we have 2 points, which is enough to create a new wheel
            // so we will always remove it from unknown_wheels
            unknown_wheels.erase(unknown_wheels.begin() + index_unknown);
        }
        else {                                              // if the closest is a known wheel
            //std::cout << "adding wheel to a known wheel" << std::endl;
            float velocity = get_velocity (all_wheels[index_known].wheel.back()[XCOORDINATE], all_wheels[index_known].wheel.back()[TIMESTAMP], x_coord, timestamp);
            std::vector<float> wheel;
            wheel.push_back(x_coord);
            wheel.push_back(velocity);
            wheel.push_back(timestamp);
            wheel.push_back(frame);
            all_wheels[index_known].wheel.push_back(wheel);
        }
}
std::vector<WheelPath> Camera::get_all_wheels() {
    return all_wheels;
}
std::vector<std::vector<float>> Camera::get_unknown_wheels() {
    return unknown_wheels;
}
// we need to check if either two things are true:
//  1) has the wheel been sitting in all_wheels for DEAD_INTERVAL?
//  2) did the wheel reach both sides of the margin?
// for unknown_wheels, we'll just check if they've been in there
// for more than DEAD_INTERVAL
// TODO: I am checking the current time with the last known time,
//      but what if somehow a new time keeps getting added?
//      but if I check the oldest time, that means that the entire
//      path of the wheel better be from the same wheel
//      otherwise a wheel could go missing
void Camera::clean_data(double cur_time) {
   
    std::vector<int> remove_idx_known;
    std::vector<int> remove_idx_unknown;
    for (int i = 0; i < all_wheels.size(); ++i) {

        // checking conditions for removal
        if ((all_wheels[i].wheel.front()[XCOORDINATE] <= COMPLETE_MARGIN &&
            all_wheels[i].wheel.back()[XCOORDINATE] >= PIXELS_DISTANCE - COMPLETE_MARGIN) ||
            (all_wheels[i].wheel.front()[XCOORDINATE] >= PIXELS_DISTANCE - COMPLETE_MARGIN &&
            all_wheels[i].wheel.back()[XCOORDINATE] <= COMPLETE_MARGIN) ||
            cur_time - all_wheels[i].wheel.back()[TIMESTAMP] > DEAD_INTERVAL)
                remove_idx_known.push_back(i);
    }
    for (auto &idx : remove_idx_known) {
        all_wheels.erase(all_wheels.begin() + idx);
    }
    for (int i = 0; i < unknown_wheels.size(); ++i) {

        if (cur_time - unknown_wheels[i][TIMESTAMP]) {
            remove_idx_unknown.push_back(i);
        }
    }
    for (auto &idx : remove_idx_unknown) {
        all_wheels.erase(all_wheels.begin() + idx);
    }
}
float Camera::get_average_velocity(std::vector<std::vector<float>> &wheelpath) {

    float avg_velocity = 0.0;

    
    for (auto &w : wheelpath) {
        avg_velocity += w[VELOCITY];
    }
    
    return avg_velocity / wheelpath.size();
}


// TODO: this currently only checks wheels with positive velocity
// first check if average is positive if so then
// get average of each wheel and compare
// if the difference is < VELOCITY_ERROR
// then both wheels belong to the same car
int Camera::car_count() {

    int count = 0;
    float avg_vel1;
    float avg_vel2;
    std::set<int> counted_wheels;

    for (int i = 0; i < all_wheels.size() - 1; ++i) {
        // check first wheel's velocity in wheel path
        if (all_wheels[i].wheel.front()[VELOCITY] < 0 ||
            counted_wheels.find(i) != counted_wheels.end()) continue;

        avg_vel1 = get_average_velocity(all_wheels[i].wheel);
    
        // check if next wheelpath has same velocity
        for (int p = i + 1; p < all_wheels.size(); ++p) {

            if (all_wheels[p].wheel.front()[VELOCITY] < 0 ||
                counted_wheels.find(p) != counted_wheels.end()) continue;

            avg_vel2 = get_average_velocity(all_wheels[p].wheel);
            // if both wheels have the same velocity
            if (abs(avg_vel1 - avg_vel2) <= VELOCITY_ERROR) {
                ++count;
                counted_wheels.insert(p);
            }
        }
    }
    
    return count;
}
// need to send all_wheels to server
void Camera::send_data_to_server(double cur_time) {
    // get count
    
    // send to server
    
    // then clean data
    clean_data(cur_time);
}
//void calculate_distance(WheelPath& wheel1, Wheel& wheel2

//void find_cars(std::vector<WheelPath> &c1) {
    

//int count_cars(std::vector<std::vector<WheelPath>> c1, std::vector<std::vector<Wheel>> c2) {
//}
/*
int main() {
    
    Camera c;
    float xcoord = 2.33;
    float radius = 2.5;
    float time = 4.55;
    int frame = 0;
    c.add_point(xcoord, radius, time, frame); 
    return 0;
}
*/
