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

class MainVC: UIViewController, UITableViewDelegate, UITableViewDataSource {

    @IBOutlet var mapView: GMSMapView!
    @IBOutlet var tableView: UITableView!
    
    var buildings:[Building] = []
    var parkingLots:[Building] = []

    // MARK: - UIViewController
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        tableView.delegate = self
        tableView.dataSource = self
                
        mapView.camera = GMSCameraPosition.camera(withLatitude: 42.999, longitude: -78.791083, zoom: 16.5)
        mapView.mapType = .hybrid
                
        retreiveBuildingParkingLotData() {
            self.addParkingLotOverlays()
            self.addBuildingOverlays()
        }
    }

    // MARK: - MainVC

    
    
    // MARK: - UITableViewDataSource

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 5
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        if (indexPath.row == 0){
            let cell = UITableViewCell.init(style: .subtitle, reuseIdentifier: "1")
            cell.textLabel?.text = "Hochstetter Lot A"
            return cell
        } else if (indexPath.row == 1) {
            let cell = UITableViewCell.init(style: .subtitle, reuseIdentifier: "1")
            cell.textLabel?.text = "Hochstetter Lot B"
            return cell
        } else if (indexPath.row == 2) {
            let cell = UITableViewCell.init(style: .subtitle, reuseIdentifier: "1")
            cell.textLabel?.text = "Hochstetter Lot C"
            return cell
        } else if (indexPath.row == 3) {
            let cell = UITableViewCell.init(style: .subtitle, reuseIdentifier: "1")
            cell.textLabel?.text = "Cooke Lot A"
            return cell
        } else if (indexPath.row == 4) {
            let cell = UITableViewCell.init(style: .subtitle, reuseIdentifier: "1")
            cell.textLabel?.text = "Cooke Lot B"
            return cell
        } else {
            let cell = UITableViewCell.init(style: .subtitle, reuseIdentifier: "1")
            cell.textLabel?.text = "Greiner Lot A"
            return cell
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
            print(response)
            
            switch response.result {
            case .success:
                let json = JSON.init(response.value!)
                print(json)

                for buildingJSON in json["buildings"] {
                    let building = Building(json: buildingJSON.1)
                    self.buildings.append(building)
                }
                
                for parkingLotJSON in json["lots"] {
                    let parkingLot = Building(json: parkingLotJSON.1)
                    self.parkingLots.append(parkingLot)

                }
            case .failure(let error):
                print(error)
            }

            complete()
        }
    }
}
