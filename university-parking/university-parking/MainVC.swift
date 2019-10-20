//
//  MainVC.swift
//  university-parking
//
//  Created by Arthur De Araujo on 9/15/19.
//  Copyright © 2019 Arthur De Araujo. All rights reserved.
//

import UIKit
import MapKit
import Alamofire

class MainVC: UIViewController, UITableViewDelegate, UITableViewDataSource {

    @IBOutlet var mapView: MKMapView!
    @IBOutlet var tableView: UITableView!
    
    // MARK: - UIViewController
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        tableView.delegate = self
        tableView.dataSource = self
        
        let centerCoord = CLLocationCoordinate2D.init(latitude: 43, longitude: -78.791083)
        
        mapView.setCamera(MKMapCamera.init(lookingAtCenter: centerCoord, fromEyeCoordinate: centerCoord, eyeAltitude: 1250), animated: false);
        mapView.mapType = .hybrid
        
        retreiveAllLocations()
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

}

// MARK: - Server API

func retreiveAllLocations() {
    AF.request("https://patm-server.herokuapp.com/register_user", method: .post, parameters: ["userID": "123"], headers: nil, interceptor: nil)
    .responseJSON { response in
        print(response)
        
        let JSON = response.value as! NSDictionary
        print(JSON)

        for i in JSON.allKeys {
            print(i)
        }
        
        if let buildingsJSON = JSON.value(forKey: "buildings") {
            for i in buildingsJSON {
                print(i)
            }
        }
        

    }
}
