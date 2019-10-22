#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <unistd.h>
#include "../scripts/get_wheels.hpp"

void print_unknown_wheels(Camera &c) {
   
    std::cout << "**** unknown wheels *****" << std::endl;
    for (auto &wheel : c.get_unknown_wheels()) {

        std::cout << "x coordinate:" << wheel[0] << std::endl;
        std::cout << "radius:" <<  wheel[1] << std::endl;
        std::cout << "timestamp:" << wheel[2] << std::endl;
        std::cout << "frame:" << wheel[3] << std::endl;
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

void print_known_wheels(Camera &c) {

    std::cout << "**** known wheels *****" << std::endl;
    for (auto &wheel : c.get_all_wheels()) {
        std::cout << "wheel id:" << wheel.id << std::endl;
        std::cout << "wheel radius:" << wheel.radius << std::endl;
        for (auto &w : wheel.wheel) {
            std::cout << "\tx coordinate:" << w[0] << std::endl;
            std::cout << "\tvelocity:" <<  w[1] << std::endl;
            std::cout << "\ttimestamp:" << w[2] << std::endl;
            std::cout << "\tframe:" << w[3] << std::endl;
            std::cout << std::endl;
        }
    }
    std::cout << std::endl;
}

void print_cars(Camera &c) {

    std::cout << "**** cars ****" << std::endl;
    for (auto car = c.get_cars().begin(); car != c.get_cars().end(); ++car) {

        auto front = car->frontwheel->wheel.begin();
        auto back = car->backwheel->wheel.begin();
        std::cout << "\t\t\tback wheel\t\t\tfront wheel" << std::endl;
        while (front != car->frontwheel->wheel.end() && back != car->backwheel->wheel.end()) {
            std::cout << "xcoordinate:" << (*back)[0] << "\t\t\t" << (*front)[0] << std::endl;
            std::cout << "velocity:" << (*back)[1] << "\t\t\t" << (*front)[1] << std::endl;
            std::cout << "timestamp:" << (*back)[2] << "\t\t\t" << (*front)[2] << std::endl;
            std::cout << "xcoordinate:" << (*back)[3] << "\t\t\t" << (*front)[3] << std::endl;
            ++front;
            ++back;
        }
        std::cout << std::endl;
        std::cout << std::endl;
    }
}

// if direction: false = left, true = right
void populate_single(Camera &c, bool direction, int& frame) {
    std::srand(std::time(NULL));
    int radius = 20;
    unsigned ms = 100;
    if (direction) {
        for (int xcoord = 1; xcoord < PIXELS_DISTANCE; xcoord += (std::rand() % 19 + 1)) {
            
            std::clock_t timer = std::clock();
            c.add_point(xcoord, radius, timer, frame);
            ++frame;
            usleep(ms);
        }
    }
    else {
        for (int xcoord = PIXELS_DISTANCE-1; xcoord > 0; xcoord -= (std::rand() % 19 + 1)) {
            
            std::clock_t timer = std::clock();
            c.add_point(xcoord, radius, timer, frame);
            ++frame;
            usleep(ms);
        }
        
    }
}
// TODO: right now this only works for 2 cars
void populate_multiple(Camera &c, int num_wheels) {
    std::srand(std::time(NULL));
    unsigned ms = 100;
    int frame = 0;
    std::vector<int> radii(num_wheels);

    // add radius to each wheel
    for (int i = 0; i < radii.size(); ++i) {    
        radii[i] = std::rand() % 15 + 5;
    }
    int xcoord1 = 1;
    int xcoord2 = PIXELS_DISTANCE - 1; 
    bool populate = true; 

    while (populate) {

        populate = false;
        std::clock_t timer = std::clock();
        if (xcoord1 < PIXELS_DISTANCE) {
            c.add_point(xcoord1, radii[0], timer, frame);
            xcoord1 += (std::rand() % radii[0] + 1);
            populate = true;
        }
        if (xcoord2 > 1) {
            c.add_point(xcoord2, radii[1], timer, frame);
            xcoord2 -= (std::rand() % radii[1] + 1);
            populate = true;
        }
        ++frame;
        usleep(ms);
    }
}
// 2 wheels, 1 of them disappears and then reappears later
// left_right : true = disappearing wheel coming from right, vice versa for false
void populate_reappear(Camera &c, int num_wheels, bool left_right) {

    std::srand(std::time(NULL));
    unsigned ms = 100;
    int frame = 0;
    
    std::vector<int> radii(num_wheels);
    for (int i = 0; i < radii.size(); ++i) {
        radii[i] = std::rand() % 15 + 5;
    }

    // disappear wheel coming from left side
    float xdisappear = PIXELS_DISTANCE * .25;
    float xreappear = PIXELS_DISTANCE * .75;
    int xcoord1 = 1;
    int xcoord2 = PIXELS_DISTANCE - 1;

    bool populate = true;
    while (populate) {

        populate = false;
        std::clock_t timer = std::clock();
        if (xcoord1 < PIXELS_DISTANCE) {
            if (xcoord1 < xdisappear || xcoord1 >= xreappear) {
                c.add_point(xcoord1, radii[0], timer, frame);
            }
            xcoord1 += (std::rand() % radii[0] + 1);
            populate = true;
        }
        if (xcoord2 > 1) {
            c.add_point(xcoord2, radii[1], timer, frame);
            xcoord2 -= (std::rand() % radii[1] + 1);
            populate = true;
        }
        ++frame;
        usleep(ms);
    }
}
// directions: true = right, false = left
void single_wheel(int frame, std::vector<bool> &directions) {

    Camera c;
    for (int i = 0; i < directions.size(); ++i) {
        populate_single(c, directions[i], frame); 
    }
    
    print_unknown_wheels(c);
    print_known_wheels(c);
    std::cout << "number of actual cars: " << c.get_cars().size() << std::endl;
    c.send_data_to_server(2);
}

void multiple_wheels(int frame, std::vector<int> &directions) {

    Camera c;
    populate_reappear(c, 2, true);
    print_unknown_wheels(c);
    print_known_wheels(c);
    c.send_data_to_server(2);
    std::cout << "number of actual cars: " << c.get_cars().size() << std::endl;
}


int main() {


    int frame = 0;
    std::vector<bool> directions;

    directions.push_back(false);
    directions.push_back(true);
    directions.push_back(true);
    directions.push_back(false);
    directions.push_back(true);
    directions.push_back(true);

    single_wheel(frame, directions);
    //multiple_wheels();
    return 0;
}
