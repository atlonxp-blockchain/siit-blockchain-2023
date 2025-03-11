// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./UserRegistration.sol";

contract CampaignRegistration is UserRegistration {
    struct Campaign {
        uint256 id;
        string title;
        string description;
        string goal;
        string financial_needs;
        string contribution;
        uint256 target_donation;
        uint256 raised_amount;
        uint256 start_date;
        uint256 end_date;
        bool isActive;
        User owner;
    }

    mapping(uint256 => Campaign) public campaigns;
    uint256 public campaignIdCounter;

    event CampaignCreated(
        uint256 indexed campaignId,
        string title,
        address indexed beneficiary
    );

    event CampaignClosed(
        uint256 indexed campaignId,
        string title,
        address indexed beneficiary
    );

    function createCampaign(
        string memory _title,
        string memory _description,
        string memory _goal,
        string memory _financial_needs,
        string memory _contribution,
        uint256 _targetDonation,
        uint256 _start_date,
        uint256 _end_date
    ) public {
        require(isRegistered(), "Unauthorized");
        require(bytes(_title).length > 0, "Title field is required");
        require(
            bytes(_description).length > 0,
            "Description field is required"
        );
        require(bytes(_goal).length > 0, "Goal field is required");
        require(
            bytes(_financial_needs).length > 0,
            "Financial needs infomation is required"
        );
        require(
            bytes(_contribution).length > 0,
            "Contribution field is required"
        );
        require(_targetDonation > 0, "Target donation is required");
        require(
            _start_date >= block.timestamp,
            "Start date is less than end date"
        );
        require(_end_date > _start_date, "End date is less than start date");

        campaignIdCounter++;

        campaigns[campaignIdCounter] = Campaign({
            id: campaignIdCounter,
            title: _title,
            description: _description,
            goal: _goal,
            financial_needs: _financial_needs,
            contribution: _contribution,
            raised_amount: 0,
            target_donation: _targetDonation,
            start_date: _start_date,
            end_date: _end_date,
            isActive: true,
            owner: users[msg.sender]
        });
        emit CampaignCreated(campaignIdCounter, _title, msg.sender);
    }

    function getAllCampaigns() public view returns (Campaign[] memory) {
        uint256 totalCampaigns = campaignIdCounter;
        Campaign[] memory allCampaigns = new Campaign[](totalCampaigns);

        uint256 index = 0;
        for (uint256 i = 1; i <= totalCampaigns; i++) {
            Campaign storage campaign = campaigns[i];
            if (campaign.isActive) {
                allCampaigns[index] = campaign;
                index++;
            }
        }
        return allCampaigns;
    }
}
