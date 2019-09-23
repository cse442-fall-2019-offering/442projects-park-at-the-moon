//
//  OnboardingVC.swift
//  university-parking
//
//  Created by Arthur De Araujo on 9/19/19.
//  Copyright © 2019 Arthur De Araujo. All rights reserved.
//

import UIKit

class OnboardingVC: UIViewController {

    @IBOutlet var titleLabelTopConstraint: NSLayoutConstraint!
    
    // MARK: - UIViewController

    override func viewDidLoad() {
        super.viewDidLoad()

        self.setNeedsStatusBarAppearanceUpdate()

        if (UIDevice.current.userInterfaceIdiom == .pad) {
            titleLabelTopConstraint.constant = 200
        }
    }
    
    override var preferredStatusBarStyle : UIStatusBarStyle {
        return .lightContent
    }
    
    // MARK: - OnboardingVC

    // MARK: - Actions

    /*
     TODO: Create LGButtons and place them
     programmatically after fetching the universities
     from the server
    */
    @IBAction func selectedUniversityAtBuffalo(_ sender: Any) {
        performSegue(withIdentifier: "segueToMain", sender: self)
    }
    
}
