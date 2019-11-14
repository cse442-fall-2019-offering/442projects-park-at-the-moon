//
//  DrawerVC.swift
//  university-parking
//
//  Created by Arthur De Araujo on 10/20/19.
//  Copyright © 2019 Arthur De Araujo. All rights reserved.
//

import UIKit
import Pulley
import SearchTextField

protocol DrawerDataSourceDelegate {
    func didRetreiveParkingLots(parkingLots: [ParkingLot], buildings: [Building])
}

class DrawerVC: UIViewController, PulleyDrawerViewControllerDelegate, UITextFieldDelegate, UITableViewDelegate, UITableViewDataSource, DrawerDataSourceDelegate {

    @IBOutlet var searchTextField: SearchTextField!
    @IBOutlet var tableView: UITableView!
    @IBOutlet var availableLotsLabel: UILabel!
    @IBOutlet var spotsLabel: UILabel!
    
    var parkingLots: [ParkingLot] = []
    var buildings: [Building] = []
    var keyboardHeight:CGFloat?
    var hasAddedSearchFilters = false
    
    var drawerActionDelegate: DrawerActionDelegate!
    
    // MARK: - UIViewController

    override func viewDidLoad() {
        super.viewDidLoad()

        tableView.delegate = self
        tableView.dataSource = self
        
        setupSearch()
                
        NotificationCenter.default.addObserver(self,
            selector: #selector(keyboardWasShown(notification:)),
            name: UIResponder.keyboardWillShowNotification,
            object: nil)

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
    
    deinit {
        NotificationCenter.default.removeObserver(self)
    }
    
    // MARK: - DrawerVC
    
    func setupSearch(){
        searchTextField.delegate = self
        searchTextField.placeholder = "Search for classroom building"
        
        // Add set theme
        if traitCollection.userInterfaceStyle == .light {
            searchTextField.theme = SearchTextFieldTheme.lightTheme()
        } else {
            searchTextField.theme = SearchTextFieldTheme.darkTheme()
        }
        searchTextField.theme.font = UIFont.systemFont(ofSize: 16.0)
        searchTextField.theme.cellHeight = 44
        
        searchTextField.itemSelectionHandler = { item, itemPosition in
            let searchedBuildingName = item[0].title
            for building in self.buildings {
                if building.name == searchedBuildingName {
                    self.drawerActionDelegate.didSearchBuilding(buildingID: building.id)
                }
            }
            
            self.searchTextField.text = ""
            self.pulleyViewController?.setDrawerPosition(position: .collapsed, animated: true)
            self.searchTextField.endEditing(true)
        }
    }
    
    func addSearchFiltersIfNeeded() {
        if !hasAddedSearchFilters {
            var buildingNames:[String] = []
            for building in buildings {
                buildingNames.append(building.name)
            }

            searchTextField.filterStrings(buildingNames)
            hasAddedSearchFilters = true
        }
    }
    
    // MARK: - DrawerDataSourceDelegate

    func didRetreiveParkingLots(parkingLots: [ParkingLot], buildings: [Building]) {
        self.parkingLots = parkingLots
        self.buildings = buildings
        self.tableView.reloadData()
        addSearchFiltersIfNeeded()
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
        return 100.0
    }

    func partialRevealDrawerHeight(bottomSafeArea: CGFloat) -> CGFloat {
        if (searchTextField.isEditing && (keyboardHeight != nil)) {
            return keyboardHeight! + 180
        } else {
            return 375.0
        }
    }
    
    func drawerPositionDidChange(drawer: PulleyViewController, bottomSafeArea: CGFloat) {
        if drawer.drawerPosition == .collapsed {
            searchTextField.endEditing(true)
        }
    }
        
    // MARK: - UITextFieldDelegate
    
    func textFieldDidBeginEditing(_ textField: UITextField) {
        UIView.animate(withDuration: 0.2, delay: 0.15, options: .curveEaseOut, animations: {
            self.availableLotsLabel.alpha = 0.25
            self.spotsLabel.alpha = 0.25
            self.tableView.alpha = 0.25
        }, completion: nil)
    }
    
    func textFieldDidEndEditing(_ textField: UITextField) {
        UIView.animate(withDuration: 0.2, delay: 0.15, options: .curveEaseIn, animations: {
            self.availableLotsLabel.alpha = 1.0
            self.spotsLabel.alpha = 1.0
            self.tableView.alpha = 1.0
        }, completion: nil)
    }

    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        searchTextField.endEditing(true)
        self.pulleyViewController?.setDrawerPosition(position: .collapsed, animated: true)
        
        return true
    }
    
    // MARK: - Keyboard
    
    @objc func keyboardWasShown(notification: NSNotification) {
        let info = notification.userInfo!
        keyboardHeight = (info[UIResponder.keyboardFrameEndUserInfoKey] as! NSValue).cgRectValue.size.height
        self.pulleyViewController?.setDrawerPosition(position: .partiallyRevealed, animated: true)
    }
}
