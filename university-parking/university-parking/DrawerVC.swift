//
//  DrawerVC.swift
//  university-parking
//
//  Created by Arthur De Araujo on 10/20/19.
//  Copyright © 2019 Arthur De Araujo. All rights reserved.
//

import UIKit
import Pulley

protocol DrawerDataSourceDelegate {
    func didRetreiveParkingLots(parkingLots: [ParkingLot])
}

class DrawerVC: UIViewController, PulleyDrawerViewControllerDelegate, UISearchBarDelegate, UITableViewDelegate, UITableViewDataSource, DrawerDataSourceDelegate {

    @IBOutlet var searchBar: UISearchBar!
    @IBOutlet var tableView: UITableView!
    
    var parkingLots: [ParkingLot] = []
    
    var drawerActionDelegate: DrawerActionDelegate!
    
    // MARK: - UIViewController

    override func viewDidLoad() {
        super.viewDidLoad()

        searchBar.delegate = self
        tableView.delegate = self
        tableView.dataSource = self
                
        self.pulleyViewController?.setDrawerPosition(position: .closed, animated: false)
    }
    
    override func viewDidAppear(_ animated: Bool) {
        if let pulleyVC = self.pulleyViewController {
            let navController = (pulleyVC.primaryContentViewController as! NavigationController)
            let mainVC = navController.viewControllers[0] as! MainVC
            
            mainVC.drawerDataSourceDelegate = self
            self.drawerActionDelegate = mainVC
            self.parkingLots = mainVC.parkingLots
            
            tableView.reloadData()
            self.pulleyViewController?.setDrawerPosition(position: .partiallyRevealed, animated: false)
        }
    }
    
    // MARK: - DrawerVC
    
    // MARK: - DrawerDataSourceDelegate

    func didRetreiveParkingLots(parkingLots: [ParkingLot]) {
        self.parkingLots = parkingLots
    }

    // MARK: - UITableViewDataSource

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return parkingLots.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let parkingLot = parkingLots[indexPath.row]
        
        let cell = tableView.dequeueReusableCell(withIdentifier: "parkingLotCellReuseIdentifier", for: indexPath) as! ParkingLotTableViewCell
        cell.nameLabel?.text = parkingLot.name
        cell.spotsLabel?.text = String(parkingLot.spotsAvailable)
        
        return cell
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        drawerActionDelegate.didSelectParkingLot(parkingLotID: parkingLots[indexPath.row].id)
    }
    
    // MARK: - PulleyDrawerViewControllerDelegate
    
    func collapsedDrawerHeight(bottomSafeArea: CGFloat) -> CGFloat {
        return 90.0
    }

    func partialRevealDrawerHeight(bottomSafeArea: CGFloat) -> CGFloat {
        return 375.0
    }
    
    // MARK: - UISearchBarDelegate
    
    func searchBarShouldBeginEditing(_ searchBar: UISearchBar) -> Bool {
        self.pulleyViewController?.setDrawerPosition(position: .partiallyRevealed, animated: true)
        
        return true
    }
    
    func searchBarSearchButtonClicked(_ searchBar: UISearchBar) {
        searchBar.endEditing(true)
    }
}
