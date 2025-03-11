// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RentalAgreement {
    struct Landlord {
        string dormNames;
        uint balance;
        bool isLandlord;
        //citizen number
        //phone number
    }
    struct Dorm {
        uint256 nextRoomId;
        Room[] rooms;
        uint256 roomCount;
    // other dorm properties
}


    struct Renter {
        address landlordAddress;
        uint deposit;
        uint monthlyPayment;
        uint lastPaymentTime;
        bool active;
        uint balance;
        bool warning;
        bool terminatePending;
        //citizen number
        //phone number
    }

    struct Room {
        uint roomID;
        uint price;
        bool exists;
        uint deposit;
        bool isAvailable;
    }
  
    mapping(string => Dorm) dorms;
    mapping(address => Landlord) landlords;
    mapping(address => Renter) renters;
    mapping(string => address) dormToLandlord;
    //dormRooms[dormName][roomNumber]
    mapping(string => mapping(uint => Room)) dormRooms;
    string[] private dormNames;
    //who is active as renters because we need to loop it
    address[] private activeRenters;
    uint public rentDueInterval = 2 minutes;

    //pending termination
    address[] pendingTermination;

    uint public lastBlockNumber=0;

    constructor() {}
    //register landlord first
    //landlord add room
    //change account and registerRenter
    modifier onlyRenter() {
        require(renters[msg.sender].active, "Only the Rebter can call this function.");
        _; // Continue executing the function after the modifier is applied
    }


    modifier onlyLandlord() {
        require(landlords[msg.sender].isLandlord, "Only the landlord can call this function.");
        _; // Continue executing the function after the modifier is applied
    }


    function registerLandlord(string memory name) public {
        require(bytes(name).length > 0, "Name cannot be empty.");
        require(dormToLandlord[name] == address(0), "Dormitory name already exists.");
        address landlordAddress = msg.sender;
        //add landlord to landlord struct
        landlords[msg.sender]=Landlord(name,0,true);

        //add dorm to landlord struct
        dormToLandlord[name] = landlordAddress;
        //push the name of the dorm in
        dormNames.push(name);
    }
    //add phone number, LineID
    function registerRenter(string memory dormName, uint roomID) public payable {
        (uint roomprice,uint roomdeposit)= getRoomPrice(dormName, roomID);
        //renter will have to input citizenID, dormName ,roomID into thefunction
        require(msg.value == roomdeposit, "Deposit is not enough.");
        require(checkifinList(dormNames, dormName), "Invalid dormitory name.");
        address landlordAddress = dormToLandlord[dormName];
        require(dormRooms[dormName][roomID].deposit >= roomdeposit, "Deposit is not enough.");

        // //landlord hold the deposits
        // landlords[landlordAddress].balance+=msg.value;
        // landlordAddress;deposit;monthlyPayment;lastPaymentTime;active;balance;warning;renteraddress
        renters[msg.sender] = Renter(landlordAddress, roomdeposit,roomprice, block.timestamp, true,0,false,false);
        //room now not available
        dormRooms[dormName][roomID].isAvailable=false;
        //add into active renter
        activeRenters.push(msg.sender);
    }

    function getAllDormNames() public view returns (string[] memory) {
        return dormNames;
    }

    function getAvailableRooms(string memory dormName) public view returns (uint256[] memory) {
    uint256[] memory temp = new uint256[](dorms[dormName].roomCount);
    uint256 j = 0;
    
    for (uint256 i = 0; i < dorms[dormName].roomCount; i++) {
        if (dorms[dormName].rooms[i].isAvailable) {
            temp[j] = i;
            j++;
        }
    }
    
    uint256[] memory result = new uint256[](j);
    for (uint256 i = 0; i < j; i++) {
        result[i] = temp[i];
    }
    
    return result;
}


    
    function getBalanceRenter() public onlyRenter view returns  (uint256) {
        return renters[msg.sender].balance;
    }
    function getBalanceLandlord() public onlyLandlord view returns  (uint256) {
        return landlords[msg.sender].balance;
    }
    

    function addRoom(string memory dormName, uint price, uint deposit) public onlyLandlord {
        address landlordAddress = dormToLandlord[dormName];
        require(msg.sender == landlordAddress, "Only the landlord can add rooms.");
        uint roomId = dorms[dormName].nextRoomId;
        Room storage room = dormRooms[dormName][roomId];
        if (!room.exists) {
            require(price > 0, "Price must be greater than zero.");
            room.exists = true;
            room.price = price;
            room.deposit = deposit;
            room.isAvailable=true;

        }

        dorms[dormName].rooms.push(room);
        dorms[dormName].roomCount++;
        dorms[dormName].nextRoomId++;
    }
    

    function getRoomPrice(string memory dormName, uint roomId) public view returns (uint,uint) {
        Room storage room = dormRooms[dormName][roomId];
        require(room.exists,"room did not exists"); 
        return (room.price,room.deposit);
    }


    function depositRent() public payable {
        require(renters[msg.sender].active, "Renter is not active.");
        require(msg.value > 0, "Deposit amount must be greater than zero.");

        renters[msg.sender].balance += msg.value;
    }

    //withdrawforLandlord
    function withdrawRent(uint amount) public  onlyLandlord{

        require(landlords[msg.sender].balance >amount, "Insufficient balance.");
        address payable  recipient= payable(msg.sender);
        landlords[msg.sender].balance-= amount;
        recipient.transfer(amount);
        
    }

    function depositLandlord() public payable onlyLandlord{
        
        require(msg.value > 0, "Deposit amount must be greater than zero.");

        landlords[msg.sender].balance += msg.value;
    }


    //withdraw for renters
    function withdrawBalance(uint amount) public 
    {
        require(renters[msg.sender].balance>amount,"You don't have enough money");
        address payable  recipient= payable(msg.sender);
        renters[msg.sender].balance-= amount;
        recipient.transfer(amount);

    }

    function terminateContractRenter() public returns (uint)
    {
        //create a list of pending renter and will loop through all the list to check who is pending
        require(renters[msg.sender].terminatePending==false,"Please wait for landlord confirmation");
        pendingTermination.push(msg.sender);
        renters[msg.sender].terminatePending=true;
        
        return 1;
    }
    function terminateContractLandlord (address termiAddress) public payable onlyLandlord
    {
        require(getPendingTermination().length!=0,"There is no one to terminate");
        require(renters[termiAddress].active, "Renter is not active.");
        //transfer deposits from contract to renter
        payable(termiAddress).transfer(renters[termiAddress].deposit);
        renters[termiAddress].active = false;
        removeElement(activeRenters,termiAddress);
    }

    function getPendingTermination() public view returns (address[] memory) {
    address landlord = msg.sender;
    address[] memory temp;
    uint count = 0;
    
    for (uint i = 0; i < pendingTermination.length; i++) {
        if (renters[pendingTermination[i]].landlordAddress == landlord) {
            count++;
        }
    }
    
    temp = new address[](count);
    uint j = 0;
    
    for (uint i = 0; i < pendingTermination.length; i++) {
        if (renters[pendingTermination[i]].landlordAddress == landlord) {
            temp[j] = pendingTermination[i];
            j++;
        }
    }
    
    return temp;
}




    //terminate automatically when not pay rent
    function terminateContractAuto(address termiAddress) private  
    {
        //not paying back deposit since you dont pay up
        require(renters[termiAddress].active, "Renter is not active.");
        renters[termiAddress].active = false;
        landlords[renters[termiAddress].landlordAddress].balance +=renters[termiAddress].deposit;
        removeElement(activeRenters,termiAddress);
    }

    //automatic pay
    function autopay() public  {
    for(uint i=0;i<activeRenters.length;i++)
    {
        address currentAddress=activeRenters[i];
        require(renters[currentAddress].active, "Renter is not active");
        // check if it's time to pay rent
        if (block.timestamp - renters[currentAddress].lastPaymentTime >= rentDueInterval) 
        {
                uint rentAmount = renters[currentAddress].monthlyPayment;
                // check if renter has enough balance to pay the rent
                if (renters[currentAddress].balance >= rentAmount) {
                    landlords[renters[currentAddress].landlordAddress].balance += rentAmount;
                    renters[currentAddress].balance -= rentAmount;
                    renters[currentAddress].lastPaymentTime = block.timestamp;
                } 
                else 
                {
                    if(renters[currentAddress].warning==true)
                    {
                        terminateContractAuto(currentAddress);
                    }
                    else
                    {
                         renters[currentAddress].warning = true;
                    }
                   
                }
        }
        
    }
}












    //helperfunction
    function checkifinList(string[] memory list, string memory _dormname) private pure returns (bool) 
    {
        for (uint256 i = 0; i < list.length; i++) 
        {
            if (keccak256(bytes(list[i])) == keccak256(bytes(_dormname))) 
            {
                return true;
            }
        }
        return false;
    }
    function removeElement(address[] storage array, address element) internal {
    for (uint i = 0; i < array.length; i++) {
        if (array[i] == element) {
            array[i] = array[array.length - 1];
            array.pop();
            return;
        }
    }
}


}
