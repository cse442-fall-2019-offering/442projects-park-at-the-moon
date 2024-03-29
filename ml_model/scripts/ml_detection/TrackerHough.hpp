//
//  HoughTracker.hpp
//  CarWheelVelocities
//
//  Created by tab on 4/26/18.
//  Copyright © 2018 tab. All rights reserved.
//

#ifndef TrackerHough_hpp
#define TrackerHough_hpp

#include <stdio.h>
#include <opencv2/core.hpp>
#include <opencv2/tracking.hpp>

#include "Wheel.hpp"

using namespace cv;
class TrackerHough{
public:
    struct CV_EXPORTS Params
    {
        Params();
        double width;
        double param1 = 100;
        double param2 = 100;
        int minRadius = 0;
        int maxRadius = 0;
    };
    
    /**
     Constructor with param
     @return ptr to HoughTracker
     */
    static Ptr<TrackerHough> create(const TrackerHough::Params &parameters);
    static Ptr<TrackerHough> createDetetor(const TrackerHough::Params &parameters);
    CV_WRAP static Ptr<TrackerHough> create();
    
    CV_WRAP bool init( InputArray image);
    
    /**
     Update wheels data for each frame
     
     @param image input image
     @param wheelList the existing wheel list
     @return true or false */
    CV_WRAP bool update( InputArray image, int frame, std::clock_t time, 
    Camera &camera, std::vector<std::vector<float>> &wheels_cur_image);
    
    virtual ~TrackerHough();
    
protected:
    virtual bool initImpl( const Mat& image) = 0;
    virtual bool updateImpl( const Mat& image, int frame, std::clock_t time, 
    Camera &camera, std::vector<std::vector<float>>& wheels_cur_image) = 0;

    bool isInit;
};

class TrackerHoughImpl: public TrackerHough{
public:
    TrackerHoughImpl(const TrackerHough::Params &parameters = TrackerHough::Params());
    bool initImpl(const Mat& image);
    bool updateImpl(const Mat& image, int frame, std::clock_t time, 
    Camera &camera, std::vector<std::vector<float>>& wheels_cur_image);

    TrackerHough::Params params;
    //candidates for each image detecting
    std::vector<Vec3f> candidates;
    //SURF feature vote vector
    std::vector<int>voteVec;
    
    
private:
    /**
     Use SURF feature detection to vote for each wheel candidate
     
     @param image input Image
     */
    void voteForCircles(const cv::Mat &image);
    
    /**
     check the if the circle if valid or not
     
     @param circle the wheel candidate
     @return true or false
     */
    bool isValidAsWheel(const cv::Vec3f &circle);
    
};

#endif /* HoughTracker_hpp */
