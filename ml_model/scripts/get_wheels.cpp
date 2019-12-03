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
// this should try to find an existing wheel path that happened before in both
// space and time, and add the new wheelpath to that existing wheelpath
bool Camera::combine_wheelpaths(WheelPath& wheelpath) {

    // look for the last xcoordinate in iter that is 
    // less than the first xcoordinate in wheelpath
    for (auto iter = all_wheels.begin(); iter != all_wheels.end(); ++iter) {
         
        if ((iter->wheel.back()[XCOORDINATE] < wheelpath.wheel.front()[XCOORDINATE] && 
             iter->wheel.back()[VELOCITY] > 0) || 
            (iter->wheel.back()[XCOORDINATE] > wheelpath.wheel.front()[XCOORDINATE] &&
            iter->wheel.back()[VELOCITY] < 0)) {

            // should I update the velocity in any way?
            for (auto npts = wheelpath.wheel.begin(); npts != wheelpath.wheel.end(); ++npts) {
                iter->wheel.push_back(*npts);
                return true;
            }
        }
    }

    return false;
}

// given an unknown wheelpoint, this function attempts to add it to another unknown
// wheelpoint, converting it into a wheelpath
// TODO: we can also specify an in between stage where we need
// a certain number of wheels to a wheelpath before it becomes a
// true known wheelpath
bool Camera::find_existing_wheelpoint(float x_coord, float time, int frame) {

    for (auto iter = unknown_wheels.begin(); iter != unknown_wheels.end();++iter) {
        // move on if the time difference in points is too great
        if (abs(time - (*iter)[TIMESTAMP]) > TIME_ERROR) continue;
        // if the distance is too great move on
        if (abs((*iter)[XCOORDINATE] - x_coord) > (*iter)[1]) continue;
        
        std::vector<float> known;
        known.push_back(x_coord);
        float velocity = get_velocity((*iter)[XCOORDINATE], (*iter)[TIMESTAMP], x_coord, time);
        known.push_back(velocity);
        known.push_back(time);
        known.push_back(frame);

        WheelPath wheelpath((*iter)[1]);
        (*iter)[VELOCITY] = velocity;
        // TODO: this should copy, but does it?
        wheelpath.wheel.push_back(*iter);
        wheelpath.wheel.push_back(known);
        // we need to now determine if we should add this to
        // an existing wheelpath
        // this function will look to add wheelpath to an existing wheel path
        if (combine_wheelpaths(wheelpath)) return true;
        // if it couldn't find an existing wheel path, then just add it as a new set to all_wheels
        all_wheels.push_back(wheelpath);
        // need to remove point now from unknown_wheels
        unknown_wheels.erase(iter);
        return true; 
    }
    return false;
}

bool  Camera::find_existing_wheelpath(float x_coord, float time, int frame) {

    for (auto iter = all_wheels.begin(); iter != all_wheels.end(); ++iter) {
        // skip if the point has appeared before the last known point of the wheel
        if ((iter->wheel.back()[VELOCITY] > 0 && x_coord < iter->wheel.back()[XCOORDINATE]) ||
            (iter->wheel.back()[VELOCITY] < 0 && x_coord > iter->wheel.back()[XCOORDINATE])) continue;

        // if the frame is much later than the last known frame of the known wheel path
        // TODO: might not need to include this as long as making sure every piece of wheelpath is getting 
        // added to another wheelpath of the same wheel
        if (abs(time - iter->wheel.back()[TIMESTAMP]) > TIME_ERROR) continue;
        // if the wheel is far away from the previous known xcoordinate of the wheel
        if (abs(iter->wheel.back()[XCOORDINATE] - x_coord) > iter->radius) continue;
        // get the xCoord of the last added point
        float first_x = iter->wheel.front()[XCOORDINATE];
        float first_timestamp = iter->wheel.front()[VELOCITY];

        std::vector<float> known;
        known.push_back(x_coord);
        float velocity = get_velocity(first_x, first_timestamp, x_coord, time);
        known.push_back(velocity);
        known.push_back(time);
        known.push_back(frame);
        // TODO: make sure this is actually storing the new wheelpoint (i forget how iterators work)
        iter->wheel.push_back(known);
        return true;
    } 
    return false;
}

void Camera::add_unknown_point(float x_coord, float radius, float timestamp, int frame) {

    std::vector<float> unknown;
    unknown.push_back(x_coord);
    unknown.push_back(radius);
    unknown.push_back(timestamp);
    unknown.push_back(frame);
    
    unknown_wheels.push_back(unknown);
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

    // either adds point to an existing wheel path, creates a wheel path with some other point
    // and either adds that new wheel path to an existing wheel path or just keeps it as a new wheel path,
    // or just adds the point as an unknown
    if (!find_existing_wheelpath(x_coord, timestamp, frame) && !find_existing_wheelpoint(x_coord, timestamp, frame)) {

        add_unknown_point(x_coord, radius, timestamp, frame);
    }
/*
    // find closest wheel
    find_closest_unknown(x_coord, index_unknown, min_distance_unknown, radius, frame);
    find_closest_known(x_coord, index_known, min_distance_known, radius, frame);
    //std::cout << "unknown min distance: " << min_distance_unknown << std::endl;
    //std::cout << "known min distance: " << min_distance_unknown << std::endl;
    float min_distance = min_distance_unknown <= min_distance_known ? min_distance_unknown : min_distance_known;

    // basically if there are no wheels yet (should be NULL), we make a new wheel
    // this wheel is the first of its kind
    // TODO: kind of ignoring the fact that I should be comparing by radius
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
            all_wheels.push_back(wheel);
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
            //unknown_wheels.erase(unknown_wheels.begin() + index_unknown);
            
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
*/
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
    for (int idx = remove_idx_known.size() - 1; idx >= 0; --idx) {
        all_wheels.erase(all_wheels.begin() + idx);
    }
    for (int i = 0; i < unknown_wheels.size(); ++i) {

        if (cur_time - unknown_wheels[i][TIMESTAMP]) {
            remove_idx_unknown.push_back(i);
        }
    }
    
    for (int idx = remove_idx_unknown.size() - 1; idx >= 0; --idx) {
        unknown_wheels.erase(unknown_wheels.begin() + idx);
    }
}
float Camera::get_average_velocity(std::vector<std::vector<float>> &wheelpath) {

    float avg_velocity = 0.0;

    
    for (auto &w : wheelpath) {
        avg_velocity += w[VELOCITY];
    }
    
    return avg_velocity / wheelpath.size();
}

// get average of each wheel and compare
// if the difference is < VELOCITY_ERROR
// then both wheels belong to the same car
void Camera::car_count() {

    int moving_right = 0;
    int moving_left = 0;
    float avg_vel1;
    float avg_vel2;
    std::set<int> counted_wheels;

    for (int i = 0; i < all_wheels.size() - 1; ++i) {
        // check first wheel's velocity in wheel path
        if (counted_wheels.find(i) != counted_wheels.end()) continue;

        avg_vel1 = get_average_velocity(all_wheels[i].wheel);
    
        // check if next wheelpath has same velocity
        for (int p = i + 1; p < all_wheels.size(); ++p) {

            if (counted_wheels.find(p) != counted_wheels.end()) continue;
            
            avg_vel2 = get_average_velocity(all_wheels[p].wheel);
            // if one velocity is positive and another is negative, then
            // they can't belong to the same car
            if (avg_vel1 * avg_vel2 < 0)
                continue;
                
            // if both wheelpaths have the same velocity
            if (abs(avg_vel1 - avg_vel2) <= VELOCITY_ERROR) {
                if (avg_vel1 > 0)
                    ++moving_right;
                else
                    ++moving_left;
                counted_wheels.insert(p);
                break;
            }
        }
    }
    std::cout << "cars moving right: " << moving_right << std::endl; 
    std::cout << "cars moving left: " << moving_left << std::endl; 
    Camera::count =  moving_right + moving_left;
}
void Camera::find_cars() {




}
// need to send all_wheels to server
void Camera::send_data_to_server(double cur_time) {
    // get count
    car_count();    
    // send count to server
//    std::cout << "car count: " << count << std::endl; 
    // then clean data
    clean_data(cur_time);
}

