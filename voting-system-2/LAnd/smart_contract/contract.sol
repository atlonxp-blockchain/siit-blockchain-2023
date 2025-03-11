// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Poll {
    mapping(string => User) username_to_info;
    address public owner;
    string[] public candidateList;
    Candidate[] public candidateInfo;
    mapping(string => uint256) public votesReceived;
    mapping(address => bool) public isVoted;
    mapping(address => User) public users; // Mapping to store user information
    address[] public userAddresses; // Array to store user addresses
    enum State {
        Created,
        Voting,
        Ended
    }
    State public state;
    address public electionContract;

    struct Candidate {
        uint id;
        string name;
        string party;
        string campaignMessage;
    }
    
    struct User {
        string username;
        string password;
        string firstName;
        string lastName;
    }

    mapping(uint256 => Candidate) public candidates;
    uint256 public candidateCount;

    struct CandidateVote {
        string candidate;
        uint256 voteCount;
    }

    event VoteStarted();
    event VoteEnded();
    event UserRegistered(address userAddress);

    constructor() {
        owner = msg.sender;
        state = State.Created;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    function startVote() public onlyOwner {
        require(state == State.Created, "Vote has already started");

        state = State.Voting;
        emit VoteStarted();
    }

    function endVote() public onlyOwner {
        require(state == State.Voting, "Vote has not started yet");

        state = State.Ended;
        emit VoteEnded();
    }

    function addCandidate(
        uint256 _id,
        string memory _name,
        string memory _party,
        string memory _campaignMessage
    ) public onlyOwner {
        candidates[_id] = Candidate(_id, _name, _party, _campaignMessage);
        candidateList.push(_name);
        candidateCount++;
        candidateInfo.push(Candidate(_id, _name, _party, _campaignMessage));
    }

    function voteForCandidate(string memory _candidate) public {
        require(state == State.Voting, "Vote has not started or has ended");
        require(isVoted[msg.sender] == false, "Already voted");
        require(candidateExists(_candidate), "Invalid candidate");

        isVoted[msg.sender] = true;
        votesReceived[_candidate] += 1;
    }

    function getVoteCountsForAllCandidates()
        public
        view
        returns (CandidateVote[] memory)
    {
        require(state == State.Ended, "Vote has not ended");

        CandidateVote[] memory voteCounts = new CandidateVote[](
            candidateList.length
        );
        for (uint256 i = 0; i < candidateList.length; i++) {
            voteCounts[i] = CandidateVote(
                candidateList[i],
                votesReceived[candidateList[i]]
            );
        }
        return voteCounts;
    }

    function candidateExists(
        string memory _candidate
    ) internal view returns (bool) {
        for (uint256 i = 0; i < candidateList.length; i++) {
            if (
                keccak256(bytes(candidateList[i])) ==
                keccak256(bytes(_candidate))
            ) {
                return true;
            }
        }
        return false;
    }

    function registerUser(
        string memory _username,
        string memory _password,
        string memory _firstName,
        string memory _lastName
    ) public {
        require(
            bytes(_username).length > 0,
            "Username cannot be empty"
        );
        require(
            bytes(_password).length > 0,
            "Password cannot be empty"
        );
        require(
            bytes(_firstName).length > 0,
            "First name cannot be empty"
        );
        require(
            bytes(_lastName).length > 0,
            "Last name cannot be empty"
        );
        

        username_to_info[_username].username = _username;
        username_to_info[_username].password = _password;
        username_to_info[_username].firstName = _firstName;
        username_to_info[_username].lastName = _lastName;

       

        emit UserRegistered(msg.sender);
    }

    function getUserCount() public view returns (uint256) {
        return userAddresses.length;
    }

    function getUserByIndex(uint256 index)
        public
        view
        returns (
            string memory,
            string memory,
            string memory,
            string memory
        )
    {
        require(index < userAddresses.length, "Invalid index");

        address userAddress = userAddresses[index];
        User memory user = users[userAddress];

        return (user.username, user.password, user.firstName, user.lastName);
    }

    function getCandidate() public view returns (string[] memory) {
        return candidateList;
    }

    function getCandidateInfo() public view returns (Candidate[] memory) {
        return candidateInfo;
    }

    function get_user_info(string memory username) public view returns (User memory){
        return username_to_info[username];
}
} 