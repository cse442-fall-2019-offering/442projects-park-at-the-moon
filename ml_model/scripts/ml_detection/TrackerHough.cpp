//
//  HoughTracker.cpp
//  CarWheelVelocities
//
//  Created by tab on 4/26/18.
//  Copyright © 2018 tab. All rights reserved.
//

#include <opencv2/xfeatures2d/nonfree.hpp>

#include "TrackerHough.hpp"
#include "Constants.h"

TrackerHough::~TrackerHough()
{
}
TrackerHough::Params::Params(){}
bool TrackerHough::init( InputArray image){
    if( isInit )
    {
        return false;
    }
    
    if( image.empty() )
        return false;
    
    bool initTracker = initImpl( image.getMat());
    
    if( initTracker )
    {
        isInit = true;
    }
    
    return initTracker;
}


/**
 Update wheels data for each frame

 @param image input image
 @param wheelList the existing wheel list
 @return true or false */
bool TrackerHough::update(cv::InputArray image, int frame, std::clock_t time, 
    Camera &camera, std::vector<std::vector<float>>& wheels_cur_image) {

    if( !isInit )
    {
        return false;
    }
    
    if( image.empty() )
        return false;
    
    return updateImpl( image.getMat(), frame, time, camera, wheels_cur_image);
}

Ptr<TrackerHough> TrackerHough::create(const TrackerHough::Params &parameters)
{
    return Ptr<TrackerHough>(new TrackerHoughImpl(parameters));
}
Ptr<TrackerHough> TrackerHough::create()
{
    return Ptr<TrackerHough>(new TrackerHoughImpl());
}

TrackerHoughImpl::TrackerHoughImpl(const TrackerHough::Params &parameters): params( parameters ){
    isInit = true;
}

bool TrackerHoughImpl::initImpl(const cv::Mat &image){
    return true;
}

bool TrackerHoughImpl::updateImpl(const cv::Mat &image, int frame, std::clock_t time, 
    Camera &c, std::vector<std::vector<float>>& wheels_cur_image) {

    HoughCircles(image, candidates, CV_HOUGH_GRADIENT, 1, params.width/3, params.param1, params.param2, params.minRadius, params.maxRadius);
    voteForCircles(image);
    int cnt=0;
    bool voting = false;
    // if enough circles were detected in the points of interest (surf)
    // then we update
    for (auto &circle : candidates) {
        std::vector<float> point(3);
        if (voting) {
            if (voteVec[cnt]>15) {
                c.add_point(circle[0], circle[2], time, frame); 
                point[0] = circle[0];
                point[1] = circle[1];
                point[2] = circle[2];
                wheels_cur_image.push_back(point);
            }
        }
        else {
            c.add_point(circle[0], circle[2], time, frame); 
            point[0] = circle[0];
            point[1] = circle[1];
            point[2] = circle[2];
            wheels_cur_image.push_back(point);
        }
        cnt++;
    }
    return true;
}






/**
 check the if the circle if valid or not

 @param circle the wheel candidate
 @return true or false
 */
bool TrackerHoughImpl::isValidAsWheel(const cv::Vec3f &circle){
    float circleX = circle[0];
    float circleR = circle[2];
    if (circleR>MIN_WHEEL_R && circleR<MAX_WHEEL_R &&
        circleX>MARGIN_TRACKING && circleX<params.width-MARGIN_TRACKING
        ) {
        return true;
    }
    return false;
}


/**
 Use SURF feature detection to vote for each wheel candidate

 @param image input Image
 */
void TrackerHoughImpl::voteForCircles(const cv::Mat &image){
    std::vector<cv::KeyPoint>keyPts;
    if (candidates.size()>0) {
        Ptr<xfeatures2d::SURF> surf = cv::xfeatures2d::SURF::create();
        surf->setHessianThreshold(1000);
        surf->detect(image, keyPts);

        Mat kpImg; 
        drawKeypoints(image, keyPts, kpImg, Scalar(255,0,0),DrawMatchesFlags::DRAW_RICH_KEYPOINTS);
        imshow("surf vote", kpImg);
    }
    voteVec = std::vector<int>(candidates.size(),0);
    int cnt = 0;
    // may try to change this so that a vote would count if it is in a rectangle
    // containing both front and back wheels possibly
    for (auto circle : candidates ) {
        
        float circleX = circle[0];
        float circleY = circle[1];
        float circleR = circle[2];
        Rect rect(circleX-circleR/2, circleY-circleR/2, circleR*2, circleR*2);
        for (auto kpt :keyPts) {
            if (rect.contains(kpt.pt)){
                voteVec[cnt]+=1;
	         }
        }
        cnt++;
    }
}
