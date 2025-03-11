const provider = new ethers.providers.Web3Provider(
    window.ethereum,
    "sepolia"
  );

  const StorageContractAddress = "0x4e7DB005350B9A04643a35bFf9Fb04020Ab04e6C";
  const StorageContractABI = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_itemid",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_itemName",
				"type": "string"
			}
		],
		"name": "addItem",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_itemid",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_borrowerName",
				"type": "string"
			}
		],
		"name": "borrowItem",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_itemid",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_itemName",
				"type": "string"
			}
		],
		"name": "changeItemName",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_itemid",
				"type": "uint256"
			}
		],
		"name": "returnItem",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "sort",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_itemid",
				"type": "uint256"
			}
		],
		"name": "getBorrowingBy",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_itemid",
				"type": "uint256"
			}
		],
		"name": "getBorrowTime",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_itemid",
				"type": "uint256"
			}
		],
		"name": "getIsBorrowed",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_itemid",
				"type": "uint256"
			}
		],
		"name": "getItemName",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getKeys",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
];

let StorageContract;
let signer;

provider.send("eth_requestAccounts", []).then(() => {
    provider.listAccounts().then(function (accounts) {
      signer = provider.getSigner(accounts[0]);
      StorageContract = new ethers.Contract(
        StorageContractAddress,
        StorageContractABI,
        signer
      );
    });
});


async function addItem() {
    const itemID = document.getElementById("itemID").value;
    const itemName = document.getElementById("itemName").value;
    const isexist = await isExist(itemID);
    if(isexist){
        document.getElementById('addItemFeed').innerHTML = "Item ID has been used";
    }
    else{
        const addItemPromise = StorageContract.addItem(itemID,itemName);
        await addItemPromise;
        document.getElementById('addItemFeed').innerHTML = "Item added";
    }

}

async function borrowItem(){
    const itemID = document.getElementById("itemIDBorrow").value;
    const borrowBy = document.getElementById("borrowBy").value;
    const getIsBorrowPromise = StorageContract.getIsBorrowed(itemID);
    const isBorrow = await getIsBorrowPromise;
    const itemName = await StorageContract.getItemName(itemID);
    if (isBorrow){
        document.getElementById('borrowFeed').innerHTML = itemName+" is being borrowed";
    }
    else{
        const isexist = await isExist(itemID);
        if (isexist){
            const borrowItemPromise = StorageContract.borrowItem(itemID,borrowBy);
            await borrowItemPromise;
			document.getElementById('borrowFeed').innerHTML = "Borrow succeed";
        }
        else{
            document.getElementById('borrowFeed').innerHTML = "Item does not exist";
        }
    }
}

async function returnItem(){
    const itemID = document.getElementById("returnItemID").value;
    const getIsBorrowPromise = StorageContract.getIsBorrowed(itemID);
    const isBorrow = await getIsBorrowPromise;
    const itemName = await StorageContract.getItemName(itemID);
    if (isBorrow){
        const returnItemPromise = StorageContract.returnItem(itemID);
        await returnItemPromise;
        document.getElementById('returnFeed').innerHTML = "Return succeed";
    }
    else{    
        const isexist = await isExist(itemID);
        if(isexist){
            document.getElementById('returnFeed').innerHTML = itemName+" has not been borrowed ";
        }
        else{
            document.getElementById('returnFeed').innerHTML = "Item does not exist";
        }
    }
}

async function changeItemName(){
    const itemID = document.getElementById("changeNameItemID").value;
    const newName = document.getElementById("newName").value;
    const isexist = await isExist(itemID);
    if(isexist){
        const changeNamePromise = StorageContract.changeItemName(itemID,newName);
        await changeNamePromise;
        document.getElementById('changeNameFeed').innerHTML = "Item name has been changed to "+newName;
    }
    else{
        document.getElementById('changeNameFeed').innerHTML = "Item does not exist";
    }
}

async function checkStatus() {
    const itemID = document.getElementById("itemIDcheck").value;
    const getIsBorrowPromise = StorageContract.getIsBorrowed(itemID);
    const isBorrow = await getIsBorrowPromise;
    const BorrowingByPromise = StorageContract.getBorrowingBy(itemID);
    const borrowingby = await BorrowingByPromise;
    const itemName = await StorageContract.getItemName(itemID);
    const isexist = await isExist(itemID);
	const borrowTimeRaw = await StorageContract.getBorrowTime(itemID);
	const borrowTime = new Date(borrowTimeRaw * 1000);
    if(isexist){
        document.getElementById('checkItemName1').innerHTML = "Name: ";
		document.getElementById('checkItemName2').innerHTML = itemName;
		document.getElementById('checkItemID1').innerHTML = "ID: ";
		document.getElementById('checkItemID2').innerHTML = itemID;
		if(isBorrow){
        	document.getElementById('checkItemStatus1').innerHTML = "Item is currently being borrowed by ";
			document.getElementById('checkItemStatus2').innerHTML = borrowingby;
			document.getElementById('checkItemTime1').innerHTML = "Borrow time: ";
			document.getElementById('checkItemTime2').innerHTML = borrowTime.toLocaleString('en-GB');
		}
		else{
			document.getElementById('checkItemStatus1').innerHTML = "Item is avaialble for borrow";
			document.getElementById('checkItemStatus2').innerHTML = "";
			document.getElementById('checkItemTime1').innerHTML = "";
			document.getElementById('checkItemTime2').innerHTML = "";
		}

    }
    else{
        document.getElementById('checkItemName1').innerHTML = "Item does not exist";
		document.getElementById('checkItemName2').innerHTML = "";
		document.getElementById('checkItemID1').innerHTML = "";
		document.getElementById('checkItemID2').innerHTML = "";
        document.getElementById('checkItemStatus1').innerHTML = "";
		document.getElementById('checkItemStatus2').innerHTML = "";
		document.getElementById('checkItemTime1').innerHTML = "";
		document.getElementById('checkItemTime2').innerHTML = "";
	}
}

async function isExist(itemID){
    const checkStringPromise = StorageContract.getItemName(itemID);
    const checkString = await checkStringPromise;
    if(checkString != ""){
        return true;
    }
    else{
        return false;
    }
}

async function sortKey(){
	await StorageContract.sort();
}

controlVar = -1;
async function getKeys(){
	keys = await StorageContract.getKeys();
	y = 0;
	for(let i = 0; i < 6; i++){
		const itemID = keys[controlVar];
		const getIsBorrowPromise = StorageContract.getIsBorrowed(itemID);
		const isBorrow = await getIsBorrowPromise;
		const itemName = await StorageContract.getItemName(itemID);

		
		document.getElementById('checkItemName1_'+y).innerHTML = "Name: ";
		document.getElementById('checkItemName2_'+y).innerHTML = itemName;
		document.getElementById('checkItemID1_'+y).innerHTML = "ID: ";
		document.getElementById('checkItemID2_'+y).innerHTML = itemID;
		document.getElementById('checkItemStatus1_'+y).innerHTML = "Status: ";
		if(isBorrow){
			document.getElementById('checkItemStatus2_'+y).innerHTML = "Borrowing";
		}
		else{
			document.getElementById('checkItemStatus2_'+y).innerHTML = "Available";
		}
		
		if(i==5){
		}
		else{
			controlVar++;
		}
		y++;
	}
}

async function allKeyNextPage(){
	keys = await StorageContract.getKeys();
	if(controlVar + 2 > keys.length){
		
	}
	else{
		increaseControlVar();
		clearGetKeyPage();
		getKeys();
	}
}

async function allKeyPrevPage(){
	if((controlVar-7) <= 0){
		controlVar = 0;
	}
	else{
		decreaseControlVar();
	}
		clearGetKeyPage();
		getKeys();
	
}

async function resetControlVar(){
	controlVar = -1;
}

async function increaseControlVar(){
	controlVar += 1;
}

async function decreaseControlVar(){
	controlVar -= 11;
}

async function clearGetKeyPage(){
	for(let i = 0; i < 6; i++){
		document.getElementById('checkItemName1_'+i).innerHTML = "";
		document.getElementById('checkItemName2_'+i).innerHTML = "";
		document.getElementById('checkItemID1_'+i).innerHTML = "";
		document.getElementById('checkItemID2_'+i).innerHTML = "";
		document.getElementById('checkItemStatus1_'+i).innerHTML = "";
		document.getElementById('checkItemStatus2_'+i).innerHTML = "";
	}
}

