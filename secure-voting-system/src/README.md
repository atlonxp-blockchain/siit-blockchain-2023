# Voting System Application

This is a simple decentralized voting system application built using React and Ethereum. The application allows users to connect their Ethereum wallet, vote for candidates, fetch voter information, and propose new candidates for the voting system.

## Installation

To run the Voting System Application locally, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/your/repo.git
```

2. Change to the project directory:

```bash
cd project-directory
```

3. Install the dependencies:

```bash
npm install
```

4. Start the development server:

```bash
npm start
```

The application will be running at [http://localhost:3000](http://localhost:3000).

## Usage

1. Connect Ethereum Wallet: Click on the "Connect" button to connect your Ethereum wallet to the application. This will prompt you to authenticate the connection using your wallet.

2. Disconnect Ethereum Wallet: Click on the "Disconnect" button to disconnect your Ethereum wallet from the application.

3. Set Candidates: Use the "Set" component to set the list of candidates for the voting system. This component requires the connected wallet to have the necessary permissions to set candidates.

4. Vote for Candidates: Use the "Vote" component to cast your vote for a specific candidate. This component requires the connected wallet to have the necessary permissions to vote.

5. Fetch Voter Information: Use the "FetchVoter" component to fetch information about a specific voter. This component requires the connected wallet to have the necessary permissions to fetch voter information.

6. Propose New Candidates: Use the "CandidateProposal" component to propose new candidates for the voting system. This component requires the connected wallet to have the necessary permissions to propose candidates.

## Dependencies

The application uses the following dependencies:

- ethers: A JavaScript library for interacting with Ethereum.
- react-bootstrap: A library of reusable UI components for React.
- react: A JavaScript library for building user interfaces.
- web3: Ethereum JavaScript API.
- VotingSystem.sol: Solidity smart contract file that defines the voting system.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, please open an issue or submit a pull request on the GitHub repository.
