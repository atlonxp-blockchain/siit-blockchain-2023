# Smart Contract Voting


> DON'T use this project in PRODUCTION. IT is only useful for EDUCATIONAL Purpose.

```

## Introduction

There are 2 contracts. First is VotingSystem and Second is Election.
All the Election will be created using VotingSystem.

This DapAp is for education purpose not for any production.

Server side Web3js is used for this DApp.
All the transaction will be signed by server.

## Set up

2. npm install (Install all the server and ethereum dependencies)
3. npm install (From client directory to install all the react dependencies)

## Start the DAPP

Open 3 command window or terminal
From Project Root Directory

#### Terminal 1: ganache-cli

#### Terminal 2:

- Step 1: Compile the contract. It will compile and create the binary in the build folder.

```
cd ethereum
node compile.js
```

- Step 2: Run the server

```
npm run dev
```

#### Terminal 3: cd client && npm start

## Election

Every election is active for n minutes. While deploying a new Election duration of election in mins and name of the election must be passed.

All the Create operation(Create Consituency, Voter, Candidate) and Close Election will be done by the Admin only.

Admin can't be a voter or a candidate.

### Step 1:

Compile and Deploy the Election Factory from the home page. http://localhost:3000

Click on Compile to compile the contract.

<img src="./images/compile.PNG"></img>

Click on Deploy to deploy the contract.

<img src="./images/deploy.PNG"></img>

### Step 2:

Create new Election. Pass duration of election in mins and Name of the election.
Click on Create.

<img src="./images/create-election.PNG"></img>

### Step 3:

Go to the new Election.  
Create the Consituencies for the election.  
Pass the consituency Id -- Integer  
Pass the consituency name. String

<img src="./images/add-consituency.PNG"></img>

### Step 4:

Click on Register candidates

<img src="./images/register-candidate.PNG"> </img>

I have created the extra candidates.

Click on Candidates to see all the registered candidates.

<img src="./images/candidates.PNG"></img>

Click on Register voters

<img src="./images/register-voter.PNG"></img>

I have created the extra voters.

Click on the Voters to see all the registered voters.

<img src="./images/voters.PNG"></img>

### Step 5:

Vote Tab: Cast Vote

Cast your vote by selecting the voter. Once the voter is selected its respective constituency candidates will gets loaded.

<img src="./images/cast-vote.PNG"></img>

I casted the remaining votes.

### Step 6:

Result Tab:

1. Click on the Close Election to close the election

<img src="./images/close-election.PNG"></img>

2. Click on the Election Result to get the election result.

<img src="./images/voting-result.PNG"></img>

## License

MIT License

Copyright (c) 2019 Shubham Chadokar
