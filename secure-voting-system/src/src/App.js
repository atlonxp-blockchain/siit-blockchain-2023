import { ethers } from "ethers";
import * as ReactBootStrap from "react-bootstrap";
import { useState, useEffect } from "react";
import ABIFILE from "./artifacts/contracts/VotingSystem.sol/VotingSytem.json";
import FetchVoter from "./comp/FetchVoter";
import CandidateProposal from "./comp/CandidateProposal";
import Set from "./comp/FetchCandidate";
import Vote from "./comp/Vote";
const ABI = ABIFILE.abi;
const ContractAddress = "YOUR_CONTRACT_ADDRESS";

function App() {
  const [account, setAccount] = useState("");
  const [contract, setContract] = useState(null);
  const [provider, setProvider] = useState(null);
  const [isoff, setOff] = useState(false);
  const [loading, setLoading] = useState(false);

  const Dicconnect = async () => {
    if (typeof window !== "undefined") {
      if (window.localStorage.getItem("Connected")) {
        window.localStorage.removeItem("Connected");
        setOff(false);
        window.location.reload();
      } else {
      }
    }
  };
  useEffect(() => {
    if (typeof window !== "undefined") {
      if (window.localStorage.getItem("Connected")) {
        Connect();
      }
    }
  }, []);

  const Connect = async (e) => {
    // e.preventDefault();
    setLoading(true);
    if (typeof window.ethereum !== "undefined") {
      const account = await window.ethereum.request({
        method: "eth_requestAccounts",
      });

      setOff(true);
      window.localStorage.setItem("Connected", "injected");
      console.log(account);
      setAccount(account);
      document.getElementById("connectbtn").innerHTML = account;

      const provider = new ethers.providers.Web3Provider(window.ethereum);
      setProvider(provider);

      const signer = provider.getSigner();
      console.log(signer);
      const contract = new ethers.Contract(ContractAddress, ABI, signer);
      setContract(contract);
      console.log(contract);
    }
  };
  return (
    <div
      className="mx-auto p-4 text-light  "
      style={{
        width: 1000,
        marginTop: 25,
        backgroundColor: "rgb(255, 255, 255)",
      }}
    >
      <p className="text-center h5 p-2" style={{ color: "black" }}>
         Voting System
      </p>
      <div className="d-flex justify-content-between">
        <button
          onClick={Connect}
          id="connectbtn"
          className="btn btn-dark text-light"
        >
          {!loading ? (
            "Connect"
          ) : (
            <ReactBootStrap.Spinner
              as="span"
              animation="grow"
              size="sm"
              role="status"
              aria-hidden="true"
            />
          )}
        </button>

        <button
          onClick={Dicconnect}
          id="Dissconnectbtn"
          className="btn btn-dark text-light"
          disabled={!isoff}
        >
          Disconnect
        </button>
      </div>

      <br></br>

      <Set contract={contract} account={account} provider={provider} />

      <Vote contract={contract} account={account} provider={provider} />

      <FetchVoter contract={contract} account={account} provider={provider} />

      <CandidateProposal contract={contract} account={account} provider={provider} />
    </div>
  );
}

export default App;
