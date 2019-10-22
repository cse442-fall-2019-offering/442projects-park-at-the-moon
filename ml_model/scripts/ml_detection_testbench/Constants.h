//
//  Constants.h
//  CarWheelVelocities
//
//  Created by tab on 4/26/18.
//  Copyright © 2018 tab. All rights reserved.
//

#ifndef Constants_h
#define Constants_h

// Sigma for GaussianBlur
static const int SIGMA = 1;
// track margin
static const float MARGIN_TRACKING = 1;
// image draw margin
static const float MARGIN_DIST = 1;
// the minimum distance between two wheels
static const float MIN_DIST_WHEELS = 10;
// the minimum and maximum offset in x for tracking
static const float MIN_WHEEL_X_OFFSET_TRACKING = 10;
static const float MAX_WHEEL_X_OFFSET_TRACKING = 500;
// the maximum offset in y for both detecting and tracking
static const float MAX_WHEEL_Y_OFFSET = 30;
// the maximum difference in radius for both detecting and tracking
static const float MAX_WHEEL_R_DIFF = 30;

static const float MIN_WHEEL_R = 1;
static const float MAX_WHEEL_R = 80;
// parameters for HoughCircles func
static const double HOUGH_CIRCLE_PARA1 = 100;
static const double HOUGH_CIRCLE_PARA2 = 30;

// SURF feature vote threshold
static const double SURF_VOTE_THRESHOLD = 15;

#endif /* Constants_h */
