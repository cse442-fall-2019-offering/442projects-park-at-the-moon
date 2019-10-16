//
//  HoughTracker.cpp
//  CarWheelVelocities
//
//  Created by tab on 4/26/18.
//  Copyright © 2018 tab. All rights reserved.
//
// to run:
// g++ $(pkg-config --cflags --libs opencv4) -std=c++11  -O3 mainNew.cpp TrackerHoughNew.cpp WheelNew.cpp -o executableNew
#include <opencv2/xfeatures2d/nonfree.hpp>

#include "TrackerHoughNew.hpp"
#include "ConstantsNew.h"

TrackerHough::~TrackerHough()
{
}
TrackerHough::Params::Params(){}
bool TrackerHough::init( InputArray image, const std::vector<Wheel>& wheelList ){
    if( isInit )
    {
        return false;
    }
    
    if( image.empty() )
        return false;
    
    bool initTracker = initImpl( image.getMat(), wheelList);
    
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
bool TrackerHough::update(cv::InputArray image, std::vector<Wheel> &wheelList, Camera& camera, int frame){
    if( !isInit )
    {
        return false;
    }
    
    if( image.empty() )
        return false;
    
    return updateImpl( image.getMat(), wheelList, camera, frame);
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

bool TrackerHoughImpl::initImpl(const cv::Mat &image, const std::vector<Wheel>& wheelList){
    return true;
}

/**
 The implementation of tracking update for each frame

 @param image input image
 @param wheelList the existing wheel list
 @return true or false
 */
bool TrackerHoughImpl::updateImpl(const cv::Mat &image, std::vector<Wheel>& wheelList, Camera& camera, int frame){
    HoughCircles(image, candidates, CV_HOUGH_GRADIENT, 1, params.width/3, params.param1, params.param2, params.minRadius, params.maxRadius);
    std::vector<Wheel>::iterator iter;
    voteForCircles(image);
    for (iter = wheelList.begin(); iter!=wheelList.end(); ++iter) {
        iter->isTracked = false;
    }
    int cnt=0;
    // if enough circles were detected in the points of interest (surf)
    // then we update
    for (auto circle : candidates) {
        if (voteVec[cnt]>15) {
            if (!updateNewWheel(circle, wheelList, camera, frame)) {
                updateTracking(circle, wheelList);
            }
        }
        cnt++;
    }
    return true;
}

/**
 Check is the circle should be the new track of the existing wheel

 @param circle the wheel candidate
 @param wheelList the existing wheel list
 @return true or false
 */
bool TrackerHoughImpl::updateTracking(const cv::Vec3f &circle, std::vector<Wheel> &wheelList ){
    if (isValidAsWheel(circle)) {
        return true;
    }
    return false;
}
/*
void updateCamera(Camera& camera, std::vector<Wheel>& WheelList, Wheel& newWheel){
    // if no cars or wheels yet detected
    if (camera.cars.empty()){
        if (camera.partialCars.empty()){
            Car car;
            car.front = &newWheel;
            camera.partialCars.push_back(&car);
        }
        else
        {
            
        }
                    
    }
                

}
*/
//bool insertWheel(const cv::Vec3f &circle
/*
 Check if the circle should be a new wheel

 @param circle the wheel candidate
 @param wheelList the existing wheel list
 @return true or false
 */
// this is where we create a car object
bool TrackerHoughImpl::updateNewWheel(const cv::Vec3f &circle, std::vector<Wheel> &wheelList, Camera& camera, int frame){
    if (isValidAsWheel(circle)) {

        Wheel newWheel(circle, frame);
        
        if (camera.cars.empty()) {
            if (circle[0] <= camera.splitRegion) {
                Car newCar(newWheel, int(newWheel.id/2), 0.0, 1);
                camera.partialCars.push_back(newCar);
            }
            else {
                Car newCar(newWheel, int(newWheel.id/2), 0.0, 2);
                camera.partialCars.push_back(newCar);
            }
            camera.xPoints[frame].push_back(circle[0]);        
        }
        
        return true;
    }
    return false;
}

/**
 check if the circle if valid or not

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
        if (PRINTFRAMES) imshow("surf vote", kpImg);
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
