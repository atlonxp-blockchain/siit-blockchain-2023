// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./CampaignRegistration.sol";
import "./PaymentSystem.sol";

contract DonationSystem is CampaignRegistration, PaymentSystem {
    struct Donation {
        uint256 id;
        address donator_address;
        uint256 campaignId;
        uint256 amount;
        bool is_refunded;
        bool is_transfered_to_owner;
    }

    mapping(uint256 => Donation) public donations;
    uint256 public donateCount;
    address private constant DONATION_POOL =
        0x3b46755B8DB3EE2758620f084b9dBAd65b5Ac73b;
    event DonationMade(
        uint256 indexed campaignId,
        address indexed userId,
        uint256 amount
    );

    function donateToPool(
        uint256 _campaign_id,
        uint256 _amount
    ) public payable {
        require(_amount > 0, "Amount must be greater than zero");
        require(isRegistered(), "User not registered");
        require(
            msg.sender.balance > _amount,
            "Amount must be greater than zero"
        );
        require(campaigns[_campaign_id].id > 0, "Campaign does not exist");

        donateCount++;

        donations[donateCount] = Donation({
            id: donateCount,
            donator_address: msg.sender,
            campaignId: _campaign_id,
            amount: _amount,
            is_refunded: false,
            is_transfered_to_owner: false
        });

        campaigns[_campaign_id].raised_amount += _amount;
        makePayment(_amount, DONATION_POOL);
        emit DonationMade(_campaign_id, msg.sender, _amount);
    }

    function closeCampaign(uint256 _campaignId) public {
        require(_campaignId <= campaignIdCounter, "Invalid campaign ID");
        Campaign storage campaign = campaigns[_campaignId];
        require(campaign.isActive, "Campaign is not active");

        Donation[] memory history = getDonationHistory(_campaignId);
        if (campaign.raised_amount >= campaign.target_donation) {
            //Success campaign
            makePayment(campaign.raised_amount, campaign.owner.user_address);
            for (uint256 i = 1; i <= history.length; i++) {
                history[i].is_transfered_to_owner = true;
            }
        } else {
            require(
                block.timestamp >= campaign.end_date,
                "Campaign end date not reached"
            );
            // Fail campaign => Refund the donated amount to the donators
            for (uint256 i = 1; i <= history.length; i++) {
                makePayment(history[i].amount, history[i].donator_address);
                history[i].is_refunded = true;
            }
        }
        campaign.isActive = false;
        emit CampaignClosed(campaign.id, campaign.title, msg.sender);
    }

    function getDonationHistory(
        uint256 _campaignId
    ) public view returns (Donation[] memory) {
        require(_campaignId <= campaignIdCounter, "Invalid campaign ID");
        Donation[] memory donationHistory = new Donation[](donateCount);
        for (uint256 i = 1; i <= donateCount; i++) {
            if (donations[i].id == _campaignId) {
                donationHistory[i] = donations[i];
            }
        }
        return donationHistory;
    }
}
