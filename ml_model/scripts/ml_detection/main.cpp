//
//  main.cpp
//  CarWheelVelocities
//
//  Created by tab on 4/23/18.
//  Copyright © 2018 tab. All rights reserved.
//
// g++ $(pkg-config --cflags --libs opencv4) -std=c++11 -O3 main.cpp TrackerHough.cpp Wheel.cpp ../get_wheels.cpp -o executable

#include <iostream>

#include <opencv2/core/utility.hpp>
#include <opencv2/tracking.hpp>
#include <opencv2/videoio/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

#include <vector>
#include <list>
#include <unordered_map>
#include <utility>

#include "TrackerHough.hpp"
#include "Wheel.hpp"
#include "Constants.h"

using namespace std;
using namespace cv;

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

int main(int argc, const char * argv[]) {

    //open the video file
    // video6x.5spd dimensions: 850 × 480
    VideoCapture reader("input_output_data/video6x.5spd2.mp4");
    int ex = static_cast<int>(reader.get(CAP_PROP_FOURCC));
    int frameCount = reader.get(CAP_PROP_FRAME_COUNT);
    int WIDTH = reader.get(CAP_PROP_FRAME_WIDTH);
    int HEIGHT = reader.get(CAP_PROP_FRAME_HEIGHT);
    int FPS = reader.get(CAP_PROP_FPS);
    //init an VideoWriter to output processed video
    VideoWriter outputVideo("input_output_data/output.mp4", ex, FPS/3, Size(WIDTH,HEIGHT), true);
    // if cannot open the file
    if (!reader.isOpened()) {
        cout << "cannot open video file" << endl;
        return EXIT_FAILURE;
    }
    
    if (!outputVideo.isOpened())
    {
        cout  << "Could not open the output video for write"<< endl;
        return EXIT_FAILURE;
    }
 
    Mat frame;
    
    //    set parameters for tracker
    TrackerHough::Params params;
    params.param1 = HOUGH_CIRCLE_PARA1;
    params.param2 = HOUGH_CIRCLE_PARA2;
    params.minRadius = MIN_WHEEL_R;
    params.maxRadius = MAX_WHEEL_R;
    params.width = WIDTH;
    
    //    create tracker
    Ptr<TrackerHough> tracker = TrackerHough::create(params);
    
    //    use a list to record wheels

    std::srand(std::time(NULL));
    std::clock_t time;
    Camera camera;
//    reader.set(1, 60);
    int count = 0;
    std::vector<std::vector<float>> wheels_cur_image;
    //    process the image frame by frame
    for (;count < frameCount; ++count) 
    {
        //cout<<"frame count "<<count<<endl;
        time = std::clock();

        reader >> frame; // get a new frame from camera
        Mat imageGray, imageBlur, imageThresh;
        Mat imageCrop = frame(Rect(0,frame.rows*.35,frame.cols,frame.rows - frame.rows*.45));
        //    convert to gray
        if(imageCrop.channels() > 1)
        {
            cvtColor( imageCrop, imageGray, CV_BGR2GRAY );
        }
        else
        {
            // if the frame is already black and white (i think)
            imageGray = imageCrop.clone();
        }
        
        //apply Gaussian Blur before Hough Circle detect
        GaussianBlur(imageGray, imageBlur, Size(10*SIGMA-1,10*SIGMA-1), SIGMA, SIGMA);
        imshow("blur image", imageBlur);
        //update tracking wheelList with the blured image in each frame

        threshold(imageBlur, imageThresh, 50, 255, THRESH_BINARY_INV);

        imshow("threshold image", imageThresh); 

        tracker->update(imageThresh, count, time, camera, wheels_cur_image);

        for (auto &iter: wheels_cur_image) {
            float circleX = iter[0];
            float circleY = iter[1]+frame.rows*.35;
            float circleR = iter[2];
            Point center(circleX, circleY);
            Point centerID(circleX, circleY-circleR);
            circle(frame, center, circleR, Scalar(0, 255, 0), 5);
//            putText(frame, "meh", centerID, 1, 10, Scalar(255, 0, 0), 3);

        }
        imshow("Tracking", frame);
        std::ostringstream originalName;
        originalName << "input_output_data/frames/frame_" << count << ".jpg";
        imwrite(originalName.str(), frame);
        outputVideo << frame;
        cv::waitKey(1);
        wheels_cur_image.clear();
        if (count % 100 == 0) {
            camera.clean_data(time);
        }
    }
    camera.send_data_to_server(time);
    print_known_wheels(camera);
    print_unknown_wheels(camera);
    outputVideo.release();
    reader.release();
    return 0;
}
