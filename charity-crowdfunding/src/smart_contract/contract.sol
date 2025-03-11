//SPDX-License-Identifier: MITchange
pragma solidity ^0.8.5; //Use complier version 0.8.5 above

contract project_fund {
    // prevent default value to be pending. Let's set to none instead.
    enum status {
        none,
        pending,
        complete,
        refund
    }

    struct project {
        uint256 project_id;
        string topic;
        string description;
        uint256 current_fund;
        uint256 goal;
        uint256 start;
        uint256 deadline;
        address payable project_owner_address;
        status fund_status;
    }

    struct funder {
        address payable funder_address;
        uint256 value;
        uint256 timestamp_fund;
    }

    mapping(uint256 => project) project_list;
    mapping(uint256 => funder[]) funder_list;

    uint256 project_ID = 1;

    function get_last_project_ID() public view returns (uint256) {
        return project_ID;
    }

    function create_project(
        string memory topic,
        string memory description,
        uint256 goal,
        uint256 deadline
    ) public {
        project_list[project_ID] = project({
            project_id: project_ID,
            topic: topic,
            description: description,
            current_fund: 0,
            goal: goal,
            start: block.timestamp,
            deadline: deadline,
            project_owner_address: payable(msg.sender),
            fund_status: status.pending
        });

        project_ID++;
    }

    function get_project(uint256 ID) public view returns (project memory) {
        return project_list[ID];
    }

    function get_funder_list(uint256 ID) public view returns (funder[] memory) {
        return funder_list[ID];
    }

    function fund_project(uint256 ID) external payable {
        require(
            project_list[ID].fund_status == status.pending,
            "The funding is already terminated"
        );
        require(
            block.timestamp < project_list[ID].deadline,
            "The fundng is expired"
        );
        require(address(msg.sender).balance > msg.value, "Insufficient fund");

        uint256 previous_fund = project_list[ID].current_fund;
        project_list[ID].project_owner_address.transfer(msg.value);
        project_list[ID].current_fund = previous_fund + msg.value;

        funder_list[ID].push(
            funder({
                funder_address: payable(msg.sender),
                value: msg.value,
                timestamp_fund: block.timestamp
            })
        );

        if (project_list[ID].current_fund >= project_list[ID].goal) {
            project_list[ID].fund_status = status.complete;
        }
    }
}
