import React, { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom';
import { ethers } from 'ethers';

import { useStateContext } from '../context';
import { CountBox, CustomButton, Loader, CustomButtonDisabled } from '../components';
import { calculateBarPercentage, daysLeft } from '../utils';
import { thirdweb } from '../assets';
// const _duplicate = true
const CampaignDetails = () => {
  const { state } = useLocation();
  const navigate = useNavigate();
  const { vote, getDonations, contract, address, isDuplicate } = useStateContext();

  const [isLoading, setIsLoading] = useState(false);
  const [amount, setAmount] = useState('');
  const [donators, setDonators] = useState([]);
  const [duplicate, setDuplicate] = useState(true);
  const remainingDays = daysLeft(state.deadline);

  const fetchDuplicate = async () => {
    const data = await isDuplicate(state.pId);
    setDuplicate(data);
  }

  const fetchDonators = async () => {
    const data = await getDonations(state.pId);
    console.log(data)
    setDonators(data);
  }

  // useEffect(() => {
  //   if (contract) fetchDonators();
  // }, [contract, address])


  const handleDonate = async () => {
    setIsLoading(true);

    await vote(state.pId);

    navigate('/')
    setIsLoading(false);
  }

  return (
    <div>
      {isLoading && <Loader />}
      <div className="w-full flex md:flex-row flex-col mt-10 gap-[30px]">
        <div className="flex-1 flex-col">
          <img src={state.image} alt="campaign" className="w-full h-[410px] object-cover rounded-xl" />
          <div className="relative w-full h-[5px] bg-[#3a3a43] mt-2">
            <div className="absolute h-full bg-[#4acd8d]" style={{ width: `${calculateBarPercentage(state.target, state.amountCollected)}%`, maxWidth: '100%' }}>
            </div>
          </div>
        </div>

        <div className="flex md:w-[150px] w-full flex-wrap justify-between gap-[30px]">
          <CountBox title="Days Left" value={remainingDays} />
          <CountBox title={`Target ${state.target}`} value={state.amountCollected} />
          {/* <CountBox title="Total Backers" value={donators.length} /> */}
        </div>
      </div>

      <div className="mt-[60px] flex lg:flex-row flex-col gap-5">
        <div className="flex-[2] flex flex-col gap-[40px]">
          <div>
            <h4 className="font-epilogue font-semibold text-[18px] text-white uppercase">Creator</h4>

            <div className="mt-[20px] flex flex-row items-center flex-wrap gap-[14px]">
              <div className="w-[52px] h-[52px] flex items-center justify-center rounded-full bg-[#2c2f32] cursor-pointer">
                <img src="https://www.theonlinecitizen.com/wp-content/uploads/2023/05/293228377_594570998695346_150969484237986654_n-1.png" alt="user" className="w-[60%] h-[60%] object-contain" />
              </div>
              <div>
                <h4 className="font-epilogue font-semibold text-[14px] text-white break-all">{state.owner}</h4>
                <p className="mt-[4px] font-epilogue font-normal text-[12px] text-[#808191]">10 Campaigns</p>
              </div>
            </div>
          </div>

          <div>
            <h4 className="font-epilogue font-semibold text-[18px] text-white uppercase">Story</h4>

            <div className="mt-[20px]">
              <p className="font-epilogue font-normal text-[16px] text-[#808191] leading-[26px] text-justify">{state.description}</p>
            </div>
          </div>

          {/* <div>
            <h4 className="font-epilogue font-semibold text-[18px] text-white uppercase">Donators {state.donator}</h4>
            <div className="mt-[20px] flex flex-col gap-4">
              {donators.length > 0 ? donators.map((item, index) => (
                <div key={`${item.donator}-${index}`} className="flex justify-between items-center gap-4">
                  <p className="font-epilogue font-normal text-[16px] text-[#b2b3bd] leading-[26px] break-ll">{index + 1}. {item.donator}</p>
                  <p className="font-epilogue font-normal text-[16px] text-[#808191] leading-[26px] break-ll">{item.donation}</p>
                </div>
              )) : (
                <p className="font-epilogue font-normal text-[16px] text-[#808191] leading-[26px] text-justify">No voters yet. Be the first one!</p>
              )}
            </div>
          </div> */}
        </div>

        <div className="flex-1">
          <h4 className="font-epilogue font-semibold text-[18px] text-white uppercase">Vote</h4>

          <div className="mt-[20px] flex flex-col p-4 bg-[#1c1c24] rounded-[10px]">
            <p className="font-epilogue fount-medium text-[20px] leading-[30px] text-center text-[#808191]">
              Vote for this Change
            </p>
            <div className="mt-[30px]">
              <div className="my-[20px] p-4 bg-[#13131a] rounded-[10px]">

                <h4 className="font-epilogue font-semibold text-[14px] leading-[22px] text-white">Voting is not only our right—it is our power.</h4>
                <p className="mt-[20px] font-epilogue font-normal leading-[22px] text-[#808191]"></p>
              </div>
              {/* {duplicate == true ?  <CustomButtonDisabled
                btnType="button"
                title="Vote for this Campaign"
                // styles="w-full bg-[#8c6dfd]"
                styles="w-full bg-grey"
                handleClick={handleDonate}
              /> : <CustomButton
                btnType="button"
                title="Vote for this Campaign"
                styles="w-full bg-[#8c6dfd]"
                // styles="w-full bg-grey"
                handleClick={handleDonate}
              />} */}
              <CustomButton
                btnType="button"
                title="Vote for this Campaign"
                styles="w-full bg-[#8c6dfd]"
                // styles="w-full bg-grey"
                handleClick={handleDonate}
              />



            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CampaignDetails
