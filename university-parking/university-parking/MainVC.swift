//
//  MainVC.swift
//  university-parking
//
//  Created by Arthur De Araujo on 9/15/19.
//  Copyright © 2019 Arthur De Araujo. All rights reserved.
//

import UIKit
import GoogleMaps
import Alamofire
import SwiftyJSON

let kMapStyle =
"""
[{"elementType":"geometry","stylers":[{"color":"#212121"}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"elementType":"labels.text.fill","stylers":[{"color":"#757575"}]},{"elementType":"labels.text.stroke","stylers":[{"color":"#212121"}]},{"featureType":"administrative","elementType":"geometry","stylers":[{"color":"#757575"}]},{"featureType":"administrative.country","elementType":"labels.text.fill","stylers":[{"color":"#9e9e9e"}]},{"featureType":"administrative.land_parcel","stylers":[{"visibility":"off"}]},{"featureType":"administrative.locality","elementType":"labels.text.fill","stylers":[{"color":"#bdbdbd"}]},{"featureType":"poi","elementType":"labels.text.fill","stylers":[{"color":"#757575"}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#181818"}]},{"featureType":"poi.park","elementType":"labels.text.fill","stylers":[{"color":"#616161"}]},{"featureType":"poi.park","elementType":"labels.text.stroke","stylers":[{"color":"#1b1b1b"}]},{"featureType":"road","elementType":"geometry.fill","stylers":[{"color":"#2c2c2c"}]},{"featureType":"road","elementType":"labels.text.fill","stylers":[{"color":"#8a8a8a"}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#373737"}]},{"featureType":"road.highway","elementType":"geometry","stylers":[{"color":"#3c3c3c"}]},{"featureType":"road.highway.controlled_access","elementType":"geometry","stylers":[{"color":"#4e4e4e"}]},{"featureType":"road.local","elementType":"labels.text.fill","stylers":[{"color":"#616161"}]},{"featureType":"transit","elementType":"labels.text.fill","stylers":[{"color":"#757575"}]},{"featureType":"water","elementType":"geometry","stylers":[{"color":"#000000"}]},{"featureType":"water","elementType":"labels.text.fill","stylers":[{"color":"#3d3d3d"}]}]
"""

protocol DrawerActionDelegate {
    func didSelectParkingLot(parkingLotID: Int)
}

class MainVC: UIViewController, DrawerActionDelegate {

    @IBOutlet var mapView: GMSMapView!
    
    var buildings:[Building] = []
    var parkingLots:[ParkingLot] = []
    
    var drawerDataSourceDelegate: DrawerDataSourceDelegate!

    // MARK: - UIViewController
    
    override func viewDidLoad() {
        super.viewDidLoad()
                        
        setupMapAppearance()

        retreiveBuildingParkingLotData() {
            self.addParkingLotOverlays()
            self.addBuildingOverlays()
        }
    }

    // MARK: - MainVC
    
    func setupMapAppearance() {
        mapView.camera = GMSCameraPosition.camera(withLatitude: 42.999, longitude: -78.791083, zoom: 16.5)
        mapView.mapType = .hybrid
        if traitCollection.userInterfaceStyle == .light {
            print("Light mode")
        } else {
            print("Dark mode")
            mapView.mapStyle(withFilename: "googlemap_style", andType: "json")
        }
    }
    
    func getParkingLot(withID: Int) -> ParkingLot? {
        for parkingLot in parkingLots {
            if parkingLot.id == withID {
                return parkingLot
            }
        }
        return nil
    }

    // MARK: - DrawerActionDelegate
    
    func didSelectParkingLot(parkingLotID: Int) {
        if let parkingLot = getParkingLot(withID: parkingLotID) {
            let path = GMSMutablePath()
            for boundaryCoord in parkingLot.boundaryCoords {
                path.add(boundaryCoord)
            }
            let bounds = GMSCoordinateBounds.init(path: path)
            let edgeInsets = UIEdgeInsets.init(top: 100, left: 100, bottom: 400.0, right: 100)
            
            let update = GMSCameraUpdate.fit(bounds, with: edgeInsets)
            mapView.animate(with: update)
        }
    }
    
    // MARK: - Map
    
    func addBuildingOverlays() {
        for building in buildings {
            let path = GMSMutablePath()
            for boundaryCoord in building.boundaryCoords {
                path.add(boundaryCoord)
            }
            
            let polygon = GMSPolygon(path: path)
            polygon.fillColor = UIColor(red: 0/255, green: 93/255, blue: 199/255, alpha: 0.20);
            polygon.strokeColor = UIColor(red: 0/255, green: 93/255, blue: 199/255, alpha: 1.0);
            polygon.strokeWidth = 2
            polygon.map = self.mapView
        }
    }
    
    func addParkingLotOverlays() {
        for parkingLot in parkingLots {
            let path = GMSMutablePath()
            for boundaryCoord in parkingLot.boundaryCoords {
                path.add(boundaryCoord)
            }
            
            let polygon = GMSPolygon(path: path)
            polygon.fillColor = UIColor(red: 244/255, green: 245/255, blue: 35/255, alpha: 0.20);
            polygon.strokeColor = UIColor(red: 244/255, green: 245/255, blue: 35/255, alpha: 1.0);
            polygon.strokeWidth = 3
            polygon.map = self.mapView
        }
    }

    // MARK: - Server API

    func retreiveBuildingParkingLotData(complete: @escaping (() -> Void)) {
        AF.request("https://patm-server.herokuapp.com/register_user", method: .post, parameters: ["userID": "123"], headers: nil, interceptor: nil)
        .responseJSON { response in
            switch response.result {
            case .success:
                let json = JSON.init(response.value!)
                //print(json)

                for buildingJSON in json["buildings"] {
                    let building = Building(json: buildingJSON.1)
                    self.buildings.append(building)
                }
                
                for parkingLotJSON in json["lots"] {
                    let parkingLot = ParkingLot(json: parkingLotJSON.1)
                    self.parkingLots.append(parkingLot)
                }
                
                if self.drawerDataSourceDelegate != nil {
                    self.drawerDataSourceDelegate.didRetreiveParkingLots(parkingLots: self.parkingLots)
                }
            case .failure(let error):
                print(error)
            }

            complete()
        }
    }
}
