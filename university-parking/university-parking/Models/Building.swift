//
//  Building.swift
//  university-parking
//
//  Created by Arthur De Araujo on 10/20/19.
//  Copyright © 2019 Arthur De Araujo. All rights reserved.
//

import UIKit
import GoogleMaps
import SwiftyJSON

class Building: NSObject {
    
    var name:String = ""
    var id:Int = -1
    
    var centerCoord:CLLocationCoordinate2D? = nil
    var boundaryCoords:[CLLocationCoordinate2D] = []
    var entranceCoords:[CLLocationCoordinate2D] = []

    init(json: JSON) {
        for i in 0..<json["boundary_lat"].count {
            let latitude = json["boundary_lat"][i]
            let longitude = json["boundary_lon"][i]
                                
            boundaryCoords.append(CLLocationCoordinate2D.init(latitude: latitude.doubleValue, longitude: longitude.doubleValue))
        }
                
        for i in 0..<json["entrance_lat"].count {
            let latitude = json["entrance_lat"][i]
            let longitude = json["entrance_lon"][i]
                                
            entranceCoords.append(CLLocationCoordinate2D.init(latitude: latitude.doubleValue, longitude: longitude.doubleValue))
        }

        centerCoord = CLLocationCoordinate2D.init(latitude: json["center"][0].doubleValue, longitude: json["center"][1].doubleValue)

        id = json["id"].intValue
        name = json["name"].stringValue
    }
}
