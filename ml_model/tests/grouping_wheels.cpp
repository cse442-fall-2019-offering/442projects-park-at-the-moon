#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include "../scripts/count_cars.hpp"

void print_unknown_wheels(Cars &c) {
   
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

void print_known_wheels(Cars &c) {

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
// if direction: false = left, true = right
void populate_path(Cars &c, std::vector<std::vector<float>> &wheel_track, bool direction) {

    std::srand(std::time(NULL));
    int frame = 0;
    int radius = 20;
    if (direction) {
        for (int xcoord = 1; xcoord < PIXELS_DISTANCE; xcoord += (std::rand() % 19 + 1)) {
            
            std::clock_t timer = std::clock();
            c.add_point(xcoord, radius, timer, frame);
            ++frame;
        }
    }
}


void single_car_right(std::vector<std::vector<float>> &wheel_track) {

    Cars c;
    
    populate_path(c, wheel_track, true); 
    
    print_unknown_wheels(c);
    print_known_wheels(c);

}


int main() {

    std::vector<std::vector<float>> wheel_track;


    single_car_right(wheel_track);
    return 0;
}
