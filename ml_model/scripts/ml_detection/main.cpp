//
//  main.cpp
//  CarWheelVelocities
//
//  Created by tab on 4/23/18.
//  Copyright © 2018 tab. All rights reserved.
//

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

void print_wheelList(vector<Wheel> &wheelList)
{
    for (auto &wheel : wheelList)
    {
        cout << "id: " << wheel.id << endl;
        cout << "circle x: " << wheel.circle[0] << endl;
        cout << "circle y: " << wheel.circle[1] << endl;
        cout << "circle radius: " << wheel.circle[2] << endl;
        for (auto &x : wheel.xPosVec)
        {
           cout << "xPosvec: " << x << endl;
        }
        cout << "isTracked: " << wheel.isTracked << endl;
        cout << "index: " << wheel.index << endl;
        cout << endl;
    }
    cout << endl;
}

int main(int argc, const char * argv[]) {
    // insert code here...
    //open the video file
    // video6x.5spd dimensions: 850 × 480
    VideoCapture reader("test_data/video_reallyslow.mp4");
    int ex = static_cast<int>(reader.get(CAP_PROP_FOURCC));
    int frameCount = reader.get(CAP_PROP_FRAME_COUNT);
    int WIDTH = reader.get(CAP_PROP_FRAME_WIDTH);
    int HEIGHT = reader.get(CAP_PROP_FRAME_HEIGHT);
    int FPS = reader.get(CAP_PROP_FPS);
    //init an VideoWriter to output processed video
    VideoWriter outputVideo("test_data/output.mp4", ex, FPS/3, Size(WIDTH,HEIGHT), true);
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
    
//    Camera camera;
//    camera.carCount = 0;
 
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
    std::vector<Wheel> wheelList = {};
    
//    reader.set(1, 60);
    int count = 0;
    //    process the image frame by frame
    for (;count < frameCount; ++count) 
    {
        cout<<"frame count "<<count<<endl;
        reader >> frame; // get a new frame from camera
        Mat imageGray, imageBlur, imageThresh;
        //cout << "rows:" << frame.rows << endl;
        // args: x, y, width, height
        //cout << frame.rows*.25 << endl;
        //cout << frame.cols << endl;
        //if (count == 20) break;
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
        //threshold(imageBlur, imageBlur, 50, 255, THRESH_BINARY);
        imshow("threshold image", imageThresh); 

        tracker->update(imageThresh, wheelList);
        std::vector<Wheel>::iterator iter = wheelList.begin();
        for (iter = wheelList.begin(); iter!=wheelList.end();) {
            float circleX = iter->circle[0];
            // add # of rows
            float circleY = iter->circle[1]+frame.rows*.35;
            float circleR = iter->circle[2];
            Point center(circleX, circleY);
            Point centerID(circleX, circleY-circleR);
            circle(frame, center, circleR, Scalar(0, 255, 0), 5);
            //putText(frame, to_string(iter->index), centerID, 1, 10, Scalar(255, 0, 0),3);
            //if the velocity has multiple records, show the average speed
            if (iter->xPosVec.size() > 1) {
                std::ostringstream speedText;
                float beginX = iter->xPosVec[0];
                float dis = circleX-beginX;
                //cout << dis << endl;
                float speed = dis/iter->xPosVec.size();
                speedText<<speed;
                Point textOrg(circleX, circleY+circleR);
                putText(frame, speedText.str(), textOrg, 1, 2, Scalar(0, 255, 0),3);
            }
            //if the wheel reach the edge of the image, remove it from the tracking list
            if (circleX>WIDTH-MARGIN_DIST) {
                iter = wheelList.erase(iter);
            }else{
                ++iter;
            }
        }
        imshow("Tracking", frame);
        std::ostringstream originalName;
        originalName << "test_data/frames/frame_" << count << ".jpg";
        imwrite(originalName.str(), frame);
        outputVideo << frame;
        cv::waitKey(1);
    }
    outputVideo.release();
    reader.release();
    return 0;
}
