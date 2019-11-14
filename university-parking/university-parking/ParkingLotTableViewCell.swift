//
//  ParkingLotTableViewCell.swift
//  university-parking
//
//  Created by Arthur De Araujo on 10/20/19.
//  Copyright © 2019 Arthur De Araujo. All rights reserved.
//

import UIKit

class ParkingLotTableViewCell: UITableViewCell {

    @IBOutlet var nameLabel: UILabel!
    @IBOutlet var spotsLabel: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()

    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

    }

}
