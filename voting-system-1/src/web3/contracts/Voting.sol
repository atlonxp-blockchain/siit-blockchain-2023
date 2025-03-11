// // SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

contract Voting {
    struct Campaign{
        address owner;
        string title;
        string description;
        uint256 target;
        uint256 deadline;
        uint256 amountCollected;
        string image;
        address[] voters;
    }

    mapping(uint256 => Campaign) public campaigns;
  
    uint256 public numberOfCampaigns = 0;

    function createCampaign(address _owner, string memory _title, string memory _description, 
        uint256 _target, uint256 _deadline, string memory _image) public returns(uint256) {
        Campaign storage campaign = campaigns[numberOfCampaigns];

        //if everything okay?
        require(campaign.deadline < block.timestamp, "The deadline should be a date in the future");
        campaign.owner = _owner;
        campaign.title = _title;
        campaign.description = _description;
        campaign.target = _target;
        campaign.deadline = _deadline;
        campaign.amountCollected = 0;
        campaign.image = _image;

        numberOfCampaigns++;
        return numberOfCampaigns - 1; //return the index of the most newly created campaign
    }

    function isDuplicate(uint256 _id) public view returns (bool) {
        for(uint i = 0; i < campaigns[_id].voters.length; i++){
            if(campaigns[_id].voters[i] == msg.sender) return true;
        }
        return false;
    }
    


    function vote(uint256 _id) public {
        require(!(isDuplicate(_id)),"You have already voted");
        Campaign storage campaign = campaigns[_id];
        campaign.voters.push(msg.sender);
        campaign.amountCollected++;
    }

    function getVoters(uint256 _id) view public returns(address[] memory) {
        return campaigns[_id].voters;
    }

    function getCampaigns() public view returns(Campaign[] memory){
        Campaign[] memory allCampaign = new Campaign[](numberOfCampaigns); //create empty array with numberOfCampaigns index
        
        for(uint i = 0; i < numberOfCampaigns; i++){
            Campaign storage item = campaigns[i];
            allCampaign[i] = item;
        }
        return allCampaign;
    }
}