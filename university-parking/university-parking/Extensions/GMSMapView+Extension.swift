//
//  GMSMapView+Extension.swift
//  university-parking
//
//  Created by Arthur De Araujo on 10/20/19.
//  Copyright © 2019 Arthur De Araujo. All rights reserved.
//

import UIKit
import GoogleMaps

extension GMSMapView {
    func mapStyle(withFilename name: String, andType type: String) {
        do {
            if let styleURL = Bundle.main.url(forResource: name, withExtension: type) {
                self.mapStyle = try GMSMapStyle(contentsOfFileURL: styleURL)
            } else {
                NSLog("Unable to find style.json")
            }
        } catch {
            NSLog("One or more of the map styles failed to load. \(error)")
        }
    }
}
