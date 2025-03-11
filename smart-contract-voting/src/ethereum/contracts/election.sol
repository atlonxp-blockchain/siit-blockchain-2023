pragma solidity ^0.8.0;


// WARNING: For using the ElectionID as parameter, use 0x as prefix. Such as the first election is usually named '0x1'.

contract VotingSystem {
    event ErrorOccurred(string errorMessage);

    struct Voter {
        string username;
        string password;
    }
    struct Candidate {
        string name;
        string party;
        string campaignMessage;
    }
    struct Vote {
        address candidateAddr;
        uint256 voteCount;
    }

    struct Election {
        uint256 startDate;
        uint256 endDate;
        address[] candidateAddresses;
        address[] voterAddresses;
        mapping(address => uint256) voteCount;
        mapping(address => bool) hasVoted;
    }

    enum ElectionType {
        General,
        Primary,
        Runoff,
        Referendum
    }

    mapping(address => Voter) voters;
    mapping(address => Candidate) candidates;
    mapping(bytes32 => Election) elections;

    address[] public candidateAddresses;
    bytes32 public electionCounter;

    function register(string memory _username, string memory _password) public { // Register as voter
        voters[msg.sender] = Voter(_username, _password);
    }

    function authenticate( // Check Username and Password, not utilized atm
        string memory _username,
        string memory _password
    ) public view returns (bool) {
        Voter memory voter = voters[msg.sender];
        return (keccak256(abi.encodePacked(_username)) ==
            keccak256(abi.encodePacked(voter.username)) &&
            keccak256(abi.encodePacked(_password)) ==
            keccak256(abi.encodePacked(voter.password)));
    }

    function registerCandidate( // Register as candidate
        string memory _name,
        string memory _party,
        string memory _campaignMessage
    ) public {
        address candidateAddr = msg.sender;
        candidates[msg.sender] = Candidate(_name, _party, _campaignMessage);
        candidateAddresses.push(candidateAddr);
    }

    function getCandidate( // Get candidate from address
        address _candidateAddr
    ) public view returns (Candidate memory) {
        return candidates[_candidateAddr];
    }

    function hasVoted( // Check whether the voter is voted in the election specified by electionID
        bytes32 _electionId,
        address _voterAddress
    ) public view returns (bool) {
        return elections[_electionId].hasVoted[_voterAddress];
    }

    function vote( // Vote by given ElectionID and both addresses, Checks whether candidate is in the election and whether voter is voted. If so, emit errors. 
        bytes32 _electionId,
        address _voterAddress,
        address _candidateAddress
    ) public {
        if (!isValidCandidate(_electionId, _candidateAddress)) {
            emit ErrorOccurred("Invalid candidate");
        }

        Election storage election = elections[_electionId];

        if (election.hasVoted[_voterAddress]) {
            emit ErrorOccurred("User Voted");
        }

        election.hasVoted[_voterAddress] = true;

        election.voteCount[_candidateAddress]++;
    }

    function isValidCandidate( // Helper function used in vote()
        bytes32 _electionId,
        address _candidateAddr
    ) internal view returns (bool) {
        Election storage election = elections[_electionId];
        for (uint256 i = 0; i < election.candidateAddresses.length; i++) {
            if (election.candidateAddresses[i] == _candidateAddr) {
                return true;
            }
        }
        return false;
    }

    function getResultsFromElection( // Provide electionID, returns 2 arrays with first being all candidates(informations), second being their votes
        bytes32 _electionID
    ) public view returns (Candidate[] memory, uint256[] memory) {
        Election storage election = elections[_electionID];
        uint256 numCandidates = election.candidateAddresses.length;
        Candidate[] memory result = new Candidate[](numCandidates);
        uint256[] memory voteCounts = new uint256[](numCandidates);

        for (uint256 i = 0; i < numCandidates; i++) {
            address candidateAddr = election.candidateAddresses[i];
            result[i] = candidates[candidateAddr];
            voteCounts[i] = election.voteCount[candidateAddr];
        }

        return (result, voteCounts);
    }

    function getResults() public view returns (Candidate[] memory) { // Return all candidates, (Not used)
        uint256 numCandidates = getNumCandidates();
        Candidate[] memory result = new Candidate[](numCandidates);
        for (uint256 i = 0; i < numCandidates; i++) {
            result[i] = getCandidate(getCandidateAddress(i));
        }
        return result;
    }

    function getCandidateAddress(uint256 _index) public view returns (address) { // Given an index in candidate array, return the address (Not used)
        return candidateAddresses[_index];
    }

    function getNumCandidates() public view returns (uint256) {
        uint256 count = 0;
        for (uint256 i = 0; i < candidateAddresses.length; i++) {
            count++;
        }
        return count;
    }

    function getCandidateByName( // Given a name of candidate return the address
        string memory _name
    ) public view returns (address) {
        for (uint256 i = 0; i < candidateAddresses.length; i++) {
            Candidate memory candidate = candidates[candidateAddresses[i]];
            if (
                keccak256(abi.encodePacked(candidate.name)) ==
                keccak256(abi.encodePacked(_name))
            ) {
                return candidateAddresses[i];
            }
        }
        revert("Candidate not found");
    }

    function createElection( // the _candidateAddresses can be explicitly defined by passing addresses, or just []
        uint256 _startDate,
        uint256 _endDate,
        address[] memory _candidateAddresses
    ) public {
        bytes32 electionId = electionCounter;
        electionCounter = incrementBytes32(electionCounter);
        Election storage newElection = elections[electionId];
        newElection.startDate = _startDate;
        newElection.endDate = _endDate;
        newElection.candidateAddresses = _candidateAddresses;
    }

    function addCandidateToElection(
        bytes32 _electionID,
        address _candidateAddr
    ) public {
        elections[_electionID].candidateAddresses.push(_candidateAddr);
    }

    function getCandidateAddressesForElection( // Used to check all the current candidates in an election
        bytes32 _electionID
    ) public view returns (address[] memory) {
        return elections[_electionID].candidateAddresses;
    }

    function findCandidateIndexv3( // helper function for checking the candidate is registered in an election or not
        address[] memory _candidateAddresses,
        address _candidateAddress
    ) public pure returns (uint256) {
        for (uint256 i = 0; i < _candidateAddresses.length; i++) {
            if (_candidateAddresses[i] == _candidateAddress) {
                return i;
            }
        }
        return 2 ** 256 - 1; // Fancier -1 but okay
    }

    function incrementBytes32(bytes32 _value) private pure returns (bytes32) { // Helper function
        return bytes32(uint256(_value) + 1);
    }
}