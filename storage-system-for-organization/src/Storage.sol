//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Storage{

    struct Stash{
        uint stashid;
        uint itemid;
        string itemName;
        bool isBorrowed;
        string borrowingBy;
        uint borrowTime;
    }

    uint stashcounter;
    mapping (uint => Stash) stashs;
    uint[] keys;

    function addItem(uint _itemid,string memory _itemName) public{
        stashcounter++;
        stashs[_itemid] = Stash(stashcounter, _itemid, _itemName, false, "", block.timestamp);
        keys.push(_itemid);
    }


    function changeItemName(uint _itemid,string memory _itemName) public{
        stashs[_itemid].itemName = _itemName;
    }


    function borrowItem(uint _itemid, string memory _borrowerName) public {
        require(!stashs[_itemid].isBorrowed,"Item is being borrowed");

        stashs[_itemid].borrowingBy = _borrowerName;
        stashs[_itemid].borrowTime = block.timestamp;
        stashs[_itemid].isBorrowed = true;
    }


    function returnItem(uint _itemid) public {
        require(stashs[_itemid].isBorrowed,"Item has not been borrowed");

        stashs[_itemid].isBorrowed = false;
        stashs[_itemid].borrowingBy = "";
    }




    function getIsBorrowed(uint _itemid) public view returns (bool){

        return stashs[_itemid].isBorrowed;
        
    }

    function getBorrowingBy(uint _itemid) public view returns (string memory){

        return stashs[_itemid].borrowingBy;
        
    }

    function getItemName(uint _itemid) public view returns (string memory){
        return stashs[_itemid].itemName;
    }

    function getBorrowTime(uint _itemid) public view returns (uint){
        return stashs[_itemid].borrowTime;
    }

    function sort() public  {
            uint length = keys.length;
            for (uint i = 1; i < length; i++) {
                uint key = keys[i];
                int j = int(i) - 1;
                while ((int(j) >= 0) && (keys[uint(j)] > key)) {
                    keys[uint(j + 1)] = keys[uint(j)];
                    j--;
                }
                keys[uint(j + 1)] = key;
            }
        }

    function getKeys() public view returns (uint[] memory){
        return keys;
    }
}