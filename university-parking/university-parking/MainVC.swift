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
            self.addParkingLotMarkers()
            self.addBuildingOverlays()
            if self.drawerDataSourceDelegate != nil {
                self.drawerDataSourceDelegate.didRetreiveParkingLots(parkingLots: self.parkingLots)
            }
        }
        Timer.scheduledTimer(timeInterval: 3, target: self, selector: #selector(reloadData), userInfo: nil, repeats: true)
    }

    // MARK: - MainVC
    
    @objc func reloadData() {
        print("Reloaded Data")
        retreiveBuildingParkingLotData() {
            if self.drawerDataSourceDelegate != nil {
                self.drawerDataSourceDelegate.didRetreiveParkingLots(parkingLots: self.parkingLots)
            }
        }
    }
    
    func setupMapAppearance() {
        mapView.camera = GMSCameraPosition.camera(withLatitude: 42.999, longitude: -78.791083, zoom: 16.5)
        mapView.mapType = .normal
        if traitCollection.userInterfaceStyle == .light {
            print("Light mode")
            mapView.mapStyle(withFilename: "googlemap_style_light", andType: "json")
        } else {
            print("Dark mode")
            mapView.mapStyle(withFilename: "googlemap_style_dark", andType: "json")
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
    
    func addParkingLotMarkers() {
        for parkingLot in parkingLots {
            let marker = GMSMarker(position: parkingLot.centerCoord)
            //marker.title = parkingLot.name
            marker.icon = UIImage.init(named: "lot-marker")
            marker.map = mapView
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

                self.buildings = []
                for buildingJSON in json["buildings"] {
                    let building = Building(json: buildingJSON.1)
                    self.buildings.append(building)
                }
                
                self.parkingLots = []
                for parkingLotJSON in json["lots"] {
                    let parkingLot = ParkingLot(json: parkingLotJSON.1)
                    self.parkingLots.append(parkingLot)
                }
                self.parkingLots = self.parkingLots.sorted(by: { $0.spotsAvailable > $1.spotsAvailable })
                
                self.parkingLots = self.parkingLots.sorted {
                    if $0.spotsAvailable != $1.spotsAvailable { // first, compare by spots
                        return $0.spotsAvailable > $1.spotsAvailable
                    } else { // All other fields are tied, break ties by name
                        return $0.name < $1.name
                    }
                }

                
            case .failure(let error):
                print(error)
            }

            complete()
        }
    }
}
